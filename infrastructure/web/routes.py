from flask import Blueprint, jsonify, request

from application.services import ProjectService, TaskService
from domain.exceptions import ValidationError
from domain.models import Project, Task, TaskStatus


def _project_json(project: Project) -> dict:
    return {"id": project.id, "name": project.name}


def _task_json(task: Task) -> dict:
    return {"id": task.id, "project_id": task.project_id, "title": task.title, "status": task.status.value}


def _parse_status(value: str) -> TaskStatus:
    try:
        return TaskStatus(value.upper())
    except ValueError:
        raise ValidationError(f"Estado inválido: {value}")


def _body() -> dict:
    return request.get_json(silent=True) or {}


def create_api_blueprint(projects: ProjectService, tasks: TaskService) -> Blueprint:
    api = Blueprint("api", __name__)

    # ---------- Proyectos ----------
    @api.get("/projects")
    def list_projects():
        return jsonify([_project_json(p) for p in projects.list_all()])

    @api.post("/projects")
    def create_project():
        project = projects.create(str(_body().get("name") or ""))
        return jsonify(_project_json(project)), 201

    @api.get("/projects/<int:project_id>")
    def get_project(project_id: int):
        return jsonify(_project_json(projects.get(project_id)))

    @api.delete("/projects/<int:project_id>")
    def delete_project(project_id: int):
        projects.delete(project_id)
        return "", 204

    # ---------- Tareas ----------
    @api.get("/projects/<int:project_id>/tasks")
    def list_tasks(project_id: int):
        status_param = request.args.get("status")
        status = _parse_status(status_param) if status_param else None
        return jsonify([_task_json(t) for t in tasks.list_by_project(project_id, status)])

    @api.post("/projects/<int:project_id>/tasks")
    def create_task(project_id: int):
        task = tasks.create(project_id, str(_body().get("title") or ""))
        return jsonify(_task_json(task)), 201

    @api.get("/tasks/<int:task_id>")
    def get_task(task_id: int):
        return jsonify(_task_json(tasks.get(task_id)))

    @api.patch("/tasks/<int:task_id>/status")
    def change_task_status(task_id: int):
        new_status = _parse_status(str(_body().get("status") or ""))
        return jsonify(_task_json(tasks.change_status(task_id, new_status)))

    @api.delete("/tasks/<int:task_id>")
    def delete_task(task_id: int):
        tasks.delete(task_id)
        return "", 204

    return api