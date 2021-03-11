import argparse
import logging

import lightgbm as lgb

# Polyaxon
from polyaxon import tracking
from polyaxon.tracking.contrib.lightgbm import polyaxon_callback

from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split

logger = logging.getLogger()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--boosting_type',
        type=str,
        default='gbdt'
    )
    parser.add_argument(
        '--objective',
        type=str,
        default='multiclass'
    )
    parser.add_argument(
        '--num_class',
        type=int,
        default=3
    )
    parser.add_argument(
        '--num_leaves',
        type=int,
        default=31
    )
    parser.add_argument(
        '--learning_rate',
        type=float,
        default=0.05,
    )
    parser.add_argument(
        '--feature_fraction',
        type=float,
        default=0.9
    )

    args = parser.parse_args()

    params = {
        'boosting_type': args.boosting_type,
        'objective': args.objective,
        'num_class': args.num_class,
        'num_leaves': args.num_leaves,
        'learning_rate': args.learning_rate,
        'feature_fraction': args.feature_fraction,
    }

    # Polyaxon
    tracking.init()

    data = load_wine()
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.1)

    # Polyaxon
    tracking.log_data_ref(content=X_train, name='x_train')
    tracking.log_data_ref(content=y_train, name='y_train')
    tracking.log_data_ref(content=X_test, name='X_test')
    tracking.log_data_ref(content=y_test, name='y_train')

    lgb_train = lgb.Dataset(X_train, y_train)
    lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)

    gbm = lgb.train(
        params,
        lgb_train,
        num_boost_round=500,
        valid_sets=[lgb_train, lgb_eval],
        valid_names=['train', 'valid'],
        callbacks=[polyaxon_callback()],  # Polyaxon
    )

    y_test_pred = gbm.predict(X_test)

    # Polyaxon
    tracking.log_sklearn_roc_auc_curve("roc_c", y_test_pred, y_test, is_multi_class=True)

    model_path = tracking.get_outputs_path("model/lightgbm.pkl")
    gbm.save_model(model_path)

    # Polyaxon
    tracking.log_model_ref(model_path, framework="lightgbm")
