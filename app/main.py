from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .database import engine, Base
from starlette.middleware.sessions import SessionMiddleware
from .routers import auth, dashboard, wardrobe, generator

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="StyleSense Python")

# Session Middleware (Secret key should be env var in prod, strict for now)
app.add_middleware(SessionMiddleware, secret_key="supersecretkey123")

# Mount Static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    return RedirectResponse(url="/login")

@app.get("/healthz")
def health_check():
    return {"status": "ok", "message": "App is running"}

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(wardrobe.router)
app.include_router(generator.router)

