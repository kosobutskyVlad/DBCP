from typing import List, Optional
from datetime import date

import pyodbc

CONNSTRING = ("Driver={SQL Server Native Client 11.0};"
              "Server=DESKTOP-P8N0IJI;"
              "Database=retail;"
              "Trusted_Connection=yes;")

def add_quotes(field_val):
    """
    Encloses string with single quotes if field_val is of str type
    """
    if isinstance(field_val, str):
        return f"'{field_val}'"
    if isinstance(field_val, date):
        return f"'{field_val.isoformat()}'"
    return str(field_val)

def get_where_clause(fields: Optional[List[str]] = None,
                     vals: Optional[List] = None) -> str:
    """Constructs WHERE clause with conjunction of equalities"""
    if fields is None or vals is None:
        return ""

    conditions = []
    for field, val in zip(fields, vals):
        if not val:
            continue
        conditions.append(f"{field} = {add_quotes(val)}")
    if conditions:
        return f" WHERE {' AND '.join(conditions)}"
    return ""
    

def exists(table_name: str, field_names: List[str],
           field_vals: List) -> bool:
    """
    Returns True if there is a record in a table where field_name
    equals field_val
    """
    with pyodbc.connect(CONNSTRING) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                f"SELECT COUNT(1) FROM {table_name}"
                f"{get_where_clause(field_names, field_vals)}"
            )
            data = []
            for row in cursor:
                data.append(row[0])
    return bool(data[0])

def is_referenced(table_name: str, field_names: List[str],
                  field_vals: List) -> bool:
    """
    Returns True if the record with field_name equals to field_val is
    being referenced by a foreign key
    """
    with pyodbc.connect(CONNSTRING) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"DELETE FROM {table_name}"
                f"{get_where_clause(field_names, field_vals)}"
            )
        except pyodbc.IntegrityError:
            return True
        return False