import pandas as pd

from sklearn.feature_selection import SelectFromModel
from sklearn.base import TransformerMixin

class SelectFromModelPandas(TransformerMixin):

    def __init__(self, *args, **kwargs):
        self.sfm = SelectFromModel(*args, **kwargs)
    
    def transform(self, X):
        return pd.DataFrame(self.sfm.transform(X), columns=X.columns[self.sfm.get_support()])

    def fit(self, X, y=None):
        self.sfm.fit(X, y)
        return self

    def fit_transform(self, X, y):
        self.sfm.fit(X)
        return pd.DataFrame(self.sfm.transform(X), columns=X.columns[self.sfm.get_support()])
    
    def __repr__(self):
        return f'pandas.{self.sfm.__repr__}'
    
    def __str__(self):
        return f'pandas.{self.sfm.__str__}'
