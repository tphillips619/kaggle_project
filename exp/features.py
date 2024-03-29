import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.preprocessing import StandardScaler
from scipy.stats import pearsonr
import warnings
from scipy.signal import hilbert
from scipy.signal import hann
from scipy.signal import convolve
from scipy import stats
from tqdm import tqdm_notebook
import kaggle_files
import inspect
warnings.filterwarnings("ignore")


def load_cv_results(cv_results_file="exp3.csv"):
    files_dir = os.path.dirname(inspect.getfile(kaggle_files))
    cv_results_dir = os.path.join(files_dir, "cv_results")
    cv_results_file_path = os.path.join(cv_results_dir, cv_results_file)
    if os.path.exists(cv_results_file_path):
        return pd.read_csv(cv_results_file_path)
    else:
        raise ValueError("Result file doesn't exist")


def load_train_features(set="standard_scaled"):
    files_dir = os.path.dirname(inspect.getfile(kaggle_files))
    features_dir = os.path.join(files_dir, "features")
    # extract pearson correlation string stuff
    if "_pc_" in set:
        pc_str = set[set.index("_pc_"):]
        set = set[:set.index("_pc_")]
    else:
        pc_str=""
    if set == "standard":
        train_dir = os.path.join(features_dir, "train")
        X = pd.read_csv(os.path.join(train_dir, "standard_138"+pc_str+".csv"), index_col=0)
        y_tr = pd.read_csv(os.path.join(train_dir, "ttf.csv"), index_col=0)
        return X, y_tr
    elif set == "standard_scaled":
        train_dir = os.path.join(features_dir, "train")
        X = pd.read_csv(os.path.join(train_dir, "standard_138_scaled"+pc_str+".csv"), index_col=0)
        y_tr = pd.read_csv(os.path.join(train_dir, "ttf.csv"), index_col=0)
        return X, y_tr
    elif set == "routine":
        train_dir = os.path.join(features_dir, "train")
        X = pd.read_csv(os.path.join(train_dir, "X_fillna_4194rows_996cols"+pc_str+".csv"), index_col=0)
        y_tr = pd.read_csv(os.path.join(train_dir, "ttf.csv"), index_col=0)
        return X, y_tr
    elif set == "more_features":
        train_dir = os.path.join(features_dir, "train")
        X = pd.read_csv(os.path.join(train_dir, "X_fillna_4194rows_1328cols"+pc_str+".csv"), index_col=0)
        y_tr = pd.read_csv(os.path.join(train_dir, "ttf.csv"), index_col=0)
        return X, y_tr
    elif set == "more_features_lgb_eli_5":
        train_dir = os.path.join(features_dir, "train")
        X = pd.read_csv(os.path.join(train_dir, "X_fillna_4194rows_1328cols"+pc_str+"_lgb_eli5_5.csv"), index_col=0)
        y_tr = pd.read_csv(os.path.join(train_dir, "ttf.csv"), index_col=0)
        return X, y_tr
    elif set == "more_features_lgb_eli_10":
        train_dir = os.path.join(features_dir, "train")
        X = pd.read_csv(os.path.join(train_dir, "X_fillna_4194rows_1328cols"+pc_str+"_lgb_eli5_10.csv"), index_col=0)
        y_tr = pd.read_csv(os.path.join(train_dir, "ttf.csv"), index_col=0)
        return X, y_tr
    elif set == "more_features_lgb_eli_15":
        train_dir = os.path.join(features_dir, "train")
        X = pd.read_csv(os.path.join(train_dir, "X_fillna_4194rows_1328cols"+pc_str+"_lgb_eli5_15.csv"), index_col=0)
        y_tr = pd.read_csv(os.path.join(train_dir, "ttf.csv"), index_col=0)
        return X, y_tr
    elif set == "more_features_lgb_eli_20":
        train_dir = os.path.join(features_dir, "train")
        X = pd.read_csv(os.path.join(train_dir, "X_fillna_4194rows_1328cols"+pc_str+"_lgb_eli5_20.csv"), index_col=0)
        y_tr = pd.read_csv(os.path.join(train_dir, "ttf.csv"), index_col=0)
        return X, y_tr
    elif set == "more_features_lgb_eli_50":
        train_dir = os.path.join(features_dir, "train")
        X = pd.read_csv(os.path.join(train_dir, "X_fillna_4194rows_1328cols"+pc_str+"_lgb_eli5_50.csv"), index_col=0)
        y_tr = pd.read_csv(os.path.join(train_dir, "ttf.csv"), index_col=0)
        return X, y_tr
    elif set == "more_features_lgb_eli_100":
        train_dir = os.path.join(features_dir, "train")
        X = pd.read_csv(os.path.join(train_dir, "X_fillna_4194rows_1328cols"+pc_str+"_lgb_eli5_100.csv"), index_col=0)
        y_tr = pd.read_csv(os.path.join(train_dir, "ttf.csv"), index_col=0)
        return X, y_tr
    elif set == "more_features_lgb_eli_200":
        train_dir = os.path.join(features_dir, "train")
        X = pd.read_csv(os.path.join(train_dir, "X_fillna_4194rows_1328cols"+pc_str+"_lgb_eli5_200.csv"), index_col=0)
        y_tr = pd.read_csv(os.path.join(train_dir, "ttf.csv"), index_col=0)
        return X, y_tr
    elif set == "quakeEdgeSplit":
        train_dir = os.path.join(features_dir, "train")
        X = pd.read_csv(os.path.join(train_dir, "X_quakebased_fillna_4153rows_984cols"+pc_str+".csv"), index_col=0)
        y_tr = pd.read_csv(os.path.join(train_dir, "y_quakebasedFE_4153rows_984cols.csv"))
        return X, y_tr
    elif set == "24000":
        train_dir = os.path.join(features_dir, "train")
        X = pd.read_csv(os.path.join(train_dir, "ML5round1_scaled_train_X"+pc_str+".csv"), index_col=0)
        y_tr = pd.read_csv(os.path.join(train_dir, "ML5round1_train_y.csv"))
        return X, y_tr
    elif set == "24000_lgb_tree_5":
        train_dir = os.path.join(features_dir, "train")
        X = pd.read_csv(os.path.join(train_dir, "ML5round1_scaled_train_X_lgb_tree_5"+pc_str+".csv"), index_col=0)
        y_tr = pd.read_csv(os.path.join(train_dir, "ML5round1_train_y.csv"))
        return X, y_tr
    elif set == "24000_lgb_tree_10":
        train_dir = os.path.join(features_dir, "train")
        X = pd.read_csv(os.path.join(train_dir, "ML5round1_scaled_train_X_lgb_tree_10"+pc_str+".csv"), index_col=0)
        y_tr = pd.read_csv(os.path.join(train_dir, "ML5round1_train_y.csv"))
        return X, y_tr
    elif set == "24000_lgb_tree_15":
        train_dir = os.path.join(features_dir, "train")
        X = pd.read_csv(os.path.join(train_dir, "ML5round1_scaled_train_X_lgb_tree_15"+pc_str+".csv"), index_col=0)
        y_tr = pd.read_csv(os.path.join(train_dir, "ML5round1_train_y.csv"))
        return X, y_tr
    elif set == "24000_lgb_tree_20":
        train_dir = os.path.join(features_dir, "train")
        X = pd.read_csv(os.path.join(train_dir, "ML5round1_scaled_train_X_lgb_tree_20"+pc_str+".csv"), index_col=0)
        y_tr = pd.read_csv(os.path.join(train_dir, "ML5round1_train_y.csv"))
        return X, y_tr
    elif set == "24000_lgb_tree_50":
        train_dir = os.path.join(features_dir, "train")
        X = pd.read_csv(os.path.join(train_dir, "ML5round1_scaled_train_X_lgb_tree_50"+pc_str+".csv"), index_col=0)
        y_tr = pd.read_csv(os.path.join(train_dir, "ML5round1_train_y.csv"))
        return X, y_tr
    elif set == "24000_lgb_tree_100":
        train_dir = os.path.join(features_dir, "train")
        X = pd.read_csv(os.path.join(train_dir, "ML5round1_scaled_train_X_lgb_tree_100"+pc_str+".csv"), index_col=0)
        y_tr = pd.read_csv(os.path.join(train_dir, "ML5round1_train_y.csv"))
        return X, y_tr
    elif set == "24000_lgb_tree_200":
        train_dir = os.path.join(features_dir, "train")
        X = pd.read_csv(os.path.join(train_dir, "ML5round1_scaled_train_X_lgb_tree_200"+pc_str+".csv"), index_col=0)
        y_tr = pd.read_csv(os.path.join(train_dir, "ML5round1_train_y.csv"))
        return X, y_tr
    elif set == "24000_lgb_tree_300":
        train_dir = os.path.join(features_dir, "train")
        X = pd.read_csv(os.path.join(train_dir, "ML5round1_scaled_train_X_lgb_tree_300"+pc_str+".csv"), index_col=0)
        y_tr = pd.read_csv(os.path.join(train_dir, "ML5round1_train_y.csv"))
        return X, y_tr
    elif set == "24000_lgb_tree_400":
        train_dir = os.path.join(features_dir, "train")
        X = pd.read_csv(os.path.join(train_dir, "ML5round1_scaled_train_X_lgb_tree_400"+pc_str+".csv"), index_col=0)
        y_tr = pd.read_csv(os.path.join(train_dir, "ML5round1_train_y.csv"))
        return X, y_tr
    elif set == "24000_lgb_tree_500":
        train_dir = os.path.join(features_dir, "train")
        X = pd.read_csv(os.path.join(train_dir, "ML5round1_scaled_train_X_lgb_tree_500"+pc_str+".csv"), index_col=0)
        y_tr = pd.read_csv(os.path.join(train_dir, "ML5round1_train_y.csv"))
        return X, y_tr
    else:
        raise ValueError("Set type doesn't exist")


def load_test_features(set="standard_scaled", pc=None):
    files_dir = os.path.dirname(inspect.getfile(kaggle_files))
    features_dir = os.path.join(files_dir, "features")
    # extract pearson correlation string stuff
    if "_pc_" in set:
        pc_str = set[set.index("_pc_"):]
        set = set[:set.index("_pc_")]
    else:
        pc_str=""
    if set == "standard":
        test_dir = os.path.join(features_dir, "test")
        X = pd.read_csv(os.path.join(test_dir, "standard_138_test"+pc_str+".csv"), index_col=0)
        return X
    elif set == "standard_scaled":
        test_dir = os.path.join(features_dir, "test")
        X = pd.read_csv(os.path.join(test_dir, "standard_138_scaled_test"+pc_str+".csv"), index_col=0)
        return X
    elif set == "routine":
        test_dir = os.path.join(features_dir, "test")
        X = pd.read_csv(os.path.join(test_dir, "Xtest_fillna_2624rows_996cols"+pc_str+".csv"), index_col=0)
        return X
    elif set == "more_features":
        test_dir = os.path.join(features_dir, "test")
        X = pd.read_csv(os.path.join(test_dir, "Xtest_fillna_2624rows_1328cols"+pc_str+".csv"), index_col=0)
        return X
    elif set == "more_features_lgb_eli_5":
        test_dir = os.path.join(features_dir, "test")
        X = pd.read_csv(os.path.join(test_dir, "Xtest_fillna_2624rows_1328cols"+pc_str+"_lgb_eli5_5.csv"), index_col=0)
        return X
    elif set == "more_features_lgb_eli_10":
        test_dir = os.path.join(features_dir, "test")
        X = pd.read_csv(os.path.join(test_dir, "Xtest_fillna_2624rows_1328cols"+pc_str+"_lgb_eli5_10.csv"), index_col=0)
        return X
    elif set == "more_features_lgb_eli_15":
        test_dir = os.path.join(features_dir, "test")
        X = pd.read_csv(os.path.join(test_dir, "Xtest_fillna_2624rows_1328cols"+pc_str+"_lgb_eli5_15.csv"), index_col=0)
        return X
    elif set == "more_features_lgb_eli_20":
        test_dir = os.path.join(features_dir, "test")
        X = pd.read_csv(os.path.join(test_dir, "Xtest_fillna_2624rows_1328cols"+pc_str+"_lgb_eli5_20.csv"), index_col=0)
        return X
    elif set == "more_features_lgb_eli_50":
        test_dir = os.path.join(features_dir, "test")
        X = pd.read_csv(os.path.join(test_dir, "Xtest_fillna_2624rows_1328cols"+pc_str+"_lgb_eli5_50.csv"), index_col=0)
        return X
    elif set == "more_features_lgb_eli_100":
        test_dir = os.path.join(features_dir, "test")
        X = pd.read_csv(os.path.join(test_dir, "Xtest_fillna_2624rows_1328cols"+pc_str+"_lgb_eli5_100.csv"), index_col=0)
        return X
    elif set == "more_features_lgb_eli_200":
        test_dir = os.path.join(features_dir, "test")
        X = pd.read_csv(os.path.join(test_dir, "Xtest_fillna_2624rows_1328cols"+pc_str+"_lgb_eli5_200.csv"), index_col=0)
        return X
    elif set == "more_features_lgb_eli_300":
        test_dir = os.path.join(features_dir, "test")
        X = pd.read_csv(os.path.join(test_dir, "Xtest_fillna_2624rows_1328cols"+pc_str+"_lgb_eli5_300.csv"), index_col=0)
        return X
    elif set == "more_features_lgb_eli_400":
        test_dir = os.path.join(features_dir, "test")
        X = pd.read_csv(os.path.join(test_dir, "Xtest_fillna_2624rows_1328cols"+pc_str+"_lgb_eli5_400.csv"), index_col=0)
        return X
    elif set == "more_features_lgb_eli_500":
        test_dir = os.path.join(features_dir, "test")
        X = pd.read_csv(os.path.join(test_dir, "Xtest_fillna_2624rows_1328cols"+pc_str+"_lgb_eli5_500.csv"), index_col=0)
        return X
    elif set == "quakeEdgeSplit":
        test_dir = os.path.join(features_dir, "test")
        X = pd.read_csv(os.path.join(test_dir, "Xtest_quakebased_fillna_2624rows_984cols"+pc_str+".csv"), index_col=0)
        return X
    elif set == "24000":
        test_dir = os.path.join(features_dir, "test")
        X = pd.read_csv(os.path.join(test_dir, "ML5round1_scaled_test_X"+pc_str+".csv"), index_col=0)
        return X
    elif set == "24000_lgb_tree_5":
        test_dir = os.path.join(features_dir, "test")
        X = pd.read_csv(os.path.join(test_dir, "ML5round1_scaled_test_X_lgb_tree_5"+pc_str+".csv"), index_col=0)
        return X, y_tr
    elif set == "24000_lgb_tree_10":
        test_dir = os.path.join(features_dir, "test")
        X = pd.read_csv(os.path.join(test_dir, "ML5round1_scaled_test_X_lgb_tree_10"+pc_str+".csv"), index_col=0)
        return X, y_tr
    elif set == "24000_lgb_tree_15":
        test_dir = os.path.join(features_dir, "test")
        X = pd.read_csv(os.path.join(test_dir, "ML5round1_scaled_test_X_lgb_tree_15"+pc_str+".csv"), index_col=0)
        return X, y_tr
    elif set == "24000_lgb_tree_20":
        test_dir = os.path.join(features_dir, "test")
        X = pd.read_csv(os.path.join(test_dir, "ML5round1_scaled_test_X_lgb_tree_20"+pc_str+".csv"), index_col=0)
        return X
    elif set == "24000_lgb_tree_50":
        test_dir = os.path.join(features_dir, "test")
        X = pd.read_csv(os.path.join(test_dir, "ML5round1_scaled_test_X_lgb_tree_50"+pc_str+".csv"), index_col=0)
        return X
    elif set == "24000_lgb_tree_100":
        test_dir = os.path.join(features_dir, "test")
        X = pd.read_csv(os.path.join(test_dir, "ML5round1_scaled_test_X_lgb_tree_100"+pc_str+".csv"), index_col=0)
        return X
    elif set == "24000_lgb_tree_200":
        test_dir = os.path.join(features_dir, "test")
        X = pd.read_csv(os.path.join(test_dir, "ML5round1_scaled_test_X_lgb_tree_200"+pc_str+".csv"), index_col=0)
        return X
    else:
        raise ValueError("Set type doesn't exist")


def feature_sel_pc(X_train, y_train, X_test, p_val=None, corr_thresh=None):
    pcol = []
    pcor = []
    pval = []

    y_train = y_train['time_to_failure'].values

    for col in X_train.columns:
        pcol.append(col)
        pcor.append(abs(pearsonr(X_train[col], y_train)[0]))
        pval.append(abs(pearsonr(X_train[col], y_train)[1]))

    df = pd.DataFrame(data={'col': pcol, 'cor': pcor, 'pval': pval}, index=range(len(pcol)))
    df.sort_values(by=['cor', 'pval'], inplace=True)
    df.dropna(inplace=True)
    if p_val:
        df = df.loc[df['pval'] <= p_val]
    elif corr_thresh:
        df = df.loc[df['cor'] >= corr_thresh]

    drop_cols = []

    for col in X_train.columns:
        if col not in df['col'].tolist():
            drop_cols.append(col)

    X_train.drop(labels=drop_cols, axis=1, inplace=True)
    X_test.drop(labels=drop_cols, axis=1, inplace=True)
    return X_train, X_test


def add_trend_feature(arr, abs_values=False):
    idx = np.array(range(len(arr)))
    if abs_values:
        arr = np.abs(arr)
    lr = LinearRegression()
    lr.fit(idx.reshape(-1, 1), arr)
    return lr.coef_[0]

def classic_sta_lta(x, length_sta, length_lta):
    sta = np.cumsum(x ** 2)

    # Convert to float
    sta = np.require(sta, dtype=np.float)

    # Copy for LTA
    lta = sta.copy()

    # Compute the STA and the LTA
    sta[length_sta:] = sta[length_sta:] - sta[:-length_sta]
    sta /= length_sta
    lta[length_lta:] = lta[length_lta:] - lta[:-length_lta]
    lta /= length_lta

    # Pad zeros
    sta[:length_lta - 1] = 0

    # Avoid division by zero by setting zero values to tiny float
    dtiny = np.finfo(0.0).tiny
    idx = lta < dtiny
    lta[idx] = dtiny

    return sta / lta


def create_train_features(train_file="train.csv"):
    train = pd.read_csv(train_file, dtype={'acoustic_data': np.int16, 'time_to_failure': np.float32})
    rows = 150000
    segments = int(np.floor(train.shape[0] / rows))

    X_tr = pd.DataFrame(index=range(segments), dtype=np.float64)
    y_tr = pd.DataFrame(index=range(segments), dtype=np.float64, columns=['time_to_failure'])

    for segment in tqdm_notebook(range(segments)):
        seg = train.iloc[segment * rows:segment * rows + rows]
        x = pd.Series(seg['acoustic_data'].values)
        y = seg['time_to_failure'].values[-1]

        y_tr.loc[segment, 'time_to_failure'] = y
        X_tr.loc[segment, 'mean'] = x.mean()
        X_tr.loc[segment, 'std'] = x.std()
        X_tr.loc[segment, 'max'] = x.max()
        X_tr.loc[segment, 'min'] = x.min()

        X_tr.loc[segment, 'mean_change_abs'] = np.mean(np.diff(x))
        X_tr.loc[segment, 'mean_change_rate'] = np.mean(np.nonzero((np.diff(x) / x[:-1]))[0])
        X_tr.loc[segment, 'abs_max'] = np.abs(x).max()
        X_tr.loc[segment, 'abs_min'] = np.abs(x).min()

        X_tr.loc[segment, 'std_first_50000'] = x[:50000].std()
        X_tr.loc[segment, 'std_last_50000'] = x[-50000:].std()
        X_tr.loc[segment, 'std_first_10000'] = x[:10000].std()
        X_tr.loc[segment, 'std_last_10000'] = x[-10000:].std()

        X_tr.loc[segment, 'avg_first_50000'] = x[:50000].mean()
        X_tr.loc[segment, 'avg_last_50000'] = x[-50000:].mean()
        X_tr.loc[segment, 'avg_first_10000'] = x[:10000].mean()
        X_tr.loc[segment, 'avg_last_10000'] = x[-10000:].mean()

        X_tr.loc[segment, 'min_first_50000'] = x[:50000].min()
        X_tr.loc[segment, 'min_last_50000'] = x[-50000:].min()
        X_tr.loc[segment, 'min_first_10000'] = x[:10000].min()
        X_tr.loc[segment, 'min_last_10000'] = x[-10000:].min()

        X_tr.loc[segment, 'max_first_50000'] = x[:50000].max()
        X_tr.loc[segment, 'max_last_50000'] = x[-50000:].max()
        X_tr.loc[segment, 'max_first_10000'] = x[:10000].max()
        X_tr.loc[segment, 'max_last_10000'] = x[-10000:].max()

        X_tr.loc[segment, 'max_to_min'] = x.max() / np.abs(x.min())
        X_tr.loc[segment, 'max_to_min_diff'] = x.max() - np.abs(x.min())
        X_tr.loc[segment, 'count_big'] = len(x[np.abs(x) > 500])
        X_tr.loc[segment, 'sum'] = x.sum()

        X_tr.loc[segment, 'mean_change_rate_first_50000'] = np.mean(
            np.nonzero((np.diff(x[:50000]) / x[:50000][:-1]))[0])
        X_tr.loc[segment, 'mean_change_rate_last_50000'] = np.mean(
            np.nonzero((np.diff(x[-50000:]) / x[-50000:][:-1]))[0])
        X_tr.loc[segment, 'mean_change_rate_first_10000'] = np.mean(
            np.nonzero((np.diff(x[:10000]) / x[:10000][:-1]))[0])
        X_tr.loc[segment, 'mean_change_rate_last_10000'] = np.mean(
            np.nonzero((np.diff(x[-10000:]) / x[-10000:][:-1]))[0])

        X_tr.loc[segment, 'q95'] = np.quantile(x, 0.95)
        X_tr.loc[segment, 'q99'] = np.quantile(x, 0.99)
        X_tr.loc[segment, 'q05'] = np.quantile(x, 0.05)
        X_tr.loc[segment, 'q01'] = np.quantile(x, 0.01)

        X_tr.loc[segment, 'abs_q95'] = np.quantile(np.abs(x), 0.95)
        X_tr.loc[segment, 'abs_q99'] = np.quantile(np.abs(x), 0.99)
        X_tr.loc[segment, 'abs_q05'] = np.quantile(np.abs(x), 0.05)
        X_tr.loc[segment, 'abs_q01'] = np.quantile(np.abs(x), 0.01)

        X_tr.loc[segment, 'trend'] = add_trend_feature(x)
        X_tr.loc[segment, 'abs_trend'] = add_trend_feature(x, abs_values=True)
        X_tr.loc[segment, 'abs_mean'] = np.abs(x).mean()
        X_tr.loc[segment, 'abs_std'] = np.abs(x).std()

        X_tr.loc[segment, 'mad'] = x.mad()
        X_tr.loc[segment, 'kurt'] = x.kurtosis()
        X_tr.loc[segment, 'skew'] = x.skew()
        X_tr.loc[segment, 'med'] = x.median()

        X_tr.loc[segment, 'Hilbert_mean'] = np.abs(hilbert(x)).mean()
        X_tr.loc[segment, 'Hann_window_mean'] = (convolve(x, hann(150), mode='same') / sum(hann(150))).mean()
        X_tr.loc[segment, 'classic_sta_lta1_mean'] = classic_sta_lta(x, 500, 10000).mean()
        X_tr.loc[segment, 'classic_sta_lta2_mean'] = classic_sta_lta(x, 5000, 100000).mean()
        X_tr.loc[segment, 'classic_sta_lta3_mean'] = classic_sta_lta(x, 3333, 6666).mean()
        X_tr.loc[segment, 'classic_sta_lta4_mean'] = classic_sta_lta(x, 10000, 25000).mean()
        X_tr.loc[segment, 'classic_sta_lta5_mean'] = classic_sta_lta(x, 50, 1000).mean()
        X_tr.loc[segment, 'classic_sta_lta6_mean'] = classic_sta_lta(x, 100, 5000).mean()
        X_tr.loc[segment, 'classic_sta_lta7_mean'] = classic_sta_lta(x, 333, 666).mean()
        X_tr.loc[segment, 'classic_sta_lta8_mean'] = classic_sta_lta(x, 4000, 10000).mean()
        X_tr.loc[segment, 'Moving_average_700_mean'] = x.rolling(window=700).mean().mean(skipna=True)
        ewma = pd.Series.ewm
        X_tr.loc[segment, 'exp_Moving_average_300_mean'] = (ewma(x, span=300).mean()).mean(skipna=True)
        X_tr.loc[segment, 'exp_Moving_average_3000_mean'] = ewma(x, span=3000).mean().mean(skipna=True)
        X_tr.loc[segment, 'exp_Moving_average_30000_mean'] = ewma(x, span=6000).mean().mean(skipna=True)
        no_of_std = 3
        X_tr.loc[segment, 'MA_700MA_std_mean'] = x.rolling(window=700).std().mean()
        X_tr.loc[segment, 'MA_700MA_BB_high_mean'] = (
                    X_tr.loc[segment, 'Moving_average_700_mean'] + no_of_std * X_tr.loc[
                segment, 'MA_700MA_std_mean']).mean()
        X_tr.loc[segment, 'MA_700MA_BB_low_mean'] = (
                    X_tr.loc[segment, 'Moving_average_700_mean'] - no_of_std * X_tr.loc[
                segment, 'MA_700MA_std_mean']).mean()
        X_tr.loc[segment, 'MA_400MA_std_mean'] = x.rolling(window=400).std().mean()
        X_tr.loc[segment, 'MA_400MA_BB_high_mean'] = (
                    X_tr.loc[segment, 'Moving_average_700_mean'] + no_of_std * X_tr.loc[
                segment, 'MA_400MA_std_mean']).mean()
        X_tr.loc[segment, 'MA_400MA_BB_low_mean'] = (
                    X_tr.loc[segment, 'Moving_average_700_mean'] - no_of_std * X_tr.loc[
                segment, 'MA_400MA_std_mean']).mean()
        X_tr.loc[segment, 'MA_1000MA_std_mean'] = x.rolling(window=1000).std().mean()
        X_tr.drop('Moving_average_700_mean', axis=1, inplace=True)

        X_tr.loc[segment, 'iqr'] = np.subtract(*np.percentile(x, [75, 25]))
        X_tr.loc[segment, 'q999'] = np.quantile(x, 0.999)
        X_tr.loc[segment, 'q001'] = np.quantile(x, 0.001)
        X_tr.loc[segment, 'ave10'] = stats.trim_mean(x, 0.1)

        for windows in [10, 100, 1000]:
            x_roll_std = x.rolling(windows).std().dropna().values
            x_roll_mean = x.rolling(windows).mean().dropna().values

            X_tr.loc[segment, 'ave_roll_std_' + str(windows)] = x_roll_std.mean()
            X_tr.loc[segment, 'std_roll_std_' + str(windows)] = x_roll_std.std()
            X_tr.loc[segment, 'max_roll_std_' + str(windows)] = x_roll_std.max()
            X_tr.loc[segment, 'min_roll_std_' + str(windows)] = x_roll_std.min()
            X_tr.loc[segment, 'q01_roll_std_' + str(windows)] = np.quantile(x_roll_std, 0.01)
            X_tr.loc[segment, 'q05_roll_std_' + str(windows)] = np.quantile(x_roll_std, 0.05)
            X_tr.loc[segment, 'q95_roll_std_' + str(windows)] = np.quantile(x_roll_std, 0.95)
            X_tr.loc[segment, 'q99_roll_std_' + str(windows)] = np.quantile(x_roll_std, 0.99)
            X_tr.loc[segment, 'av_change_abs_roll_std_' + str(windows)] = np.mean(np.diff(x_roll_std))
            X_tr.loc[segment, 'av_change_rate_roll_std_' + str(windows)] = np.mean(
                np.nonzero((np.diff(x_roll_std) / x_roll_std[:-1]))[0])
            X_tr.loc[segment, 'abs_max_roll_std_' + str(windows)] = np.abs(x_roll_std).max()

            X_tr.loc[segment, 'ave_roll_mean_' + str(windows)] = x_roll_mean.mean()
            X_tr.loc[segment, 'std_roll_mean_' + str(windows)] = x_roll_mean.std()
            X_tr.loc[segment, 'max_roll_mean_' + str(windows)] = x_roll_mean.max()
            X_tr.loc[segment, 'min_roll_mean_' + str(windows)] = x_roll_mean.min()
            X_tr.loc[segment, 'q01_roll_mean_' + str(windows)] = np.quantile(x_roll_mean, 0.01)
            X_tr.loc[segment, 'q05_roll_mean_' + str(windows)] = np.quantile(x_roll_mean, 0.05)
            X_tr.loc[segment, 'q95_roll_mean_' + str(windows)] = np.quantile(x_roll_mean, 0.95)
            X_tr.loc[segment, 'q99_roll_mean_' + str(windows)] = np.quantile(x_roll_mean, 0.99)
            X_tr.loc[segment, 'av_change_abs_roll_mean_' + str(windows)] = np.mean(np.diff(x_roll_mean))
            X_tr.loc[segment, 'av_change_rate_roll_mean_' + str(windows)] = np.mean(
                np.nonzero((np.diff(x_roll_mean) / x_roll_mean[:-1]))[0])
            X_tr.loc[segment, 'abs_max_roll_mean_' + str(windows)] = np.abs(x_roll_mean).max()
    print(f'{X_tr.shape[0]} samples in new train data and {X_tr.shape[1]} columns.')

    # fillna in new columns
    classic_sta_lta5_mean_fill = X_tr.loc[X_tr['classic_sta_lta5_mean'] != -np.inf, 'classic_sta_lta5_mean'].mean()
    X_tr.loc[X_tr['classic_sta_lta5_mean'] == -np.inf, 'classic_sta_lta5_mean'] = classic_sta_lta5_mean_fill
    X_tr['classic_sta_lta5_mean'] = X_tr['classic_sta_lta5_mean'].fillna(classic_sta_lta5_mean_fill)
    classic_sta_lta7_mean_fill = X_tr.loc[X_tr['classic_sta_lta7_mean'] != -np.inf, 'classic_sta_lta7_mean'].mean()
    X_tr.loc[X_tr['classic_sta_lta7_mean'] == -np.inf, 'classic_sta_lta7_mean'] = classic_sta_lta7_mean_fill
    X_tr['classic_sta_lta7_mean'] = X_tr['classic_sta_lta7_mean'].fillna(classic_sta_lta7_mean_fill)

    # scale feature vector
    scaler = StandardScaler()
    scaler.fit(X_tr)
    X_train_scaled = pd.DataFrame(scaler.transform(X_tr), columns=X_tr.columns)

    return X_tr, X_train_scaled, y_tr, scaler, classic_sta_lta5_mean_fill, classic_sta_lta7_mean_fill


def create_test_features(scaler=None, test_dir="test", submission_file="sample_submission.csv",
                         classic_sta_lta5_mean_fill=0, classic_sta_lta7_mean_fill=0):
    # read test data
    submission = pd.read_csv(submission_file, index_col='seg_id')
    X_test = pd.DataFrame(dtype=np.float64, index=submission.index)
    plt.figure(figsize=(22, 16))

    for i, seg_id in enumerate(tqdm_notebook(X_test.index)):
        seg = pd.read_csv(os.path.join(test_dir,seg_id + '.csv'))
        x = pd.Series(seg['acoustic_data'].values)
        X_test.loc[seg_id, 'mean'] = x.mean()
        X_test.loc[seg_id, 'std'] = x.std()
        X_test.loc[seg_id, 'max'] = x.max()
        X_test.loc[seg_id, 'min'] = x.min()

        X_test.loc[seg_id, 'mean_change_abs'] = np.mean(np.diff(x))
        X_test.loc[seg_id, 'mean_change_rate'] = np.mean(np.nonzero((np.diff(x) / x[:-1]))[0])
        X_test.loc[seg_id, 'abs_max'] = np.abs(x).max()
        X_test.loc[seg_id, 'abs_min'] = np.abs(x).min()

        X_test.loc[seg_id, 'std_first_50000'] = x[:50000].std()
        X_test.loc[seg_id, 'std_last_50000'] = x[-50000:].std()
        X_test.loc[seg_id, 'std_first_10000'] = x[:10000].std()
        X_test.loc[seg_id, 'std_last_10000'] = x[-10000:].std()

        X_test.loc[seg_id, 'avg_first_50000'] = x[:50000].mean()
        X_test.loc[seg_id, 'avg_last_50000'] = x[-50000:].mean()
        X_test.loc[seg_id, 'avg_first_10000'] = x[:10000].mean()
        X_test.loc[seg_id, 'avg_last_10000'] = x[-10000:].mean()

        X_test.loc[seg_id, 'min_first_50000'] = x[:50000].min()
        X_test.loc[seg_id, 'min_last_50000'] = x[-50000:].min()
        X_test.loc[seg_id, 'min_first_10000'] = x[:10000].min()
        X_test.loc[seg_id, 'min_last_10000'] = x[-10000:].min()

        X_test.loc[seg_id, 'max_first_50000'] = x[:50000].max()
        X_test.loc[seg_id, 'max_last_50000'] = x[-50000:].max()
        X_test.loc[seg_id, 'max_first_10000'] = x[:10000].max()
        X_test.loc[seg_id, 'max_last_10000'] = x[-10000:].max()

        X_test.loc[seg_id, 'max_to_min'] = x.max() / np.abs(x.min())
        X_test.loc[seg_id, 'max_to_min_diff'] = x.max() - np.abs(x.min())
        X_test.loc[seg_id, 'count_big'] = len(x[np.abs(x) > 500])
        X_test.loc[seg_id, 'sum'] = x.sum()

        X_test.loc[seg_id, 'mean_change_rate_first_50000'] = np.mean(
            np.nonzero((np.diff(x[:50000]) / x[:50000][:-1]))[0])
        X_test.loc[seg_id, 'mean_change_rate_last_50000'] = np.mean(
            np.nonzero((np.diff(x[-50000:]) / x[-50000:][:-1]))[0])
        X_test.loc[seg_id, 'mean_change_rate_first_10000'] = np.mean(
            np.nonzero((np.diff(x[:10000]) / x[:10000][:-1]))[0])
        X_test.loc[seg_id, 'mean_change_rate_last_10000'] = np.mean(
            np.nonzero((np.diff(x[-10000:]) / x[-10000:][:-1]))[0])

        X_test.loc[seg_id, 'q95'] = np.quantile(x, 0.95)
        X_test.loc[seg_id, 'q99'] = np.quantile(x, 0.99)
        X_test.loc[seg_id, 'q05'] = np.quantile(x, 0.05)
        X_test.loc[seg_id, 'q01'] = np.quantile(x, 0.01)

        X_test.loc[seg_id, 'abs_q95'] = np.quantile(np.abs(x), 0.95)
        X_test.loc[seg_id, 'abs_q99'] = np.quantile(np.abs(x), 0.99)
        X_test.loc[seg_id, 'abs_q05'] = np.quantile(np.abs(x), 0.05)
        X_test.loc[seg_id, 'abs_q01'] = np.quantile(np.abs(x), 0.01)

        X_test.loc[seg_id, 'trend'] = add_trend_feature(x)
        X_test.loc[seg_id, 'abs_trend'] = add_trend_feature(x, abs_values=True)
        X_test.loc[seg_id, 'abs_mean'] = np.abs(x).mean()
        X_test.loc[seg_id, 'abs_std'] = np.abs(x).std()

        X_test.loc[seg_id, 'mad'] = x.mad()
        X_test.loc[seg_id, 'kurt'] = x.kurtosis()
        X_test.loc[seg_id, 'skew'] = x.skew()
        X_test.loc[seg_id, 'med'] = x.median()

        X_test.loc[seg_id, 'Hilbert_mean'] = np.abs(hilbert(x)).mean()
        X_test.loc[seg_id, 'Hann_window_mean'] = (convolve(x, hann(150), mode='same') / sum(hann(150))).mean()
        X_test.loc[seg_id, 'classic_sta_lta1_mean'] = classic_sta_lta(x, 500, 10000).mean()
        X_test.loc[seg_id, 'classic_sta_lta2_mean'] = classic_sta_lta(x, 5000, 100000).mean()
        X_test.loc[seg_id, 'classic_sta_lta3_mean'] = classic_sta_lta(x, 3333, 6666).mean()
        X_test.loc[seg_id, 'classic_sta_lta4_mean'] = classic_sta_lta(x, 10000, 25000).mean()
        X_test.loc[seg_id, 'classic_sta_lta5_mean'] = classic_sta_lta(x, 50, 1000).mean()
        X_test.loc[seg_id, 'classic_sta_lta6_mean'] = classic_sta_lta(x, 100, 5000).mean()
        X_test.loc[seg_id, 'classic_sta_lta7_mean'] = classic_sta_lta(x, 333, 666).mean()
        X_test.loc[seg_id, 'classic_sta_lta8_mean'] = classic_sta_lta(x, 4000, 10000).mean()
        X_test.loc[seg_id, 'Moving_average_700_mean'] = x.rolling(window=700).mean().mean(skipna=True)
        ewma = pd.Series.ewm
        X_test.loc[seg_id, 'exp_Moving_average_300_mean'] = (ewma(x, span=300).mean()).mean(skipna=True)
        X_test.loc[seg_id, 'exp_Moving_average_3000_mean'] = ewma(x, span=3000).mean().mean(skipna=True)
        X_test.loc[seg_id, 'exp_Moving_average_30000_mean'] = ewma(x, span=6000).mean().mean(skipna=True)
        no_of_std = 3
        X_test.loc[seg_id, 'MA_700MA_std_mean'] = x.rolling(window=700).std().mean()
        X_test.loc[seg_id, 'MA_700MA_BB_high_mean'] = (
                    X_test.loc[seg_id, 'Moving_average_700_mean'] + no_of_std * X_test.loc[
                seg_id, 'MA_700MA_std_mean']).mean()
        X_test.loc[seg_id, 'MA_700MA_BB_low_mean'] = (
                    X_test.loc[seg_id, 'Moving_average_700_mean'] - no_of_std * X_test.loc[
                seg_id, 'MA_700MA_std_mean']).mean()
        X_test.loc[seg_id, 'MA_400MA_std_mean'] = x.rolling(window=400).std().mean()
        X_test.loc[seg_id, 'MA_400MA_BB_high_mean'] = (
                    X_test.loc[seg_id, 'Moving_average_700_mean'] + no_of_std * X_test.loc[
                seg_id, 'MA_400MA_std_mean']).mean()
        X_test.loc[seg_id, 'MA_400MA_BB_low_mean'] = (
                    X_test.loc[seg_id, 'Moving_average_700_mean'] - no_of_std * X_test.loc[
                seg_id, 'MA_400MA_std_mean']).mean()
        X_test.loc[seg_id, 'MA_1000MA_std_mean'] = x.rolling(window=1000).std().mean()
        X_test.drop('Moving_average_700_mean', axis=1, inplace=True)

        X_test.loc[seg_id, 'iqr'] = np.subtract(*np.percentile(x, [75, 25]))
        X_test.loc[seg_id, 'q999'] = np.quantile(x, 0.999)
        X_test.loc[seg_id, 'q001'] = np.quantile(x, 0.001)
        X_test.loc[seg_id, 'ave10'] = stats.trim_mean(x, 0.1)

        for windows in [10, 100, 1000]:
            x_roll_std = x.rolling(windows).std().dropna().values
            x_roll_mean = x.rolling(windows).mean().dropna().values

            X_test.loc[seg_id, 'ave_roll_std_' + str(windows)] = x_roll_std.mean()
            X_test.loc[seg_id, 'std_roll_std_' + str(windows)] = x_roll_std.std()
            X_test.loc[seg_id, 'max_roll_std_' + str(windows)] = x_roll_std.max()
            X_test.loc[seg_id, 'min_roll_std_' + str(windows)] = x_roll_std.min()
            X_test.loc[seg_id, 'q01_roll_std_' + str(windows)] = np.quantile(x_roll_std, 0.01)
            X_test.loc[seg_id, 'q05_roll_std_' + str(windows)] = np.quantile(x_roll_std, 0.05)
            X_test.loc[seg_id, 'q95_roll_std_' + str(windows)] = np.quantile(x_roll_std, 0.95)
            X_test.loc[seg_id, 'q99_roll_std_' + str(windows)] = np.quantile(x_roll_std, 0.99)
            X_test.loc[seg_id, 'av_change_abs_roll_std_' + str(windows)] = np.mean(np.diff(x_roll_std))
            X_test.loc[seg_id, 'av_change_rate_roll_std_' + str(windows)] = np.mean(
                np.nonzero((np.diff(x_roll_std) / x_roll_std[:-1]))[0])
            X_test.loc[seg_id, 'abs_max_roll_std_' + str(windows)] = np.abs(x_roll_std).max()

            X_test.loc[seg_id, 'ave_roll_mean_' + str(windows)] = x_roll_mean.mean()
            X_test.loc[seg_id, 'std_roll_mean_' + str(windows)] = x_roll_mean.std()
            X_test.loc[seg_id, 'max_roll_mean_' + str(windows)] = x_roll_mean.max()
            X_test.loc[seg_id, 'min_roll_mean_' + str(windows)] = x_roll_mean.min()
            X_test.loc[seg_id, 'q01_roll_mean_' + str(windows)] = np.quantile(x_roll_mean, 0.01)
            X_test.loc[seg_id, 'q05_roll_mean_' + str(windows)] = np.quantile(x_roll_mean, 0.05)
            X_test.loc[seg_id, 'q95_roll_mean_' + str(windows)] = np.quantile(x_roll_mean, 0.95)
            X_test.loc[seg_id, 'q99_roll_mean_' + str(windows)] = np.quantile(x_roll_mean, 0.99)
            X_test.loc[seg_id, 'av_change_abs_roll_mean_' + str(windows)] = np.mean(np.diff(x_roll_mean))
            X_test.loc[seg_id, 'av_change_rate_roll_mean_' + str(windows)] = np.mean(
                np.nonzero((np.diff(x_roll_mean) / x_roll_mean[:-1]))[0])
            X_test.loc[seg_id, 'abs_max_roll_mean_' + str(windows)] = np.abs(x_roll_mean).max()

    # fillna in new columns
    X_test.loc[X_test['classic_sta_lta5_mean'] == -np.inf, 'classic_sta_lta5_mean'] = classic_sta_lta5_mean_fill
    X_test.loc[X_test['classic_sta_lta7_mean'] == -np.inf, 'classic_sta_lta7_mean'] = classic_sta_lta7_mean_fill

    X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)
    return X_test, X_test_scaled
