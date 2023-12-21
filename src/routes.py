from starlette.routing import Mount, Route

from config import config as conf
from src.handlers.list_handlers import create_list, delete_list, homepage
from src.handlers.task_handlers import (
    all_tasks,
    create_task,
    delete_task,
    task_by_id,
    update_task,
)
from src.handlers.user_handlers import user_login, user_register

task_prefix = conf.api_prefix + 'task/'
list_prefix = conf.api_prefix + 'list'
user_prefix = conf.api_prefix + 'user'

task_routes = [
    Route(
        '/',
        create_task,
        methods=[
            'POST',
        ],
    ),  # create task
    Route(
        '/',
        update_task,
        methods=[
            'PATCH',
        ],
    ),  # update task
    Route(
        '/',
        delete_task,
        methods=[
            'DELETE',
        ],
    ),  # delete task
    Route(
        '/',
        all_tasks,
        methods=[
            'GET',
        ],
    ),  # get all tasks
    Route(
        '/{task_id}',
        task_by_id,
        methods=[
            'GET',
        ],
    ),  # get task by name
]

list_routes = [
    Route(
        '/',
        create_list,
        methods=[
            'GET',
        ],
    ),  # create list
    Route(
        '/',
        delete_list,
        methods=[
            'DELETE',
        ],
    ),  # delete list
]

routes = [
    Route('/', homepage),
    Mount(
        task_prefix,
        routes=task_routes,
    ),
    Mount(
        list_prefix,
        routes=list_routes,
    ),
    Route(
        "/register",
        endpoint=user_register,
        methods=["POST"],
        name="user__register",
    ),
    Route("/login", endpoint=user_login, methods=["POST"], name="user__login"),
]
