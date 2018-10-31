
from torchvision.transforms import RandomVerticalFlip, RandomHorizontalFlip, ColorJitter, ToTensor, Normalize
from torchvision.transforms.functional import _is_pil_image


def convert_colorspace(img, mode):
    if not _is_pil_image(img):
        raise TypeError('img should be PIL Image. Got {}'.format(type(img)))
    if mode not in ("RGB", "YCbCr", "HSV"):
        raise TypeError('mode should be one of "RGB", "YCbCr", "HSV". Got {}'.format(mode))
    return img.convert(mode)


class ConvertColorspace(object):
    def __init__(self, mode):

        assert mode in ("RGB", "YCbCr", "HSV")
        self.mode = mode

    def __call__(self, img):
        return convert_colorspace(img, self.mode)

    def __repr__(self):
        return self.__class__.__name__ + '(mode={})'.format(self.mode)


train_data_transform = [
    RandomHorizontalFlip(p=0.5),
    RandomVerticalFlip(p=0.5),
    ColorJitter(hue=0.1, brightness=0.1),
    ConvertColorspace("YCbCr"),
    ToTensor(),
    Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
]


val_data_transform = [
    RandomHorizontalFlip(p=0.5),
    RandomVerticalFlip(p=0.5),
    ConvertColorspace("YCbCr"),
    ToTensor(),
    Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
]


test_data_transform = val_data_transform
