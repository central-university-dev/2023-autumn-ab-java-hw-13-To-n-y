from json import JSONDecodeError

from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from starlette.templating import Jinja2Templates

from src.security import get_csrf_token
from src.services.list_service import ListService
from src.services.task_service import TaskService
from src.services.user_service import UserService

templates = Jinja2Templates(directory="frontend")


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
    try:
        content_type = request.headers['content-type']
        if content_type == 'text/plain':
            curr_user_id = request.session['user_id']
        elif content_type == 'application/json':
            if 'authenticated' not in request.auth.scopes:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="Authenticate first!",
                )
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
    if content_type == 'text/plain':
        return templates.TemplateResponse(
            "all_tasks.html", {"request": request, "todo_list": dump_tasks}
        )
    return JSONResponse(dump_tasks)


async def create_task(request):
    try:
        content_type = request.headers['content-type']
        if content_type == 'text/plain':
            try:
                curr_user_id = request.session['user_id']
                email = request.session['email']
                payload: bytes = await request.body()
            except Exception:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="Authenticate first!",
                )
            payload: str = payload.decode()
            payload: list[str, ...] = payload.split()

            task_name = payload[0].replace('name=', '')
            description = payload[1].replace('description=', '')
            try:
                csrf_token = payload[2].replace('csrf_token=', '')
            except Exception:
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST, detail="Can't parse csrf"
                )
            if csrf_token != get_csrf_token(curr_user_id):
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST, detail="Invalid csrf"
                )
        if content_type == 'application/json':
            if 'authenticated' not in request.auth.scopes:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="Authenticate first!",
                )
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
    if content_type == 'text/plain':
        user = UserService().get_user_by_email(user_email=email)
        return templates.TemplateResponse(
            "home.html",
            {
                "request": request,
                "user": user,
                "id": new_task.id,
                "csrf_token": get_csrf_token(user_id=curr_user_id),
            },
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
