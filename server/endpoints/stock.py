from typing import List

import pyodbc
from pydantic import BaseModel, constr, conint
from fastapi import APIRouter, HTTPException

from sql_utils import exists
from sql_requests import select_ids, select_eq, insert, update, delete

TABLE_NAME = "Stock"
ID_NAME = "stock_id"

class Stock(BaseModel):
    store_id: constr(curtail_length=5)
    product_id: constr(curtail_length=5)
    stock: conint(ge=0) = 0

router = APIRouter(
    prefix="/stock",
    tags=["stock"],
    responses={404: {"description": "Not found"}})


@router.get("/get-stock")
def get_stock_by_store(store_id: str) -> List[List]:
    return select_eq(TABLE_NAME, "store_id", store_id)

@router.get("/get-stock/{stock_id}")
def get_stock_by_id(stock_id: int) -> List[List]:
    return select_eq(TABLE_NAME, ID_NAME, stock_id)

@router.post("/add-stock")
def add_stock(stock: Stock) -> dict:
    if not exists("Stores", "store_id", stock.store_id):
        raise HTTPException(
            status_code=422,
            detail=f"{stock.store_id} does not exist."
        )

    if not exists("Products", "product_id", stock.product_id):
        raise HTTPException(
            status_code=422,
            detail=f"{stock.product_id} does not exist."
        )

    return insert(TABLE_NAME, ID_NAME, stock)

@router.put("/update-stock")
def update_stock(stock_id: int, stock: Stock) -> dict:

    if not exists("Stores", "store_id", stock.store_id):
        raise HTTPException(
            status_code=422,
            detail=f"{stock.store_id} does not exist."
        )

    if not exists("Products", "product_id", stock.product_id):
        raise HTTPException(
            status_code=422,
            detail=f"{stock.product_id} does not exist."
        )

    return update(TABLE_NAME, ID_NAME, stock, stock_id)

@router.delete("/delete-stock/{stock_id}")
def delete_stock(stock_id: int) -> dict:
    return delete(TABLE_NAME, ID_NAME, stock_id)