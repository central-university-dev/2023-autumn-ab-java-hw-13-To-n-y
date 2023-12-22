import jwt
from starlette.authentication import (AuthCredentials, AuthenticationBackend,
                                      AuthenticationError, BaseUser)
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from config import config
from src.jwt_utils import decode_token


class JWTUser(BaseUser):
    def __init__(
            self, username: str, user_id: int, email: str, token: str, **kw
    ) -> None:
        self.username = username
        self.user_id = user_id
        self.email = email
        self.token = token


class JWTAuthenticationBackend(AuthenticationBackend):
    def __init__(
            self, secret_key: str, algorithm: str = "HS256", prefix: str = "Bearer"
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.prefix = prefix

    @classmethod
    def get_token_from_header(cls, authorization: str, prefix: str):
        try:
            token = authorization
        except ValueError:
            raise AuthenticationError(
                "Could not separate Authorization token"
            )
        return token

    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return None
        content_type = request.headers['content-type']
        if content_type == 'application/json':
            authorization = request.headers["Authorization"]
            token = self.get_token_from_header(
                authorization=authorization, prefix=self.prefix
            )
            try:
                jwt_payload = decode_token(token)
            except jwt.ExpiredSignatureError:
                raise AuthenticationError("Expired JWT token")
            except jwt.InvalidTokenError:
                raise AuthenticationError("Invalid JWT token")
            return (
                AuthCredentials(["authenticated"]),
                JWTUser(
                    username=jwt_payload["username"],
                    user_id=jwt_payload["user_id"],
                    email=jwt_payload["email"],
                    token=token,
                ),
            )
        elif content_type == 'text/plain':
            ...


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(
        AuthenticationMiddleware,
        backend=JWTAuthenticationBackend(
            secret_key=str(config.SECRET), algorithm=config.ALGO, prefix=''
        ),
    ),
    Middleware(SessionMiddleware, secret_key=config.SECRET),
]
