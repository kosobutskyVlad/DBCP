from fastapi import APIRouter
from typing import Optional
import pyodbc

router = APIRouter(
    prefix="/cities",
    tags=["City"],
    responses={404: {"description": "Not found"}},
)

@router.post("/add-loss-parameters")
def add_loss_parameters(product_id: str, store_id: str,
                        loyalty_charge_x: Optional[float], loyalty_charge_coef: Optional[float],
                        storage_cost_coef: Optional[float], bank_rate_x: Optional[float],
                        bank_rate_coef: Optional[float], product_cost_x: Optional[float],
                        product_cost_coef: Optional[float]):
    pass

@router.get("/get-loss-parameters")
def get_loss_parameters(product_id: str, store_id: str):
    pass

@router.get("/get-product-store-history")
def get_product_store_history(product_id: str, store_id: str):
    pass

@router.get("get-item")
def get_item(table: str, item_id: str):
    pass

@router.get("/get-city")
def get_cities(city_id: Optional[str] = None):
    data = []

    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-P8N0IJI;"
        "Database=retail;"
        "Trusted_Connection=yes;"
    )

    where_clause = ""
    if city_id:
        where_clause = f"WHERE city_id = '{city_id}'"

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Cities {where_clause}")
    for row in cursor:
        data.append(list(row))
    conn.close()

    return {"Data": data}