import argparse
import logging

# Polyaxon
from polyaxon.tracking import Run

from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

logger = logging.getLogger()


def model(log_learning_rate, max_depth=3, num_rounds=10, min_child_weight=5):
    model = XGBClassifier(
        learning_rate=10 ** log_learning_rate,
        max_depth=max_depth,
        num_rounds=num_rounds,
        min_child_weight=min_child_weight,
        objective='binary:logistic',
    )
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    return accuracy_score(pred, y_test)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--log_learning_rate',
        type=int,
        default=-3
    )
    parser.add_argument(
        '--max_depth',
        type=int,
        default=3
    )
    parser.add_argument(
        '--num_rounds',
        type=int,
        default=10
    )
    parser.add_argument(
        '--min_child_weight',
        type=int,
        default=5
    )
    args = parser.parse_args()

    # Polyaxon
    experiment = Run(project='iris')
    experiment.create(tags=['examples', 'xgboost'])
    experiment.log_inputs(log_learning_rate=args.log_learning_rate,
                          max_depth=args.max_depth,
                          num_rounds=args.num_rounds,
                          min_child_weight=args.min_child_weight)

    iris = load_iris()
    X = iris.data
    Y = iris.target

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

    # Polyaxon
    experiment.log_data_ref(content=X_train, name='x_train')
    experiment.log_data_ref(content=y_train, name='y_train')
    experiment.log_data_ref(content=X_test, name='X_test')
    experiment.log_data_ref(content=y_test, name='y_train')

    logger.info('Train model...')
    accuracy = model(log_learning_rate=args.log_learning_rate,
                     max_depth=args.max_depth,
                     num_rounds=args.num_rounds,
                     min_child_weight=args.min_child_weight)
    experiment.log_outputs(accuracy=accuracy)
