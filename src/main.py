from fastapi import FastAPI
import uvicorn
from src.endpoint.api import router as api_router


app = FastAPI()
app.include_router(api_router, prefix="/routeur")
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port="8000")