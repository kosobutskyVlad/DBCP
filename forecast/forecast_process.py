import multiprocessing

from fastapi import FastAPI, APIRouter
import uvicorn

from endpoints import predict

forecast_process = None

app = FastAPI()
router = APIRouter()
app.include_router(predict.router)

def start_forecast():
    global forecast_process
    forecast_process = multiprocessing.Process(
        target=uvicorn.run,
        args=("forecast_process:app",),
        kwargs={"host": "127.0.0.1", "port": 5001}
    )
    forecast_process.start()

def stop_forecast():
    if forecast_process is not None:
        forecast_process.terminate()