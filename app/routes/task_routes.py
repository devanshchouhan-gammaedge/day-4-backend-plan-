from fastapi import APIRouter, Depends, HTTPException
from app.schemas.task_model import Task
from app.routes.auth import get_current_user
router = APIRouter(prefix="/tasks")

task_list = []
next_task_id = 1
@router.get("/")
def get_tasks(current_user: dict = Depends(get_current_user)):
    return {
        "message": "List of tasks",
        "tasks": task_list
    }


@router.post("/")
def create_task(task: Task):
    global next_task_id
    new_task=task.model_dump()
    new_task["id"] = next_task_id
    task_list.append(new_task)
    print(f"Current task list: {task_list}")
    next_task_id += 1
    
    return {
        "message": "Task created successfully",
        "task": new_task
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