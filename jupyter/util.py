import numpy as np
import pandas as pd


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

    @staticmethod
    def from_dict(dct):
        ad = AttrDict()
        for k in dct:
            ad[k] = dct[k]

        return ad


def split_data(df, sizes=None, shuffle=True, np_random=None):
    if sizes is None:
        sizes = [2, 2, 1]

    parts = sum(sizes)

    if shuffle:
        splits = np.array_split(df.sample(frac=1, random_state=np_random), parts)
    else:
        splits = np.array_split(df, parts)

    highs = prefix_sums(sizes)
    lows = [0] + highs[:-1]

    res = []
    for l, h in zip(lows, highs):
        tdf = pd.DataFrame(np.concatenate(splits[l:h]), columns=df.columns)
        res.append(tdf)

    return res


def prefix_sums(arr):
    res = arr[:]

    for i in range(1, len(arr)):
        res[i] = res[i - 1] + res[i]

    return res


def split_X_y(df, selected_label, all_labels):
    X = df.copy().drop(columns=all_labels)
    y = df.copy()[selected_label]

    return AttrDict.from_dict(
        {
            'X': X,
            'y': y
        }
    )


def split_X_y_all(train, test, validation, selected_label, all_labels):
    return AttrDict.from_dict(
        {
            'train': split_X_y(train, selected_label, all_labels),
            'test': split_X_y(test, selected_label, all_labels),
            'validation': split_X_y(validation, selected_label, all_labels)
        }
    )


def empty_features(df):
    return pd.DataFrame(index=df.index)


def column_feature(df, colname):
    return pd.DataFrame(df[colname], index=df.index, columns=[colname])


def str_contains(where, what, case=True):
    if case:
        return what in where
    else:
        return what.casefold() in where.casefold()
