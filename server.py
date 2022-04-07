import multiprocessing
from typing import Optional

from fastapi import FastAPI, APIRouter
import pyodbc
import uvicorn

server_process = None

app = FastAPI()
router = APIRouter()

def start_server():
    global server_process
    server_process = multiprocessing.Process(
        target=uvicorn.run,
        args=("server:app",),
        kwargs={"host": "127.0.0.1", "port": 5001})
    server_process.start()

def stop_server():
    server_process.terminate()