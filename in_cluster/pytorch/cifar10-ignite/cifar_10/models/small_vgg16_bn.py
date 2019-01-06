# Code is adapted from torchvision.models.vgg
from torch.nn import Sequential, ReLU, Dropout, Linear
from torchvision.models.vgg import vgg16_bn


def get_small_vgg16_bn(num_classes):

    model = vgg16_bn(num_classes=num_classes)

    model.classifier = Sequential(
        Linear(512, 512),
        ReLU(True),
        Dropout(),
        Linear(512, 512),
        ReLU(True),
        Dropout(),
        Linear(512, num_classes),
    )
    model._initialize_weights()
    return model