import argparse
import logging
import mxnet as mx
import os

# Polyaxon
from polyaxon import tracking

logger = logging.getLogger('mnist')


def model(context,
          train_iter,
          val_iter,
          conv1_kernel,
          conv1_filters,
          conv1_activation,
          conv2_kernel,
          conv2_filters,
          conv2_activation,
          fc1_hidden,
          fc1_activation,
          optimizer,
          log_learning_rate,
          batch_size,
          epochs):

    data = mx.sym.Variable('data')
    conv1 = mx.sym.Convolution(
        data=data,
        kernel=(conv1_kernel, conv1_kernel),
        num_filter=conv1_filters,
    )
    act1 = mx.sym.Activation(data=conv1, act_type=conv1_activation)
    pool1 = mx.sym.Pooling(data=act1, pool_type="max", kernel=(2, 2), stride=(2, 2))
    conv2 = mx.sym.Convolution(
        data=pool1,
        kernel=(conv2_kernel, conv2_kernel),
        num_filter=conv2_filters,
    )
    act2 = mx.sym.Activation(data=conv2, act_type=conv2_activation)
    pool2 = mx.sym.Pooling(data=act2, pool_type="max", kernel=(2, 2), stride=(2, 2))
    flatten = mx.sym.Flatten(data=pool2)
    fc1 = mx.symbol.FullyConnected(data=flatten, num_hidden=fc1_hidden)
    act3 = mx.sym.Activation(data=fc1, act_type=fc1_activation)
    fc2 = mx.symbol.FullyConnected(data=act3, num_hidden=10)
    net = mx.sym.SoftmaxOutput(data=fc2, name='softmax')
    net = mx.mod.Module(net, context=context())

    net.fit(
        train_iter,
        eval_metric='acc',
        optimizer=optimizer,
        optimizer_params={
            'learning_rate': 10 ** log_learning_rate
        },
        batch_end_callback=mx.callback.Speedometer(batch_size, 100),
        num_epoch=epochs,
    )

    return net.score(val_iter, mx.metric.Accuracy())[0][1]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--conv1_kernel',
        type=int,
        default=5)
    parser.add_argument(
        '--conv1_filters',
        type=int,
        default=10
    )
    parser.add_argument(
        '--conv1_activation',
        type=str,
        default='relu'
    )
    parser.add_argument(
        '--conv2_kernel',
        type=int,
        default=5)
    parser.add_argument(
        '--conv2_filters',
        type=int,
        default=10
    )
    parser.add_argument(
        '--conv2_activation',
        type=str,
        default='relu'
    )
    parser.add_argument(
        '--fc1_hidden',
        type=int,
        default=10
    )
    parser.add_argument(
        '--fc1_activation',
        type=str,
        default='relu'
    )
    parser.add_argument(
        '--optimizer',
        type=str,
        default='adam'
    )
    parser.add_argument(
        '--log_learning_rate',
        type=int,
        default=-3
    )
    parser.add_argument(
        '--batch_size',
        type=int,
        default=100
    )
    parser.add_argument(
        '--epochs',
        type=int,
        default=1
    )
    args = parser.parse_args()

    # Polyaxon
    tracking.init()

    logger.info('Downloading data ...')
    mnist = mx.test_utils.get_mnist()
    train_iter = mx.io.NDArrayIter(mnist['train_data'], mnist['train_label'], args.batch_size,
                                   shuffle=True)
    val_iter = mx.io.NDArrayIter(mnist['test_data'], mnist['test_label'], args.batch_size)

    # Polyaxon
    tracking.log_data_ref(content=mnist['train_data'], name='x_train')
    tracking.log_data_ref(content=mnist['train_label'], name='y_train')
    tracking.log_data_ref(content=mnist['test_data'], name='x_test')
    tracking.log_data_ref(content=mnist['test_label'], name='y_test')

    context = mx.gpu if os.environ.get('NVIDIA_VISIBLE_DEVICES') else mx.cpu

    metrics = model(context=context,
                    train_iter=train_iter,
                    val_iter=val_iter,
                    conv1_kernel=args.conv1_kernel,
                    conv1_filters=args.conv1_filters,
                    conv1_activation=args.conv1_activation,
                    conv2_kernel=args.conv1_kernel,
                    conv2_filters=args.conv1_filters,
                    conv2_activation=args.conv1_activation,
                    fc1_hidden=args.fc1_hidden,
                    fc1_activation=args.fc1_activation,
                    optimizer=args.optimizer,
                    log_learning_rate=args.log_learning_rate,
                    batch_size=args.batch_size,
                    epochs=args.epochs)

    # Polyaxon
    tracking.log_metrics(accuracy=metrics)
