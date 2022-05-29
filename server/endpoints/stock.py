from typing import List

from pydantic import BaseModel, constr, conint
from fastapi import APIRouter, HTTPException

from sql_utils import exists, get_where_clause
from sql_requests import select_eq, insert, update, delete

TABLE_NAME = "Stock"
ID_FIELD = "stock_id"

class Stock(BaseModel):
    store_id: constr(curtail_length=5)
    product_id: constr(curtail_length=5)
    stock: conint(ge=0) = 0

router = APIRouter(
    prefix="/stock",
    tags=["Stock"],
    responses={404: {"description": "Not found"}})


@router.get("/get-stock")
def get_stock_by_store(store_id: str) -> List[List]:
    where_clause = get_where_clause(["store_id"], [store_id])
    return select_eq(TABLE_NAME, where_clause=where_clause)

@router.get("/get-stock/{stock_id}")
def get_stock_by_id(stock_id: int) -> List[List]:
    where_clause = get_where_clause([ID_FIELD], [stock_id])
    return select_eq(TABLE_NAME, where_clause=where_clause)

@router.post("/add-stock")
def add_stock(stock: Stock) -> dict:
    if not exists("Stores", ["store_id"], [stock.store_id]):
        raise HTTPException(
            status_code=422,
            detail=f"{stock.store_id} does not exist."
        )

    if not exists("Products", ["product_id"], [stock.product_id]):
        raise HTTPException(
            status_code=422,
            detail=f"{stock.product_id} does not exist."
        )

    where_clause = get_where_clause(
        ["store_id", "product_id"],
        [stock.store_id, stock.product_id]
    )
    if select_eq(TABLE_NAME, ["parameters_id"], where_clause) != [[]]:
        raise HTTPException(
            status_code=422,
            detail=(f"{stock.store_id} and {stock.product_id}"
                    "already exists.")
        )

    return insert(TABLE_NAME, stock)

@router.put("/update-stock")
def update_stock(stock_id: int, stock: Stock) -> dict:

    if not exists("Stores", ["store_id"], [stock.store_id]):
        raise HTTPException(
            status_code=422,
            detail=f"{stock.store_id} does not exist."
        )

    if not exists("Products", ["product_id"], [stock.product_id]):
        raise HTTPException(
            status_code=422,
            detail=f"{stock.product_id} does not exist."
        )

    return update(TABLE_NAME, ID_FIELD, stock, stock_id)

@router.delete("/delete-stock/{stock_id}")
def delete_stock(stock_id: int) -> dict:
    return delete(TABLE_NAME, ID_FIELD, stock_id)