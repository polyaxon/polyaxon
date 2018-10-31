# Code is adapted from torchvision.models.squeezenet
import torch
from torch.nn import Conv2d, AdaptiveAvgPool2d, Sequential, Module, ReLU, BatchNorm2d, MaxPool2d, Dropout
from torch.nn.init import normal, kaiming_uniform
from torchvision.models.squeezenet import squeezenet1_1


def get_small_squeezenet_v1_1(num_classes):

    model = squeezenet1_1(num_classes=num_classes, pretrained=False)
    # As input image size is small 64x64, we modify first layers:
    # replace : Conv2d(3, 64, (3, 3), stride=(2, 2)) by Conv2d(3, 64, (3, 3), stride=(1, 1), padding=1)
    # replace : MaxPool2d (size=(3, 3), stride=(2, 2), dilation=(1, 1)))
    # by MaxPool2d (size=(2, 2), stride=(1, 1))
    layers = [l for i, l in enumerate(model.features)]
    layers[0] = Conv2d(3, 64, kernel_size=(3, 3), padding=1)
    layers[2] = MaxPool2d(kernel_size=2, stride=1)
    model.features = Sequential(*layers)
    # Replace the last AvgPool2d -> AdaptiveAvgPool2d
    layers = [l for l in model.classifier]
    layers[-1] = AdaptiveAvgPool2d(1)
    model.classifier = Sequential(*layers)
    return model


class FireBN(Module):

    def __init__(self, inplanes, squeeze_planes,
                 expand1x1_planes, expand3x3_planes):
        super(FireBN, self).__init__()
        self.inplanes = inplanes
        self.squeeze = Conv2d(inplanes, squeeze_planes, kernel_size=1)
        self.squeeze_bn = BatchNorm2d(squeeze_planes)
        self.squeeze_activation = ReLU(inplace=True)
        self.expand1x1 = Conv2d(squeeze_planes, expand1x1_planes,
                                kernel_size=1)
        self.expand1x1_bn = BatchNorm2d(expand1x1_planes)
        self.expand1x1_activation = ReLU(inplace=True)
        self.expand3x3 = Conv2d(squeeze_planes, expand3x3_planes,
                                kernel_size=3, padding=1)
        self.expand3x3_bn = BatchNorm2d(expand3x3_planes)
        self.expand3x3_activation = ReLU(inplace=True)

    def forward(self, x):
        x = self.squeeze(x)
        x = self.squeeze_bn(x)
        x = self.squeeze_activation(x)

        x1 = self.expand1x1(x)
        x1 = self.expand1x1_bn(x1)
        x1 = self.expand1x1_activation(x1)
        x2 = self.expand3x3(x)
        x2 = self.expand3x3_bn(x2)
        x2 = self.expand3x3_activation(x2)
        return torch.cat([x1, x2], 1)


class SqueezeNetV11BN(Module):

    def __init__(self, num_classes=1000):
        super(SqueezeNetV11BN, self).__init__()
        self.num_classes = num_classes

        self.features = Sequential(
            Conv2d(3, 64, kernel_size=3, stride=1, padding=1),
            BatchNorm2d(64),
            ReLU(inplace=True),
            MaxPool2d(kernel_size=2, stride=1),
            FireBN(64, 16, 64, 64),
            FireBN(128, 16, 64, 64),
            MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            FireBN(128, 32, 128, 128),
            FireBN(256, 32, 128, 128),
            MaxPool2d(kernel_size=3, stride=2, ceil_mode=True),
            FireBN(256, 48, 192, 192),
            FireBN(384, 48, 192, 192),
            FireBN(384, 64, 256, 256),
            FireBN(512, 64, 256, 256),
        )
        # Final convolution is initialized differently form the rest
        final_conv = Conv2d(512, self.num_classes, kernel_size=1)
        self.classifier = Sequential(
            Dropout(p=0.5),
            final_conv,
            ReLU(inplace=True),
            AdaptiveAvgPool2d(1)
        )

        for m in self.modules():
            if isinstance(m, Conv2d):
                if m is final_conv:
                    normal(m.weight.data, mean=0.0, std=0.01)
                else:
                    kaiming_uniform(m.weight.data)
                if m.bias is not None:
                    m.bias.data.zero_()

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x.view(x.size(0), self.num_classes)
