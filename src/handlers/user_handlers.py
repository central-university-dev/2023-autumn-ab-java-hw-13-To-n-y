from json import JSONDecodeError

from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST

from config import config
from src.jwt_utils import create_token
from src.security import get_hashed_password, verify_password
from src.services.user_service import UserService


async def user_register(request) -> JSONResponse:
    try:
        payload = await request.json()
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


async def user_login(request) -> JSONResponse:
    try:
        payload = await request.json()
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
