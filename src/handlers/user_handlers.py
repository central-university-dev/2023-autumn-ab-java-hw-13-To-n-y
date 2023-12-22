from json import JSONDecodeError

from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.templating import Jinja2Templates, _TemplateResponse

from config import config
from src.jwt_utils import create_token
from src.security import get_hashed_password, verify_password
from src.services.user_service import UserService

templates = Jinja2Templates(directory="frontend")


# 'content-type': 'multipart/form-data
async def user_register(request) -> _TemplateResponse | JSONResponse:
    try:
        content_type = request.headers['content-type']
        if content_type == 'text/plain':
            payload: bytes = await request.body()
            payload: str = payload.decode()
            payload: list[str, ...] = payload.split()

            username = payload[0].replace('username=', '')
            email = payload[1].replace('email=', '')
            password = get_hashed_password(payload[2].replace('password=', ''))

            user_exist = UserService().get_user_by_email(user_email=email)
            if user_exist is not None:
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST,
                    detail="Already registered",
                )
            new_user = UserService().create_user(
                name=username, email=email, role='user', password=password
            )

            request.session['email'] = email
            request.session['username'] = username

            user = UserService().get_user_by_email(user_email=email)
            return templates.TemplateResponse(
                "home.html", {"request": request, "user": user, "id": -1}
            )

        elif content_type == 'application/json':
            payload: dict = await request.json()
            username = payload["username"]
            email = payload["email"]
            password = get_hashed_password(payload["password"])
    except JSONDecodeError:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Can't parse json request"
        )
    user_exist = UserService().get_user_by_email(user_email=email)
    if user_exist is not None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Already registered"
        )
    new_user = UserService().create_user(
        name=username, email=email, role='user', password=password
    )

    token = create_token(
        {
            "email": email,
            "username": username,
            "user_id": new_user.id,
            "get_expired_token": 1,
            "expiration_minutes": config.A_EXP,
        }
    )

    return JSONResponse(
        {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "token": token,
        },
        status_code=200,
    )


async def user_login(request) -> _TemplateResponse | JSONResponse:
    try:
        content_type = request.headers['content-type']
        if content_type == 'text/plain':
            payload: bytes = await request.body()
            payload: str = payload.decode()
            payload: list[str, ...] = payload.split()

            email = payload[0].replace('email=', '')
            password = payload[1].replace('password=', '')
            user = UserService().get_user_by_email(user_email=email)
            if user is not None:
                user_hashed_password = user.password
                if verify_password(password, user_hashed_password):
                    request.session['email'] = email
                    request.session['username'] = user.name
                    request.session['user_id'] = user.id
                    print(request.session)
                    user = UserService().get_user_by_email(user_email=email)
                    return templates.TemplateResponse(
                        "home.html",
                        {"request": request, "user": user, "id": -1},
                    )
                else:
                    raise HTTPException(
                        status_code=HTTP_400_BAD_REQUEST,
                        detail="Invalid login or password",
                    )
            else:
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST,
                    detail="Invalid login or password",
                )

        elif content_type == 'application/json':
            payload: dict = await request.json()
            email = payload["email"]
            password = payload["password"]
    except JSONDecodeError:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Can't parse json request"
        )

    user = UserService().get_user_by_email(user_email=email)
    if user is not None:
        user_hashed_password = user.password
        if verify_password(password, user_hashed_password):
            token = create_token(
                {
                    "email": email,
                    "username": user.name,
                    "user_id": user.id,
                    "get_expired_token": 1,
                    "expiration_minutes": config.A_EXP,
                }
            )

            return JSONResponse(
                {
                    "id": user.id,
                    "username": user.name,
                    "email": email,
                    "token": token,
                },
                status_code=200,
            )
        else:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Invalid login or password",
            )
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Invalid login or password",
        )


async def user_logout(request) -> _TemplateResponse:
    content_type = request.headers['content-type']
    if content_type == 'text/plain':
        request.session.clear()
        return templates.TemplateResponse(
            "home.html", {"request": request, "user": None, "id": -1}
        )
