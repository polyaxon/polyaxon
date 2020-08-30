import argparse

# Polyaxon
from polyaxon import tracking

from model import train_and_eval

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--n_neighbors',
        type=int,
        default=3,
    )
    parser.add_argument(
        '--leaf_size',
        type=int,
        default=30,
    )
    parser.add_argument(
        '--metric',
        type=str,
        default='minkowski',
    )
    parser.add_argument(
        '--p',
        type=int,
        default=2,
    )
    parser.add_argument(
        '--weights',
        type=str,
        default='uniform',
    )
    parser.add_argument(
        '--test_size',
        type=float,
        default=0.3,
    )
    parser.add_argument(
        '--random_state',
        type=int,
        default=33,
    )
    args = parser.parse_args()

    # Polyaxon
    tracking.init()

    # Train and eval the model with given parameters.
    # Polyaxon
    model_path = "model.joblib"
    metrics = train_and_eval(
        model_path=model_path,
        n_neighbors=args.n_neighbors,
        leaf_size=args.leaf_size,
        metric=args.metric,
        p=args.p,
        weights=args.weights,
        test_size=args.test_size,
        random_state=args.random_state,
    )

    # Logging metrics to Polyaxon
    print("Testing metrics: {}", metrics)
    # Polyaxon
    tracking.log_metrics(**metrics)

    # Logging the model
    tracking.log_model(model_path, name="iris-model", framework="scikit-learn")
