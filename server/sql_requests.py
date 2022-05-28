from typing import List, Tuple

import pyodbc
from fastapi import HTTPException

from sql_utils import CONNSTRING, add_quotes, exists, is_referenced

def select_ids(table_name: str, field_name: str) -> List:
    """
    Returns IDs from a table
    """
    with pyodbc.connect(CONNSTRING) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT {field_name} FROM {table_name}")
        data = []
        for row in cursor:
            data.append(row[0])
    return data

def select_eq(table_name: str, field_name: str, field_val) -> List[Tuple]:
    """
    Returns records  where field_name equals field_val
    """
    with pyodbc.connect(CONNSTRING) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT * FROM {table_name} "
            f"WHERE {field_name} = {add_quotes(field_val)}"
        )
        data = []
        for row in cursor:
            data.append(row)
    return data

def delete(table_name: str, field_name: str, item_id: str) -> bool:
    item = select_eq(table_name, field_name, item_id)
    if not item:
        raise HTTPException(status_code=404,
                            detail=f"{item_id} not found.")

    if is_referenced(table_name, field_name, item_id):
        raise HTTPException(
            status_code=409,
            detail=f"{item_id} is being referenced by a foreign key."
        )

    with pyodbc.connect(CONNSTRING) as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name} WHERE"
                           f"{field_name} = {add_quotes(item_id)}")

    return item