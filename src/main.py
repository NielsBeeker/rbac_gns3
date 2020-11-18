from fastapi import FastAPI
import uvicorn
from endpoint.api import router as api_router


app = FastAPI()
app.include_router(api_router)
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port="8000")