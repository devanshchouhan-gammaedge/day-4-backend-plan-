from fastapi import APIRouter, Depends, Query
import json
from app.redis_client import redis_client
from sqlalchemy.orm import Session
from app.schemas.task_model import Task
from app.database.database import get_db
from app.database.database_models import Task as TaskDB
from app.routes.auth import get_current_user
router = APIRouter(prefix="/tasks")


task_list = []
next_task_id = 1
@router.get("/")
def get_tasks(
    skip: int = 0,
    limit: int = 100,
    completed: bool = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # cache_key = f"tasks:{skip}:{limit}:{completed}"
    # cached_tasks = redis_client.get(cache_key)
    # if cached_tasks:
    #   print("CACHE HIT")
    #   return json.loads(cached_tasks)

    # print("CACHE MISS")
    

    query = db.query(TaskDB)

    if completed is not None:
        query = query.filter(TaskDB.completed == completed)

    tasks = query.offset(skip).limit(limit).all()

    # 4. Convert SQLAlchemy objects into dictionaries
    result = [
        {
            "id": task.id,
            "title": task.title,
            "completed": task.completed
        }
        for task in tasks
    ]

    # 5. Store data in Redis for 60 seconds
    redis_client.set(
        cache_key,
        json.dumps(result),
        ex=60
    )

    return result


@router.post("/")
def create_task(
    task: Task,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_task = TaskDB(
        title=task.title,
        completed=task.completed
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "message": "Task created successfully",
        "task": {
            "id": new_task.id,
            "title": new_task.title,
            "completed": new_task.completed
        }
    }


@router.get("/{task_id}")
def get_task(task_id: int):
    for task in task_list:
        if task["id"] == task_id:
            return {
                "message": "Task found",
                "task": task
            }
    raise HTTPException(status_code=404, detail="Task not found")


@router.delete("/{task_id}")
def delete_task(task_id: int):
    for task in task_list:
        if task["id"] == task_id:
            task_list.remove(task)
            return {
                "message": "Task deleted successfully",
                "task": task
            }
    raise HTTPException(status_code=404, detail="Task not found")


@router.put("/{task_id}")
def update_task(task_id : int , new_task : Task):
    for task in task_list:
        if task_id==task["id"]:
            task["title"] = new_task.title
            task["description"] = new_task.description
            task["status"] = new_task.status
            return {
                "message": "Task updated successfully",
                "task": task
            }

    raise HTTPException(status_code=404,detail="user not found")     