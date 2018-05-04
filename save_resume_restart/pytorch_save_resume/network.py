import os

import torch
import torch.nn as nn
import torch.nn.functional as F

from utils import get_weight_filename


class Network(nn.Module):
    def __init__(self, num_classes):
        super(Network, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3)
        self.drop1 = nn.Dropout2d(p=0.25)
        self.fc1 = nn.Linear(9216, 128)
        self.drop2 = nn.Dropout2d(p=0.5)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = self.drop1(x)
        x = x.view(-1, 9216)
        x = F.relu(self.fc1(x))
        x = self.drop2(x)
        x = self.fc2(x)
        return F.log_softmax(x)


def get_model(num_classes, learning_rate, cuda):
    model = Network(num_classes)

    # If you are running a GPU instance, load the model on GPU
    if cuda:
        model.cuda()

    loss_fn = nn.CrossEntropyLoss()
    # If you are running a GPU instance, compute the loss on GPU
    if cuda:
        loss_fn.cuda()

    # Set parameters to be updated.
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    return model, loss_fn, optimizer


def load_model(model, cuda):
    filename = get_weight_filename()
    if not os.path.isfile(filename):
        return 0, torch.FloatTensor([0])

    print('Loading model from {}'.format(filename))
    if cuda:
        checkpoint = torch.load(filename)
    else:
        checkpoint = torch.load(filename, map_location=lambda storage, loc: storage)
    start_epoch = checkpoint['epoch']
    best_accuracy = checkpoint['accuracy']
    model.load_state_dict(checkpoint['state'])
    print('Last epoch: {}'.format(start_epoch))
    return start_epoch, best_accuracy
