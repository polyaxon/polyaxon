import os
import argparse

from polyaxon_helper import get_data_paths, get_outputs_path
from polyaxon_client.tracking import Experiment, get_log_level, get_data_paths, get_outputs_path
from polyaxon_helper import send_metrics
from model import train_and_eval

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--ngram',
        type=float,
        default=1.0,
        help='n-gram size.')
    parser.add_argument(
        '--max_features',
        type=float,
        default=None,
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

    experiment = Experiment()

    # Train and eval the model with given parameters.
    output_path = os.path.join(get_outputs_path(), "model.joblib")
    metrics = train_and_eval(output=output_path,
                             ngram_range=(int(args.ngram), int(args.ngram)),
                             max_features=int(args.max_features),
                             max_df=args.max_df,
                             C=args.C)

    # Logging metrics
    print("Testing metrics: {}", metrics)
    experiment.log_metrics(recall=metrics['recall'],
                           accuracy=metrics['accuracy'],
                           f1=metrics['f1'])
    send_metrics(**metrics)
