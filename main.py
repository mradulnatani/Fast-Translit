from Backend.auth.router import router as auth_router
from fastapi import FastAPI
from Backend.gateway.router import router as gateway_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(gateway_router)


