from domain.exceptions import BusinessRuleError, NotFoundError
from domain.models import Project, Task, TaskStatus
from domain.ports import ProjectRepository, TaskRepository


class ProjectService:
    def __init__(self, projects: ProjectRepository, tasks: TaskRepository):
        self._projects = projects
        self._tasks = tasks

    def create(self, name: str) -> Project:
        return self._projects.save(Project(id=None, name=name))

    def list_all(self) -> list[Project]:
        return self._projects.find_all()

    def get(self, project_id: int) -> Project:
        project = self._projects.find_by_id(project_id)
        if project is None:
            raise NotFoundError(f"Proyecto {project_id} no encontrado")
        return project

    def delete(self, project_id: int) -> None:
        self.get(project_id)
        if any(task.is_open for task in self._tasks.find_by_project(project_id)):
            raise BusinessRuleError("No se puede borrar un proyecto con tareas abiertas")
        self._projects.delete(project_id)


class TaskService:
    def __init__(self, tasks: TaskRepository, projects: ProjectRepository):
        self._tasks = tasks
        self._projects = projects

    def create(self, project_id: int, title: str) -> Task:
        if self._projects.find_by_id(project_id) is None:
            raise NotFoundError(f"Proyecto {project_id} no encontrado")
        return self._tasks.save(Task(id=None, project_id=project_id, title=title))

    def list_by_project(self, project_id: int, status: TaskStatus | None = None) -> list[Task]:
        if self._projects.find_by_id(project_id) is None:
            raise NotFoundError(f"Proyecto {project_id} no encontrado")
        return self._tasks.find_by_project(project_id, status)

    def get(self, task_id: int) -> Task:
        task = self._tasks.find_by_id(task_id)
        if task is None:
            raise NotFoundError(f"Tarea {task_id} no encontrada")
        return task

    def change_status(self, task_id: int, new_status: TaskStatus) -> Task:
        task = self.get(task_id)
        return self._tasks.save(task.change_status(new_status))

    def delete(self, task_id: int) -> None:
        self.get(task_id)
        self._tasks.delete(task_id)