from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, dashboard, meal_logs, plans, profile, recipes, water, workouts
from app.core.config import settings
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(title="FitFuel API")

cors_origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
allow_credentials = True
if "*" in cors_origins:
    cors_origins = ["*"]
    allow_credentials = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(plans.router)
app.include_router(recipes.router)
app.include_router(workouts.router)
app.include_router(meal_logs.router)
app.include_router(water.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {"status": "ok"}
