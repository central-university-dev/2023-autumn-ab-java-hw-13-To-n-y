from typing import Optional

from src.models.task import Task
from src.repo.task import TaskRepo


class TaskService:
    def create_task(self, name: str, description: str, list_id: int) -> Task:
        new_task_id = TaskRepo().create_task(
            name=name, description=description, list_id=list_id
        )
        return Task(
            id=new_task_id, name=name, description=description, list_id=list_id
        )

    def delete_task(self, task_id: int) -> int:
        result = TaskRepo().delete_task(task_id=task_id)
        return result

    def update_task(
        self, task_id: int, list_id: int, name: str, description: str
    ) -> Task:
        TaskRepo().update_task(
            task_id=task_id, new_name=name, new_description=description
        )
        return Task(
            id=task_id, name=name, description=description, list_id=list_id
        )

    def get_task_by_id(self, task_id: int) -> Task:
        task = TaskRepo().get_task_by_id(task_id=task_id)
        return Task(
            id=task[0], list_id=task[1], name=task[2], description=task[3]
        )

    def get_all_tasks(self) -> list[Optional[Task], ...]:
        """

        :rtype: object
        """
        db_tasks = TaskRepo().get_all_tasks()
        tasks = [
            Task(
                id=task[0], list_id=task[1], name=task[2], description=task[3]
            )
            for task in db_tasks
        ]
        return tasks
