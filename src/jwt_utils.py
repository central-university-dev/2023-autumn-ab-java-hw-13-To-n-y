import jwt

from config import config


def create_token(payload: dict) -> str:
    """
    encode user payload as a jwt
    :param payload:
    :return:
    """
    encoded_data = jwt.encode(
        payload=payload, key=config.SECRET, algorithm=config.ALGO
    )

    return encoded_data


def decode_token(token: str) -> dict:
    """
    :param token: jwt token
    :return:
    """
    decoded_data = jwt.decode(
        jwt=token, key=config.SECRET, algorithms=[config.ALGO]
    )
    return decoded_data
