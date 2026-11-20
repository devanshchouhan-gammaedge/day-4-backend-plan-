from fastapi import FastAPI, Request
from app.routes import task_routes

app=FastAPI(title="My FastAPI Application", description="This is a sample FastAPI application.", version="1.0.0")

app.include_router(task_routes.router)