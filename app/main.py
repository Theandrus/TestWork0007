from fastapi import FastAPI
from .database import Base, engine
from .routers import auth, tasks

Base.metadata.create_all(bind=engine)

app = FastAPI()
@app.get("/")
async def read_root():
    return {"message": "App is running"}
app.include_router(auth.router)
app.include_router(tasks.router)