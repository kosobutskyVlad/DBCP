import pandas as pd

def ffill_history(response):
    purchase_history = response.json()["purchases"]
    dataframe = pd.DataFrame(
        purchase_history,
        columns=[
            "id", "store_id", "product_id", "purchase_date",
            "price", "sales", "discount", "revenue"
        ]
    )
    dataframe = dataframe.loc[:, ["purchase_date","sales"]]
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
    ).drop([0], axis=1)
    return full_history.fillna(method='ffill')

def aggregate_history(history):
    zero_values_count = (history["purchase_date"] == 0).sum()
    zv_ratio = zero_values_count / len(history.index)
    if zv_ratio > 0.96:
        return history.resample('M', on="purchase_date").sum()
    if zv_ratio > 0.8:
        return history.resample('2W', on="purchase_date").sum()
    if zv_ratio > 0.6:
        return history.resample('W', on="purchase_date").sum()
    if zv_ratio > 0.2:
        return history.resample('3D', on="purchase_date").sum()
    return history