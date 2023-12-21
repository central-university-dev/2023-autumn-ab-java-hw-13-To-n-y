from db.db import conn
from src.repo.list import ListRepo


class TaskRepo:
    def get_task_by_id(self, task_id: int) -> tuple:
        req = '''SELECT * FROM task
                            WHERE id = ?;'''
        cursor = conn.cursor()
        insert = (task_id,)
        curr_task = cursor.execute(req, insert).fetchone()
        cursor.close()
        conn.commit()
        return curr_task

    def get_all_tasks(self) -> list:
        req = '''SELECT * FROM task LIMIT 50;'''
        cursor = conn.cursor()
        task_list = cursor.execute(req).fetchall()
        cursor.close()
        conn.commit()
        return task_list

    def create_task(self, name: str, description: str, list_id: int) -> int:
        insert = (name, description, list_id)
        req = '''INSERT INTO task (name,
                                    description, 
                                    list_id) 
                                    VALUES (?, ?, ?);'''
        created_task_id = -1
        cursor = conn.cursor()
        cursor.execute(req, insert)
        created_task_id = cursor.lastrowid
        cursor.close()
        conn.commit()
        ListRepo().update_list_cnt(list_id, 1)
        return created_task_id

    def update_task(
        self, task_id: int, new_name: str, new_description: str
    ) -> int:
        insert = (new_name, new_description, task_id)
        req = '''UPDATE task
              SET name = ? ,
                  description = ?
              WHERE id = ?'''
        cursor = conn.cursor()
        cursor.execute(req, insert)
        cursor.close()
        conn.commit()
        return task_id

    def delete_task(self, task_id: int) -> int:
        req1 = '''SELECT list_id FROM task
                    WHERE id = ?;'''
        req2 = '''DELETE FROM task
                    WHERE id = ?;'''
        cursor = conn.cursor()
        insert = (task_id,)
        list_id = cursor.execute(req1, insert).fetchone()[0]
        cursor.execute(req2, insert)
        cursor.close()
        conn.commit()
        ListRepo().update_list_cnt(list_id, -1)
        return task_id
