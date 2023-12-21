from typing import Optional

from src.models.user import User
from src.repo.user import UserRepo


class UserService:
    def create_user(
        self, email: str, name: str, role: str, password: str
    ) -> User:
        new_user_id = UserRepo().create_user(
            email=email, name=name, role=role, password=password
        )
        return User(
            id=new_user_id,
            email=email,
            name=name,
            role=role,
            password=password,
        )

    def delete_user(self, user_id: int) -> int:
        result = UserRepo().delete_user(user_id=user_id)
        return result

    def get_user_by_id(self, user_id: int) -> User:
        user = UserRepo().get_user_by_id(user_id=user_id)
        return User(
            id=user_id,
            email=user[1],
            name=user[2],
            role=user[3],
            password=user[4],
        )

    def get_user_by_email(self, user_email: str) -> Optional[User]:
        user = UserRepo().get_user_by_email(user_email=user_email)
        if user is None:
            return None
        return User(
            id=user[0],
            email=user[1],
            name=user[2],
            role=user[3],
            password=user[4],
        )

    # def get_user_by_list_id(self, list_id):
    #     list = ListRepo()
