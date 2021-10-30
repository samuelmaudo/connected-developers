from fastapi import FastAPI

from api.routers import connected

app = FastAPI()
app.include_router(connected.router)
