from __future__ import print_function

from time import time

import joblib

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics.classification import accuracy_score, f1_score, recall_score


def train_and_eval(output, ngram_range=(1, 1), max_features=None, max_df=1.0, C=1.0):
    """Train and eval newsgroup classification.

    :param ngram_range: ngram range
    :param max_features: the number of maximum features
    :param max_df: max document frequency ratio
    :param C: Inverse of regularization strength for LogisticRegression
    :return: metrics
    """
    # Loads train and test data.
    train_data = fetch_20newsgroups(subset='train')
    test_data = fetch_20newsgroups(subset='test')

    # Define the pipeline.
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', LogisticRegression(multi_class='auto'))
    ])

    # Set pipeline parameters.
    params = {
        'tfidf__ngram_range': ngram_range,
        'tfidf__max_features': max_features,
        'tfidf__max_df': max_df,
        'clf__C': C,
    }
    pipeline.set_params(**params)
    print(pipeline.get_params().keys())

    # Train the model.
    pipeline.fit(train_data.data, train_data.target)
    # Predict test data.
    start_time = time()
    predictions = pipeline.predict(test_data.data)
    inference_time = time() - start_time
    avg_inference_time = 1.0 * inference_time / len(test_data.target)
    print("Avg. inference time: {}".format(avg_inference_time))

    # Calculate the metrics.
    accuracy = accuracy_score(test_data.target, predictions)
    recall = recall_score(test_data.target, predictions, average='weighted')
    f1 = f1_score(test_data.target, predictions, average='weighted')
    metrics = {
        'accuracy': accuracy,
        'recall': recall,
        'f1': f1,
    }

    # Persistent the model.
    joblib.dump(pipeline, output)

    return metrics
