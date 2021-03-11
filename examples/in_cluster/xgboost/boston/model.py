import argparse
import logging

import pandas as pd
import xgboost as xgb

# Polyaxon
from polyaxon import tracking
from polyaxon.tracking.contrib.xgboost import polyaxon_callback

from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split

logger = logging.getLogger()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--max_depth',
        type=int,
        default=5
    )
    parser.add_argument(
        '--eta',
        type=float,
        default=0.5
    )
    parser.add_argument(
        '--gamma',
        type=float,
        default=0.1
    )
    parser.add_argument(
        '--subsample',
        type=int,
        default=1
    )
    parser.add_argument(
        '--lambda',
        type=int,
        default=1,
        dest='lambda_',
    )
    parser.add_argument(
        '--alpha',
        type=float,
        default=0.35
    )
    parser.add_argument(
        '--objective',
        type=str,
        default='reg:squarederror'
    )
    parser.add_argument(
        '--cross_validate',
        type=bool,
        default=False
    )

    args = parser.parse_args()

    params = {
        'max_depth': args.max_depth,
        'eta': args.eta,
        'gamma': args.gamma,
        'subsample': args.subsample,
        'lambda': args.lambda_,
        'alpha': args.alpha,
        'objective': args.objective,
        'eval_metric': ['mae', 'rmse']
    }

    # Polyaxon
    tracking.init()

    boston = load_boston()
    data = pd.DataFrame(boston.data)
    data.columns = boston.feature_names
    data['PRICE'] = boston.target
    X, y = data.iloc[:, :-1], data.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1012)

    # Polyaxon
    tracking.log_data_ref(content=X_train, name='x_train')
    tracking.log_data_ref(content=y_train, name='y_train')
    tracking.log_data_ref(content=X_test, name='X_test')
    tracking.log_data_ref(content=y_test, name='y_train')

    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)

    if args.cross_validate:
        xgb.cv(params, dtrain, num_boost_round=20, nfold=7, callbacks=[polyaxon_callback()])
    else:
        xgb.train(
            params,
            dtrain,
            20,
            [(dtest, 'eval'), (dtrain, 'train')],
            callbacks=[polyaxon_callback()]  # Polyaxon
        )

