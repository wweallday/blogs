from fastapi import FastAPI
from models import *
from routers import api
from sqlmodel import SQLModel

from core.database_session import _ASYNC_ENGINE
async def create_tables() -> None: 
    async with _ASYNC_ENGINE.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

app = FastAPI()  # This is the "app" that FastAPI expects

app.include_router(api.api_router)
app.add_event_handler("startup", create_tables)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

if __name__ == '__main__':

    import uvicorn 
    uvicorn.run("main:app", 
                host="0.0.0.0", 
                port=8002, 
                reload=True)