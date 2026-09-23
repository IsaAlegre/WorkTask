from dataclasses import dataclass, replace
from enum import Enum

from domain.exceptions import InvalidTransitionError, ValidationError


class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


# Qué estados se pueden alcanzar desde cada estado
ALLOWED_TRANSITIONS = {
    TaskStatus.TODO: {TaskStatus.IN_PROGRESS},
    TaskStatus.IN_PROGRESS: {TaskStatus.TODO, TaskStatus.DONE},
    TaskStatus.DONE: set(),
}


@dataclass(frozen=True)
class Project:
    id: int | None
    name: str

    def __post_init__(self):
        if not self.name.strip():
            raise ValidationError("El nombre del proyecto no puede estar vacío")


@dataclass(frozen=True)
class Task:
    id: int | None
    project_id: int
    title: str
    status: TaskStatus = TaskStatus.TODO

    def __post_init__(self):
        if not self.title.strip():
            raise ValidationError("El título de la tarea no puede estar vacío")

    @property
    def is_open(self) -> bool:
        return self.status != TaskStatus.DONE

    def change_status(self, new_status: TaskStatus) -> "Task":
        if new_status not in ALLOWED_TRANSITIONS[self.status]:
            raise InvalidTransitionError(
                f"No se puede pasar de {self.status.value} a {new_status.value}"
            )
        return replace(self, status=new_status)