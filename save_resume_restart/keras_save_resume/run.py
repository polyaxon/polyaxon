from __future__ import print_function

import argparse

from .data import get_data
from .models import get_model
from .train import train
from .utils import get_depth


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--batch-size',
        type=int,
        default=32)
    parser.add_argument(
        '--epochs',
        type=int,
        default=200)
    parser.add_argument(
        '--data-augmentation',
        type=bool,
        default=True)
    parser.add_argument(
        '--num-classes',
        type=int,
        default=10)
    parser.add_argument(
        '--model-depth-param',
        type=int,
        default=3)
    parser.add_argument(
        '--version',
        type=int,
        default=1,
        help='Orig paper: version = 1 (ResNet v1), Improved ResNet: version = 2 (ResNet v2)')
    args = parser.parse_args()

    # Model parameter
    # ----------------------------------------------------------------------------
    #           |      | 200-epoch | Orig Paper| 200-epoch | Orig Paper| sec/epoch
    # Model     |  n   | ResNet v1 | ResNet v1 | ResNet v2 | ResNet v2 | GTX1080Ti
    #           |v1(v2)| %Accuracy | %Accuracy | %Accuracy | %Accuracy | v1 (v2)
    # ----------------------------------------------------------------------------
    # ResNet20  | 3 (2)| 92.16     | 91.25     | -----     | -----     | 35 (---)
    # ResNet32  | 5(NA)| 92.46     | 92.49     | NA        | NA        | 50 ( NA)
    # ResNet44  | 7(NA)| 92.50     | 92.83     | NA        | NA        | 70 ( NA)
    # ResNet56  | 9 (6)| 92.71     | 93.03     | 93.01     | NA        | 90 (100)
    # ResNet110 |18(12)| 92.65     | 93.39+-.16| 93.15     | 93.63     | 165(180)
    # ResNet164 |27(18)| -----     | 94.07     | -----     | 94.54     | ---(---)
    # ResNet1001| (111)| -----     | 92.39     | -----     | 95.08+-.14| ---(---)
    # ---------------------------------------------------------------------------

    # Model name, depth and version
    depth = get_depth(version=args.version, model_depth_param=args.model_depth_param)
    model_type = 'ResNet%dv%d' % (depth, args.version)

    # Subtracting pixel mean improves accuracy
    subtract_pixel_mean = True
    # Data
    train_data, test_data, input_shape = get_data(subtract_pixel_mean, args.num_classes)

    # Score trained model.
    model = get_model(version=args.version, input_shape=input_shape, depth=depth)
    train(model,
          model_type,
          train_data['x'],
          train_data['y'],
          test_data['x'],
          test_data['y'],
          args.data_augmentation,
          args.batch_size,
          args.epochs)
    scores = model.evaluate(test_data['x'], test_data['y'], verbose=1)
    print('Test loss:', scores[0])
    print('Test accuracy:', scores[1])
