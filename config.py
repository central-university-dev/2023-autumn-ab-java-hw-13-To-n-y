import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Config:
    api_prefix = '/api/v1/'

    DBPATH = os.environ.get(
        "DBPATH"
    )
    SECRET = os.environ.get(
        "SECRET"
    )
    ALGO = os.environ.get(
        "ALGO"
    )
    A_EXP = os.environ.get(
        "A_EXP"
    )
    B_EXP = os.environ.get(
        "B_EXP"
    )


config = Config()
