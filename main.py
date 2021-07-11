from fastapi import FastAPI
import uvicorn
from settings import config
from app import create_app


def run(app: FastAPI):
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT)


if __name__ == "__main__":
    run(create_app())
