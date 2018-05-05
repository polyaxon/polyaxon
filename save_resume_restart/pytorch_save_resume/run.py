from __future__ import print_function

import argparse

import torch

from data import get_data_loaders
from eval import eval_model
from network import load_model, get_model
from train import train_model
from utils import set_seed, get_weight_filename

from polyaxon_helper import send_metrics

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--batch-size',
        type=int,
        default=128)
    parser.add_argument(
        '--epochs',
        type=int,
        default=12)
    parser.add_argument(
        '--learning-rate',
        type=float,
        default=1e-3)
    parser.add_argument(
        '--num-classes',
        type=int,
        default=12)
    parser.add_argument(
        '--notify',
        type=int,
        default=100)
    args = parser.parse_args()

    cuda = torch.cuda.is_available()
    set_seed(seed=1, cuda=cuda)

    # Data
    train_loader, train_dataset, test_loader, test_dataset = get_data_loaders(
        batch_size=args.batch_size)

    # Model
    model, loss_fn, optimizer = get_model(
        num_classes=args.num_classes,
        learning_rate=args.learning_rate,
        cuda=cuda)
    start_epoch, best_accuracy = load_model(model, cuda)

    for epoch in range(start_epoch, args.epochs):
        train_model(model=model,
                    optimizer=optimizer,
                    train_loader=train_loader,
                    train_dataset=train_dataset,
                    loss_fn=loss_fn,
                    num_epochs=args.epochs,
                    epoch=epoch,
                    batch_size=args.batch_size,
                    notify=args.notify,
                    cuda=cuda)
        accuracy = eval_model(model=model, test_loader=test_loader, cuda=cuda)
        accuracy = 100. * accuracy / len(test_loader.dataset)

        print('Test Accuracy: {:.2f}%'.format(accuracy))
        send_metrics(accuracy=accuracy)

        # Save checkpoint logic
        accuracy = torch.FloatTensor([accuracy])
        best_accuracy = torch.FloatTensor(max(accuracy.numpy(), best_accuracy.numpy()))
        if bool(accuracy.numpy() > best_accuracy.numpy()):
            print('Saving new state for epoch {}'.format(epoch))
            state = {
                'epoch': epoch + 1,
                'state': model.state_dict(),
                'accuracy': best_accuracy
            }
            torch.save(state, get_weight_filename())
        else:
            print('State did not change for epoch {}'.format(epoch))
