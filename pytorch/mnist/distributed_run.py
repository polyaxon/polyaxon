from __future__ import print_function

import argparse
import logging
from math import ceil

import os
import torch
import torch.distributed as dist
import torch.optim as optim

from polyaxon_helper import get_data_paths

from distributed_train import distributed_train, partition_dataset
from network import Network

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PyTorch MNIST Example')
    parser.add_argument('--batch-size', type=int, default=128, metavar='N',
                        help='input batch size for training (default: 128)')
    parser.add_argument('--test-batch-size', type=int, default=1000, metavar='N',
                        help='input batch size for testing (default: 1000)')
    parser.add_argument('--epochs', type=int, default=10, metavar='N',
                        help='number of epochs to train (default: 10)')
    parser.add_argument('--lr', type=float, default=0.01, metavar='LR',
                        help='learning rate (default: 0.01)')
    parser.add_argument('--momentum', type=float, default=0.5, metavar='M',
                        help='SGD momentum (default: 0.5)')
    parser.add_argument('--seed', type=int, default=1, metavar='S',
                        help='random seed (default: 1)')
    parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                        help='how many batches to wait before logging training status')
    args = parser.parse_args()

    logging.info('initializing process')
    dist.init_process_group('tcp')
    rank = dist.get_rank()
    torch.manual_seed(args.seed)

    model = Network()

    data_dir = os.path.join(list(get_data_paths().values())[0], 'pytorch', 'mnist')

    train_set, bsz = partition_dataset(data_dir=data_dir,
                                       batch_size=args.batch_size,
                                       seed=args.seed)
    optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum)
    num_batches = ceil(len(train_set.dataset) / float(bsz))
    logging.info('Start training ...')
    for epoch in range(1, args.epochs + 1):
        distributed_train(model=model,
                          train_set=train_set,
                          epoch=epoch,
                          optimizer=optimizer,
                          rank=rank,
                          num_batches=num_batches,
                          log_interval=args.log_interval)
