from __future__ import division
from __future__ import print_function


import logging
import os

import torch

from torchvision import datasets
from torchvision import transforms

from polyaxon_helper import get_data_path

logging.basicConfig(level=logging.INFO)


def get_data_loaders(batch_size):
    data_dir = os.path.join(get_data_path(), 'pytorch', 'mnist')

    train_dataset = datasets.MNIST(root=data_dir,
                                   train=True,
                                   download=True,
                                   transform=transforms.ToTensor())
    x_train_mnist = train_dataset.train_data.type(torch.FloatTensor)
    y_train_mnist = train_dataset.train_labels

    test_dataset = datasets.MNIST(root=data_dir,
                                  train=False,
                                  download=True,
                                  transform=transforms.ToTensor())
    x_test_mnist = test_dataset.test_data.type(torch.FloatTensor)
    y_test_mnist = test_dataset.test_labels

    logging.info('Training Data Size: ', x_train_mnist.size(), '-', y_train_mnist.size())
    logging.info('Testing Data Size: ', x_test_mnist.size(), '-', y_test_mnist.size())

    train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                               batch_size=batch_size,
                                               shuffle=True)
    test_loader = torch.utils.data.DataLoader(dataset=test_dataset,
                                              batch_size=batch_size,
                                              shuffle=False)

    return train_loader, train_dataset, test_loader, test_dataset
