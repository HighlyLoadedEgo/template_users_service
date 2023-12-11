import uvicorn
from fastapi import FastAPI

from src.auth.routers import test_r
from src.config import Settings
from src.utils.config_loader import load_config

a = load_config(Settings)
app = FastAPI()
app.include_router(test_r)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
