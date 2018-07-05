from __future__ import print_function

import argparse
import logging

import os
import torch
import torch.optim as optim

from polyaxon_helper import get_data_paths

from network import Network
from train import train, test, get_test_loader, get_train_loader

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PyTorch MNIST Example')
    parser.add_argument('--batch-size', type=int, default=64, metavar='N',
                        help='input batch size for training (default: 64)')
    parser.add_argument('--test-batch-size', type=int, default=1000, metavar='N',
                        help='input batch size for testing (default: 1000)')
    parser.add_argument('--epochs', type=int, default=10, metavar='N',
                        help='number of epochs to train (default: 10)')
    parser.add_argument('--lr', type=float, default=0.01, metavar='LR',
                        help='learning rate (default: 0.01)')
    parser.add_argument('--momentum', type=float, default=0.5, metavar='M',
                        help='SGD momentum (default: 0.5)')
    parser.add_argument('--no-cuda', action='store_true', default=False,
                        help='disables CUDA training')
    parser.add_argument('--seed', type=int, default=1, metavar='S',
                        help='random seed (default: 1)')
    parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                        help='how many batches to wait before logging training status')
    args = parser.parse_args()
    args.cuda = not args.no_cuda and torch.cuda.is_available()

    torch.manual_seed(args.seed)
    if args.cuda:
        torch.cuda.manual_seed(args.seed)

    model = Network()
    if args.cuda:
        model.cuda()

    data_dir = os.path.join(list(get_data_paths().values())[0], 'pytorch', 'mnist')

    logging.info('Downloading data ...')
    train_loader = get_train_loader(data_dir, args.batch_size, args.cuda)
    test_loader = get_test_loader(data_dir, args.test_batch_size, args.cuda)
    optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum)
    logging.info('Start training ...')
    for epoch in range(1, args.epochs + 1):
        train(model=model,
              train_loader=train_loader,
              epoch=epoch,
              cuda=args.cuda,
              optimizer=optimizer,
              log_interval=args.log_interval)
        test(model=model, test_loader=test_loader, cuda=args.cuda)
