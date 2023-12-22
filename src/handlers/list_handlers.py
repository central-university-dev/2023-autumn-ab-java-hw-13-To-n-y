from json import JSONDecodeError

from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from starlette.templating import Jinja2Templates

from src.services.list_service import ListService

templates = Jinja2Templates(directory="frontend")


async def homepage(request):
    return templates.TemplateResponse(
        "home.html", {"request": request, "user": None}
    )


async def delete_list(request):
    if 'authenticated' not in request.auth.scopes:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Authenticate first!"
        )
    try:
        curr_user_id = request.user.user_id
        payload = await request.json()
        list_id = payload['id']
    except JSONDecodeError:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Can't parse json request"
        )
    user_id = ListService().get_list_by_id(list_id=list_id).user_id
    if user_id != curr_user_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Not your list!"
        )
    delete_list_id = ListService().delete_list(list_id=list_id)
    return JSONResponse({'deleted_list_id': delete_list_id})


async def create_list(request):
    if 'authenticated' not in request.auth.scopes:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Authenticate first!"
        )
    exist_list = ListService().get_list_by_user_id(request.user.user_id)
    if exist_list is not None:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="List already exists!"
        )
    try:
        payload = await request.json()
        list_name = payload['list_name']
        curr_user_id = request.user.user_id
    except JSONDecodeError:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Can't parse json request"
        )
    list_id = ListService().create_list(
        name=list_name, cnt=0, user_id=curr_user_id
    )
    return JSONResponse({'created_list_id': list_id})
