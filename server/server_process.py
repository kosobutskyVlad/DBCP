import multiprocessing

from fastapi import FastAPI, APIRouter
import uvicorn

from endpoints import (
    cities,
    storetypes,
    stores,
    products,
    parameters,
    purchases,
    stock
)

server_process = None

app = FastAPI()

app.include_router(cities.router)
app.include_router(storetypes.router)
app.include_router(stores.router)
app.include_router(products.router)
app.include_router(parameters.router)
app.include_router(purchases.router)
app.include_router(stock.router)

def start_server():
    global server_process
    server_process = multiprocessing.Process(
        target=uvicorn.run,
        args=("server_process:app",),
        kwargs={"host": "127.0.0.1", "port": 5000}
    )
    server_process.start()

def stop_server():
    if server_process is not None:
        server_process.terminate()