from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        tasks = Task.query.all()
        tasks_response = []
        for task in tasks:
            task_complete = bool(task.completed_at)
            tasks_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task_complete    
            })
        return jsonify(tasks_response)
    if request.method == "POST":
        request_body = request.get_json()
        try:
            new_task = Task(title=request_body["title"],
            description=request_body["description"],
            completed_at=request_body["completed_at"])

            db.session.add(new_task)
            db.session.commit()

            task_complete = bool(new_task.completed_at)
            return {
                "task": {
                "id": new_task.task_id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": task_complete  
                }
            }, 201
        except KeyError:
            return {"details": "Invalid data"}, 400 

@task_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response(f"Task {task_id} not found", 404)
    if request.method == "GET":
        task_complete = bool(task.completed_at)
        return {
            "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task_complete  
            }
        }
    if request.method == "PUT":
        request_body = request.get_json()
        task.title = request_body["title"]
        task.description = request_body["description"]
        db.session.commit()
        task = Task.query.get(task_id)
        task_complete = bool(task.completed_at)
        return {
            "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task_complete  
            }
        }
    if request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return {
            "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
        }, 200
