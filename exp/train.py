import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from sklearn.metrics import mean_absolute_error
import seaborn as sns
import warnings
from statsmodels import robust
from sklearn.model_selection import KFold
warnings.filterwarnings("ignore")

def train_get_test_preds(X, Y, X_test, params, model_cls, model_type='sklearn'):
    if model_type == 'sklearn':
        model = model_cls(**params)
        model.fit(X, Y)
        y_pred = model.predict(X_test)
    if model_type == 'lgb':
        model = model_cls(**params)
        model.fit(X, Y)
        y_pred = model.predict(X_test)
    if model_type == 'xgb':
        # add early stopping option
        train_data = model_cls.DMatrix(data=X, label=Y, feature_names=X.columns)
        if "num_boost_round" in params:
            num_boost_round = params.pop("num_boost_round")
            model = model_cls.train(dtrain=train_data, num_boost_round=num_boost_round, params=params)
        y_pred = model.predict(model_cls.DMatrix(X_test, feature_names=X.columns))
    if model_type == 'cat':
        model = model_cls(**params)
        model.fit(X, Y, cat_features=[], verbose=False)
        y_pred = model.predict(X_test)

    y_pred = y_pred.reshape(-1, )
    return model, y_pred


def train_model(X, Y, params, X_test=None, n_fold=10, model_type='sklearn', model_cls=None,
                plot_feature_importance=False):
    """Taken from the `Earthquakes FE. More features and samples` kaggle notebook"""
    if n_fold is None:
        return train_get_test_preds(X, Y, X_test, params, model_cls, model_type)

    oof = np.zeros(len(X))
    if X_test is not None:
        prediction = np.zeros(len(X_test))
    scores = []
    feature_importance = pd.DataFrame()

    folds = KFold(n_splits=n_fold, shuffle=True)
    for fold_n, (train_index, valid_index) in enumerate(folds.split(X)):
        print('Fold', fold_n, 'started at', time.ctime())
        X_train, X_valid = X.iloc[train_index], X.iloc[valid_index]
        y_train, y_valid = Y.iloc[train_index], Y.iloc[valid_index]

        if model_type == 'sklearn':
            model = model_cls(**params)
            model.fit(X_train, y_train)
            y_pred_valid = model.predict(X_valid)

            if X_test is not None:
                y_pred = model.predict(X_test)

        if model_type == 'lgb':
            # add early stopping option
            model = model_cls(**params)
            model.fit(X_train, y_train)
            y_pred_valid = model.predict(X_valid)

            if X_test is not None:
                y_pred = model.predict(X_test)

        if model_type == 'xgb':
            # add early stopping option
            train_data = model_cls.DMatrix(data=X_train, label=y_train, feature_names=X.columns)
            if "num_boost_round" in params:
                num_boost_round = params.pop("num_boost_round")
                model = model_cls.train(dtrain=train_data, num_boost_round=num_boost_round, params=params)
            y_pred_valid = model.predict(model_cls.DMatrix(X_valid, feature_names=X.columns))

            if X_test is not None:
                y_pred = model.predict(model_cls.DMatrix(X_test, feature_names=X.columns))

        if model_type == 'cat':
            model = model_cls(**params)
            model.fit(X_train, y_train, cat_features=[], verbose=False)
            y_pred_valid = model.predict(X_valid)

            if X_test is not None:
                y_pred = model.predict(X_test)

        y_pred_valid = y_pred_valid.reshape(-1, )
        oof[valid_index] = y_pred_valid
        score = mean_absolute_error(y_valid, y_pred_valid)
        scores.append(score)

        print(f'Fold {fold_n}. MAE: {score:.4f}.')
        print('')

        if X_test is not None:
            prediction += y_pred

        if model_type == 'lgb':
            # feature importance
            fold_importance = pd.DataFrame()
            fold_importance["feature"] = X.columns
            fold_importance["importance"] = model.feature_importances_
            fold_importance["fold"] = fold_n + 1
            feature_importance = pd.concat([feature_importance, fold_importance], axis=0)

    if X_test is not None:
        prediction /= n_fold

    print('CV mean score: {0:.4f}, mad: {1:.4f}.'.format(np.mean(scores), robust.mad(scores)))

    if model_type == 'lgb':
        feature_importance["importance"] /= n_fold
        if plot_feature_importance:
            cols = feature_importance[["feature", "importance"]].groupby("feature").mean().sort_values(
                by="importance", ascending=False)[:50].index

            best_features = feature_importance.loc[feature_importance.feature.isin(cols)]

            plt.figure(figsize=(16, 12));
            sns.barplot(x="importance", y="feature", data=best_features.sort_values(by="importance", ascending=False));
            plt.title('LGB Features (avg over folds)');

    if X_test is not None:
        return np.mean(scores), robust.mad(scores), prediction
    else:
        return np.mean(scores), robust.mad(scores)
