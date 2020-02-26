import pandas as pd
import numpy as np

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
    
    return X, y
