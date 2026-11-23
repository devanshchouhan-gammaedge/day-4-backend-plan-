from fastapi import FastAPI, Request
from app.routes import task_routes
from app.routes.auth import router as auth_router

app=FastAPI(title="My FastAPI Application", description="This is a sample FastAPI application.", version="1.0.0")



@app.middleware("http")
async def my_middleware(request:Request,call_next):
    print(f"response url{request.url} and response method is : {request.method}")
    response=await call_next(request)
    print(f"response is {response} and response status code is {response.status_code}")
    return response


app.include_router(task_routes.router)
app.include_router(auth_router)