from typing import Tuple
from requests.models import Response

import pandas as pd
import numpy as np

FEATURE_COUNT = {
    "3D": 12,
    "W": 10,
    "2W": 8,
    "M": 7
}

def ffill_history(response: Response) -> pd.DataFrame:
    """
    Adds missing days to the dataframe and forward fills them
    """
    purchase_history = response.json()
    dataframe = pd.DataFrame(
        purchase_history,
        columns=[
            "id", "store_id", "product_id", "purchase_date",
            "price", "sales", "discount", "revenue"
        ]
    )
    dataframe = dataframe.loc[:, ["purchase_date", "sales"]]
    dataframe = dataframe.sort_values("purchase_date")
    dataframe["purchase_date"] = pd.to_datetime(
        dataframe["purchase_date"]
    )
    
    date_range = pd.DataFrame(pd.date_range(
        dataframe["purchase_date"].min(),
        dataframe["purchase_date"].max(),
        freq='1D'
        ))

    full_history = date_range.merge(
        dataframe, "left",
        left_on=0, right_on="purchase_date"
    ).drop(["purchase_date"], axis=1)

    full_history = full_history.rename(columns={0: "purchase_date"})
    return full_history.fillna(method="ffill")

def aggregate_history(history: pd.DataFrame) -> pd.DataFrame:
    zero_values_count = (history["sales"] == 0).sum()
    zv_ratio = zero_values_count / len(history.index)
    if zv_ratio > 0.96:
        return history.resample('M', on="purchase_date").sum(), "M"
    if zv_ratio > 0.8:
        return history.resample('2W', on="purchase_date").sum(), "2W"
    if zv_ratio > 0.6:
        return history.resample('W', on="purchase_date").sum(), "W"
    return history.resample("3D", on="purchase_date").sum(), "3D"

def prepare_data(dataframe: pd.DataFrame,
                 aggr_window: str) -> Tuple[np.ndarray, np.ndarray]:
    y = dataframe.iloc[:, 0].values
    X = np.zeros((len(dataframe.index), FEATURE_COUNT[aggr_window]))

    for i in range(6):
        X[i+1:, i] = dataframe.iloc[:-i-1].values[:, 0]

    if aggr_window == "M":
        X[11:, 6] = dataframe.iloc[:-11].values[:, 0]

    if aggr_window == "2W":
        X[12:, 6] = dataframe.iloc[:-12].values[:, 0]
        X[26:, 7] = dataframe.iloc[:-26].values[:, 0]

    if aggr_window == "W":
        X[7:, 6] = dataframe.iloc[:-7].values[:, 0]
        X[12:, 7] = dataframe.iloc[:-12].values[:, 0]
        X[26:, 8] = dataframe.iloc[:-22].values[:, 0]
        X[52:, 9] = dataframe.iloc[:-52].values[:, 0]

    if aggr_window == "3D":
        X[7:, 6] = dataframe.iloc[:-7].values[:, 0]
        X[10:, 7] = dataframe.iloc[:-10].values[:, 0]
        X[20:, 8] = dataframe.iloc[:-20].values[:, 0]
        X[30:, 9] = dataframe.iloc[:-30].values[:, 0]
        X[61:, 7] = dataframe.iloc[:-61].values[:, 0]
        X[122:, 8] = dataframe.iloc[:-122].values[:, 0]

    return X, y