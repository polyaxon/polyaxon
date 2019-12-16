import argparse

# Polyaxon
from polyaxon_client.tracking import Experiment, get_outputs_path

from model import train_and_eval

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--ngram',
        type=int,
        default=1,
        help='n-gram size.')
    parser.add_argument(
        '--max_features',
        type=int,
        default=2000,
        help='The maximum number of features.')
    parser.add_argument(
        '--max_df',
        type=float,
        default=1.0,
        help='the maximum document frequency.')
    parser.add_argument(
        '--C',
        type=float,
        default=1.0,
        help='Inverse of regularization strength of LogisticRegression')
    args = parser.parse_args()

    # Polyaxon
    experiment = Experiment(project='newsgroup')
    experiment.create(framework='scikit-learn', tags=['examples'])
    experiment.log_params(ngram_range=(args.ngram, args.ngram),
                          max_features=args.max_features,
                          max_df=args.max_df,
                          C=args.C)

    # Train and eval the model with given parameters.
    # Polyaxon
    metrics = train_and_eval(ngram_range=(args.ngram, args.ngram),
                             max_features=args.max_features,
                             max_df=args.max_df,
                             C=args.C)

    # Logging metrics
    print("Testing metrics: {}", metrics)
    # Polyaxon
    experiment.log_metrics(**metrics)
