import joblib

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.datasets import load_iris


def train_and_eval(
    n_neighbors=3,
    leaf_size=30,
    metric='minkowski',
    p=2,
    weights='uniform',
    test_size=0.3,
    random_state=1012,
    model_path=None,
):
    iris = load_iris()
    X = iris.data
    y = iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    classifier = KNeighborsClassifier(n_neighbors=n_neighbors, leaf_size=leaf_size, metric=metric, p=p, weights=weights)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    accuracy = metrics.accuracy_score(y_test, y_pred)
    recall = metrics.recall_score(y_test, y_pred, average='weighted')
    f1 = metrics.f1_score(y_pred, y_pred, average='weighted')
    results = {
        'accuracy': accuracy,
        'recall': recall,
        'f1': f1,
    }
    if model_path:
        joblib.dump(classifier, model_path)
    return results
