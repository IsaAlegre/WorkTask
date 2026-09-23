from flask import Flask, jsonify

from application.services import ProjectService, TaskService
from infrastructure.config import database_url
from infrastructure.persistence.db import build_session_factory
from infrastructure.persistence.repositories import SqlProjectRepository, SqlTaskRepository
from infrastructure.web.errors import register_error_handlers
from infrastructure.web.routes import create_api_blueprint


def create_app() -> Flask:
    # 1. Adaptadores de salida
    session_factory = build_session_factory(database_url())
    project_repo = SqlProjectRepository(session_factory)
    task_repo = SqlTaskRepository(session_factory)

    # 2. Casos de uso
    project_service = ProjectService(project_repo, task_repo)
    task_service = TaskService(task_repo, project_repo)

    # 3. Adaptador de entrada (Flask)
    app = Flask(__name__)
    app.register_blueprint(create_api_blueprint(project_service, task_service))
    register_error_handlers(app)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    return app