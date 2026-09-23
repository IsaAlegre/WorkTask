from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from domain.models import Project, Task, TaskStatus
from infrastructure.persistence.db import ProjectRow, TaskRow


def _to_project(row: ProjectRow) -> Project:
    return Project(id=row.id, name=row.name)


def _to_task(row: TaskRow) -> Task:
    return Task(id=row.id, project_id=row.project_id, title=row.title, status=TaskStatus(row.status))


class SqlProjectRepository:
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory

    def save(self, project: Project) -> Project:
        with self._session_factory() as session:
            row = session.get(ProjectRow, project.id) if project.id else ProjectRow()
            row.name = project.name
            session.add(row)
            session.commit()
            return _to_project(row)

    def find_by_id(self, project_id: int) -> Project | None:
        with self._session_factory() as session:
            row = session.get(ProjectRow, project_id)
            return _to_project(row) if row else None

    def find_all(self) -> list[Project]:
        with self._session_factory() as session:
            rows = session.scalars(select(ProjectRow).order_by(ProjectRow.id)).all()
            return [_to_project(row) for row in rows]

    def delete(self, project_id: int) -> None:
        with self._session_factory() as session:
            row = session.get(ProjectRow, project_id)
            if row:
                session.delete(row)
                session.commit()


class SqlTaskRepository:
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory

    def save(self, task: Task) -> Task:
        with self._session_factory() as session:
            row = session.get(TaskRow, task.id) if task.id else TaskRow()
            row.project_id = task.project_id
            row.title = task.title
            row.status = task.status.value
            session.add(row)
            session.commit()
            return _to_task(row)

    def find_by_id(self, task_id: int) -> Task | None:
        with self._session_factory() as session:
            row = session.get(TaskRow, task_id)
            return _to_task(row) if row else None

    def find_by_project(self, project_id: int, status: TaskStatus | None = None) -> list[Task]:
        with self._session_factory() as session:
            query = select(TaskRow).where(TaskRow.project_id == project_id)
            if status:
                query = query.where(TaskRow.status == status.value)
            rows = session.scalars(query.order_by(TaskRow.id)).all()
            return [_to_task(row) for row in rows]

    def delete(self, task_id: int) -> None:
        with self._session_factory() as session:
            row = session.get(TaskRow, task_id)
            if row:
                session.delete(row)
                session.commit()