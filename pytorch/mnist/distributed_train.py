from __future__ import print_function

import logging
from random import Random

import torch
import torch.distributed as dist
import torch.nn.functional as F
from torch.autograd import Variable
from torchvision import datasets, transforms

from polyaxon_helper import send_metrics

logging.basicConfig(level=logging.INFO)


class Partition(object):
    """ Dataset-like object, but only access a subset of it. """

    def __init__(self, data, index):
        self.data = data
        self.index = index

    def __len__(self):
        return len(self.index)

    def __getitem__(self, index):
        data_idx = self.index[index]
        return self.data[data_idx]


class DataPartitioner(object):
    """ Partitions a dataset into different chuncks. """

    def __init__(self, data, sizes=[0.7, 0.2, 0.1], seed=1234):
        self.data = data
        self.partitions = []
        rng = Random()
        rng.seed(seed)
        data_len = len(data)
        indexes = [x for x in range(0, data_len)]
        rng.shuffle(indexes)
        for frac in sizes:
            part_len = int(frac * data_len)
            self.partitions.append(indexes[0:part_len])
            indexes = indexes[part_len:]

    def use(self, partition):
        return Partition(self.data, self.partitions[partition])


def partition_dataset(data_dir, batch_size, seed):
    """ Partitioning MNIST """
    dataset = datasets.MNIST(data_dir, train=True, download=True,
                             transform=transforms.Compose([
                                 transforms.ToTensor(),
                                 transforms.Normalize((0.1307,), (0.3081,))
                             ]))
    size = dist.get_world_size()
    partition_batch_size = batch_size / float(size)
    partition_sizes = [1.0 / size for _ in range(size)]
    partition = DataPartitioner(dataset, partition_sizes, seed=seed)
    partition = partition.use(dist.get_rank())
    train_set = torch.utils.data.DataLoader(partition,
                                            batch_size=partition_batch_size,
                                            shuffle=True)
    return train_set, partition_batch_size


def average_gradients(model):
    """ Gradient averaging. """
    size = float(dist.get_world_size())
    for param in model.parameters():
        dist.all_reduce(param.grad.data, op=dist.reduce_op.SUM, group=0)
        param.grad.data /= size


def distributed_train(model, train_set, epoch, optimizer, rank, num_batches, log_interval):
    """ Distributed Synchronous SGD Example """
    epoch_loss = 0.0
    train_dataset = [d for d in train_set]
    for batch_idx, (data, target) in enumerate(train_dataset):
        data, target = Variable(data), Variable(target)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        epoch_loss += loss.data[0]
        loss.backward()
        average_gradients(model)
        optimizer.step()
        if batch_idx % log_interval == 0:
            logging.info(
                'Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                    epoch,
                    batch_idx * len(data),
                    len(train_set.dataset),
                    100. * batch_idx / len(train_dataset),
                    loss.data[0])
            )
    logging.info('Rank {}, epoch: {}, loss: {}'.format(rank, epoch, epoch_loss / num_batches))
    send_metrics(loss=epoch_loss / num_batches)
