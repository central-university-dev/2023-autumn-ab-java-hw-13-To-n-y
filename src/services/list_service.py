from typing import Optional

from src.models.list import List
from src.repo.list import ListRepo


class ListService:
    def create_list(self, name: str, cnt: int, user_id: int) -> List:
        new_list_id = ListRepo().create_list(name=name, user_id=user_id)
        return List(id=new_list_id, name=name, cnt=cnt, user_id=user_id)

    def delete_list(self, list_id: int) -> int:
        result = ListRepo().delete_list(list_id=list_id)
        return result

    def get_list_by_id(self, list_id: int) -> List:
        list = ListRepo().get_list_by_id(list_id=list_id)
        return List(id=list[0], name=list[1], cnt=list[2], user_id=list[3])

    def get_list_by_user_id(self, user_id: int) -> Optional[List]:
        list = ListRepo().get_list_by_user_id(user_id=user_id)
        try:
            curr_list = List(
                id=list[0], name=list[1], cnt=list[2], user_id=list[3]
            )
            return curr_list
        except Exception:
            return None

    def get_list_by_task_id(self, task_id: int) -> Optional[List]:
        list = ListRepo().get_list_by_task_id(task_id=task_id)
        try:
            curr_list = List(
                id=list[0], name=list[1], cnt=list[2], user_id=list[3]
            )
            return curr_list
        except Exception:
            return None
