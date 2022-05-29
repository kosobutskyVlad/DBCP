from datetime import date
from typing import Optional, List

from pydantic import BaseModel, constr, conint, confloat
from fastapi import APIRouter, HTTPException

from sql_utils import exists, get_where_clause
from sql_requests import select_eq, insert, update, delete

TABLE_NAME = "Purchases"
ID_FIELD = "purchase_id"

class Purchase(BaseModel):
    store_id: constr(curtail_length=5)
    product_id: constr(curtail_length=5)
    purchase_date: Optional[date] = None
    price: confloat(gt=0) = 0.01
    sales: conint(ge=0) = 0
    discount: confloat(ge=0) = 0
    revenue: confloat(ge=0) = 0

router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"],
    responses={404: {"description": "Not found"}})

@router.get("/get-purchases")
def get_purchases(store_id: str, product_id: str) -> List[List]:
    where_clause = get_where_clause(["store_id", "product_id"],
                                    [store_id, product_id])
    return select_eq(TABLE_NAME, where_clause=where_clause)

@router.get("/get-purchase")
def get_purchases(purchase_id: int) -> dict:
    where_clause = get_where_clause(["purchase_id"], [purchase_id])
    return select_eq(TABLE_NAME, where_clause=where_clause)

@router.post("/add-purchase")
def add_purchase(purchase: Purchase) -> dict:
    if not exists("Stores", ["store_id"], [purchase.store_id]):
        raise HTTPException(
            status_code=422,
            detail=f"{purchase.store_id} does not exist."
        )

    if not exists("Products", ["product_id"], [purchase.product_id]):
        raise HTTPException(
            status_code=422,
            detail=f"{purchase.product_id} does not exist."
        )

    return insert(TABLE_NAME, purchase)

@router.put("/update-purchase")
def update_purchase(purchase_id: int, purchase: Purchase) -> dict:

    if not exists("Stores", ["store_id"], [purchase.store_id]):
        raise HTTPException(
            status_code=422,
            detail=f"{purchase.store_id} does not exist."
        )

    if not exists("Products", ["product_id"], [purchase.product_id]):
        raise HTTPException(
            status_code=422,
            detail=f"{purchase.product_id} does not exist."
        )

    return update(TABLE_NAME, ID_FIELD, purchase, purchase_id)

@router.delete("/delete-purchase/{purchase_id}")
def delete_purchase(purchase_id: int):
    return delete(TABLE_NAME, ID_FIELD, purchase_id)