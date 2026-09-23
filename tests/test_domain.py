import pytest

from domain.exceptions import BusinessRuleError, InvalidTransitionError, ValidationError
from domain.models import Task, TaskStatus



def test_new_task_starts_in_todo():
    assert Task(id=None, project_id=1, title="Algo").status == TaskStatus.TODO


def test_valid_transition_returns_new_task():
    task = Task(id=None, project_id=1, title="Algo")
    moved = task.change_status(TaskStatus.IN_PROGRESS)
    assert moved.status == TaskStatus.IN_PROGRESS
    assert task.status == TaskStatus.TODO  # el original no cambió


def test_cannot_jump_from_todo_to_done():
    with pytest.raises(InvalidTransitionError):
        Task(id=None, project_id=1, title="Algo").change_status(TaskStatus.DONE)


def test_empty_title_is_rejected():
    with pytest.raises(ValidationError):
        Task(id=None, project_id=1, title="   ")

def test_rename_task():
    task = Task(id=None, project_id=1, title="Viejo")
    assert task.rename("Nuevo").title == "Nuevo"


def test_rename_to_empty_title_is_rejected():
    with pytest.raises(ValidationError):
        Task(id=None, project_id=1, title="Algo").rename("  ")


def test_cannot_rename_done_task():
    task = Task(id=None, project_id=1, title="Algo", status=TaskStatus.DONE)
    with pytest.raises(BusinessRuleError):
        task.rename("Otro")