import os
import argparse

from cifar10_main import train
from generate_cifar10_tfrecords import generate_data

from polyaxon_helper import get_data_path, get_outputs_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--variable-strategy',
        choices=['CPU', 'GPU'],
        type=str,
        default='CPU',
        help='Where to locate variable operations')
    parser.add_argument(
        '--num-gpus',
        type=int,
        default=0,
        help='The number of gpus used. Uses only CPU if set to 0.')
    parser.add_argument(
        '--num-layers',
        type=int,
        default=44,
        help='The number of layers of the model.')
    parser.add_argument(
        '--train-steps',
        type=int,
        default=80000,
        help='The number of steps to use for training.')
    parser.add_argument(
        '--train-batch-size',
        type=int,
        default=128,
        help='Batch size for training.')
    parser.add_argument(
        '--eval-batch-size',
        type=int,
        default=100,
        help='Batch size for validation.')
    parser.add_argument(
        '--momentum',
        type=float,
        default=0.9,
        help='Momentum for MomentumOptimizer.')
    parser.add_argument(
        '--weight-decay',
        type=float,
        default=2e-4,
        help='Weight decay for convolutions.')
    parser.add_argument(
        '--learning-rate',
        type=float,
        default=0.1,
        help="""\
      This is the inital learning rate value. The learning rate will decrease
      during training. For more details check the model_fn implementation in
      this file.\
      """)
    parser.add_argument(
        '--use-distortion-for-training',
        type=bool,
        default=True,
        help='If doing image distortion for training.')
    parser.add_argument(
        '--sync',
        action='store_true',
        default=False,
        help="""\
      If present when running in a distributed environment will run on sync mode.\
      """)
    parser.add_argument(
        '--num-intra-threads',
        type=int,
        default=0,
        help="""\
      Number of threads to use for intra-op parallelism. When training on CPU
      set to 0 to have the system pick the appropriate number or alternatively
      set it to the number of physical CPU cores.\
      """)
    parser.add_argument(
        '--num-inter-threads',
        type=int,
        default=0,
        help="""\
      Number of threads to use for inter-op parallelism. If set to 0, the
      system will pick an appropriate number.\
      """)
    parser.add_argument(
        '--data-format',
        type=str,
        default=None,
        help="""\
      If not set, the data format best for the training device is used. 
      Allowed values: channels_first (NCHW) channels_last (NHWC).\
      """)
    parser.add_argument(
        '--log-device-placement',
        action='store_true',
        default=False,
        help='Whether to log device placement.')
    parser.add_argument(
        '--batch-norm-decay',
        type=float,
        default=0.997,
        help='Decay for batch norm.')
    parser.add_argument(
        '--batch-norm-epsilon',
        type=float,
        default=1e-5,
        help='Epsilon for batch norm.')
    args = parser.parse_args()

    if args.num_gpus < 0:
        raise ValueError(
            'Invalid GPU count: \"--num-gpus\" must be 0 or a positive integer.')
    if args.num_gpus == 0 and args.variable_strategy == 'GPU':
        raise ValueError('num-gpus=0, CPU must be used as parameter server. Set'
                         '--variable-strategy=CPU.')
    if (args.num_layers - 2) % 6 != 0:
        raise ValueError('Invalid --num-layers parameter.')
    if args.num_gpus != 0 and args.train_batch_size % args.num_gpus != 0:
        raise ValueError('--train-batch-size must be multiple of --num-gpus.')
    if args.num_gpus != 0 and args.eval_batch_size % args.num_gpus != 0:
        raise ValueError('--eval-batch-size must be multiple of --num-gpus.')

    data_dir = os.path.join(list(get_data_path().values())[0], 'cifar-10-data')
    # We create data for the project if it does not exists
    if not os.path.exists(os.path.join(data_dir, 'train.tfrecords')):
        generate_data(data_dir)

    train(job_dir=get_outputs_path(), data_dir=data_dir, **vars(args))
