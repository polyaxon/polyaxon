import argparse
import logging

from keras.datasets import imdb
from keras import optimizers
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras.layers import Conv1D, MaxPooling1D
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding
from keras.layers import LSTM
from keras.models import Sequential
from keras.preprocessing import sequence

# Polyaxon
from polyaxon import tracking
from polyaxon.tracking.contrib.keras import PolyaxonCallback

logger = logging.getLogger('cnn-lstm')

OPTIMIZERS = {
    'adam': optimizers.Adam,
    'rmsprop': optimizers.RMSprop,
    'sgd': optimizers.SGD,
}


def transform_data(x_train, y_train, x_test, y_test, maxlen):
    x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
    x_test = sequence.pad_sequences(x_test, maxlen=maxlen)
    return x_train, y_train, x_test, y_test


def train(max_features,
          maxlen,
          embedding_size,
          kernel_size,
          optimizer,
          filters, pool_size, lstm_output_size,
          log_learning_rate,
          batch_size,
          epochs):
    model = Sequential()
    model.add(Embedding(max_features, embedding_size, input_length=maxlen))
    model.add(Dropout(0.25))
    model.add(Conv1D(filters,
                     kernel_size,
                     padding='valid',
                     activation='relu',
                     strides=1))
    model.add(MaxPooling1D(pool_size=pool_size))
    model.add(LSTM(lstm_output_size))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(OPTIMIZERS[optimizer](lr=10 ** log_learning_rate),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              validation_data=(x_test, y_test),
              callbacks=[
                  PolyaxonCallback(),
                  TensorBoard(log_dir=tracking.get_tensorboard_path(), histogram_freq=1),
                  ModelCheckpoint(tracking.get_outputs_path("model"))
              ])

    score, accuracy = model.evaluate(x_test, y_test, batch_size=batch_size)
    return score, accuracy


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--max_features',
        type=int,
        default=20000)
    parser.add_argument(
        '--skip_top',
        type=int,
        default=50,
        help='Top occurring words to skip'
    )
    parser.add_argument(
        '--maxlen',
        type=int,
        default=100
    )
    parser.add_argument(
        '--embedding_size',
        type=int,
        default=128
    )
    parser.add_argument(
        '--pool_size',
        type=int,
        default=4
    )
    parser.add_argument(
        '--kernel_size',
        type=int,
        default=5
    )
    parser.add_argument(
        '--filters',
        type=int,
        default=64
    )
    parser.add_argument(
        '--lstm_output_size',
        type=int,
        default=70
    )
    parser.add_argument(
        '--batch_size',
        type=int,
        default=32
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
        '--epochs',
        type=int,
        default=1
    )
    args = parser.parse_args()

    # Polyaxon
    tracking.init()

    logger.info('Loading data...')
    (x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=args.max_features,
                                                          skip_top=args.skip_top)

    logger.info('train sequences %s', len(x_train))
    logger.info('test sequences %s', len(x_test))

    # Polyaxon
    tracking.log_data_ref(content=x_train, name='x_train')
    tracking.log_data_ref(content=y_train, name='y_train')
    tracking.log_data_ref(content=x_test, name='x_test')
    tracking.log_data_ref(content=y_test, name='y_test')

    logger.info('Transforming data...')
    x_train, y_train, x_test, y_test = transform_data(x_train,
                                                      y_train,
                                                      x_test,
                                                      y_test,
                                                      args.maxlen)

    logger.info('Training...')
    score, accuracy = train(max_features=args.max_features,
                            maxlen=args.maxlen,
                            epochs=args.epochs,
                            embedding_size=args.embedding_size,
                            pool_size=args.pool_size,
                            kernel_size=args.kernel_size,
                            filters=args.filters,
                            lstm_output_size=args.lstm_output_size,
                            batch_size=args.batch_size,
                            optimizer=args.optimizer,
                            log_learning_rate=args.log_learning_rate)

    # Polyaxon
    tracking.log_metrics(eval_score=score, eval_accuracy=accuracy)

    logger.info('Test score: %s', score)
    logger.info('Test accuracy: %s', accuracy)
