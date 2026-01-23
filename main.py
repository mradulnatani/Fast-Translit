from fastapi import FastAPI
from Backend.auth.router import router as auth_router
from Backend.gateway.router import router as gateway_router

app = FastAPI(title="AI Transliteration Gateway")

app.include_router(auth_router)
app.include_router(gateway_router)

