from json import JSONDecodeError

from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from src.services.list_service import ListService
from src.services.task_service import TaskService
from src.services.user_service import UserService


async def task_by_id(request):
    if 'authenticated' not in request.auth.scopes:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Authenticate first!"
        )
    try:
        task_id = request.path_params['task_id']
        curr_user_id = request.user.user_id
    except JSONDecodeError:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Can't parse payload"
        )
    list_id = TaskService().get_task_by_id(task_id=task_id).list_id
    user_id = ListService().get_list_by_id(list_id=list_id).user_id
    curr_user_role = UserService().get_user_by_id(user_id=curr_user_id).role
    if curr_user_id != user_id and curr_user_role != 'admin':
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Not your task!"
        )
    task = TaskService().get_task_by_id(task_id=task_id)
    return JSONResponse(task.model_dump())


async def all_tasks(request):
    if 'authenticated' not in request.auth.scopes:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Authenticate first!"
        )
    try:
        curr_user_id = request.user.user_id
    except JSONDecodeError:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Can't parse payload"
        )
    curr_user = UserService().get_user_by_id(user_id=curr_user_id)
    if curr_user.role != 'admin':
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Admin only!"
        )
    all_tasks = TaskService().get_all_tasks()
    dump_tasks = [task.model_dump() for task in all_tasks]
    return JSONResponse(dump_tasks)


async def create_task(request):
    if 'authenticated' not in request.auth.scopes:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Authenticate first!"
        )
    try:
        curr_user_id = request.user.user_id
        payload = await request.json()
        task_name = payload['name']
        description = payload['description']
    except JSONDecodeError:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Can't parse payload"
        )
    curr_list = ListService().get_list_by_user_id(user_id=curr_user_id)
    if curr_list is None:
        curr_list_id = (
            ListService()
            .create_list(name='default_list_name', cnt=0, user_id=curr_user_id)
            .id
        )
    else:
        curr_list_id = curr_list.id
    new_task = TaskService().create_task(
        name=task_name, description=description, list_id=curr_list_id
    )
    return JSONResponse(new_task.model_dump())


async def update_task(request):
    if 'authenticated' not in request.auth.scopes:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Authenticate first!"
        )
    try:
        curr_user_id = request.user.user_id
        payload = await request.json()
        task_id = payload['id']
        new_task_name = payload['name']
        new_description = payload['description']
    except JSONDecodeError:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Can't parse payload"
        )
    curr_list = ListService().get_list_by_task_id(task_id=task_id)
    if curr_list is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Create list first!"
        )
    else:
        curr_list_id = curr_list.id
    user_id = curr_list.user_id
    if curr_user_id != user_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Not your task!"
        )
    new_task = TaskService().update_task(
        task_id=task_id,
        list_id=curr_list_id,
        name=new_task_name,
        description=new_description,
    )
    return JSONResponse(new_task.model_dump())


async def delete_task(request):
    if 'authenticated' not in request.auth.scopes:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Authenticate first!"
        )
    try:
        curr_user_id = request.user.user_id
        payload = await request.json()
        task_id = payload['id']
    except JSONDecodeError:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Can't parse payload"
        )
    list_id = TaskService().get_task_by_id(task_id=task_id).list_id
    if list_id is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Create list first!"
        )
    user_id = ListService().get_list_by_id(list_id=list_id).user_id
    if user_id != curr_user_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Not your task!"
        )
    TaskService().delete_task(task_id=task_id)
    return JSONResponse({'deleted_task_id': task_id})
