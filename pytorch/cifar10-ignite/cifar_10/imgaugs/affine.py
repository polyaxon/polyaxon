
from torchvision.transforms import RandomVerticalFlip, RandomHorizontalFlip, RandomChoice, RandomAffine
from torchvision.transforms import ColorJitter, ToTensor, Normalize


train_data_transform = [
    RandomChoice([
        RandomAffine(degrees=(-50, 50), translate=(0.05, 0.05)),
        RandomHorizontalFlip(p=0.5),
        RandomVerticalFlip(p=0.5),
    ]),
    ColorJitter(hue=0.1),
    ToTensor(),
    Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
]


val_data_transform = [
    RandomHorizontalFlip(p=0.5),
    RandomVerticalFlip(p=0.5),
    ToTensor(),
    Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
]

test_data_transform = val_data_transform

