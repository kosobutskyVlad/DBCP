import requests

from fastapi import APIRouter, HTTPException

from forecasting.data_prep_utils import ffill_history, aggregate_history
from forecasting.predict import predict

router = APIRouter(
    prefix="/predict",
    tags=["Predict"],
    responses={404: {"description": "Not found"}})

@router.get("")
def get_prediction(store_id: str, product_id: str,
                   host: str = "127.0.0.1", port: int = 5000):
    try:
        response_get_store = requests.get(
            f"http://{host}:{port}/stores/get-store/{store_id}"
        )

        if response_get_store.status_code != 200:
            raise HTTPException(
                status_code=404,
                detail=f"{store_id} not found."
            )

        response_get_product = requests.get(
            f"http://{host}:{port}/products/get-product/{product_id}"
        )

        if response_get_product.status_code != 200:
            raise HTTPException(
                status_code=404,
                detail=f"{product_id} not found."
            )

        response_get_purchases = requests.get(
            f"http://{host}:{port}/purchases/get-purchases",
            params={"store_id": store_id, "product_id": product_id}
        )

        if response_get_purchases.status_code == 200:
            purchases_dataframe, aggregation_window = aggregate_history(ffill_history(response_get_purchases))
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Purchases for {store_id} and {product_id} not found."
            )

        response_get_parameters = requests.get(
            f"http://{host}:{port}/parameters/get-parameters",
            params={"store_id": store_id, "product_id": product_id}
        )

        if response_get_parameters.status_code == 200:
            loss_parameters = response_get_parameters.json()["parameters"][0][3:]
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Parameters for {store_id} and {product_id} not found."
            )
    except requests.exceptions.ConnectionError:
         raise HTTPException(
                status_code=404,
                detail=f"Server at {host}:{port} is not available."
            )

    prediction_results = predict(
        purchases_dataframe, aggregation_window, loss_parameters
    )[-1]

    return prediction_results