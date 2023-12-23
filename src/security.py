import binascii
import os

from passlib.context import CryptContext

from db.db import conn

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_csrf_token(user_id: int) -> str:
    return binascii.hexlify(os.urandom(20)).decode()


def get_csrf_token(user_id: int) -> str:
    req = '''SELECT token FROM csrf_token
                        WHERE user_id = ?;'''
    cursor = conn.cursor()
    insert = (user_id,)
    token = cursor.execute(req, insert).fetchone()[0]
    cursor.close()
    return token


def set_csrf_token(user_id: int) -> str:
    # create csrf_token
    req = '''INSERT INTO csrf_token (user_id, token) VALUES
    (?, ?);'''
    csrf_token = create_csrf_token(user_id=user_id)
    cursor = conn.cursor()
    insert = (user_id, csrf_token)
    cursor.execute(req, insert)
    cursor.close()
    conn.commit()
    return csrf_token
