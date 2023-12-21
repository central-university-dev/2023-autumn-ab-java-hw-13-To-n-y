from db.db import conn


class ListRepo:
    def get_list_by_id(self, list_id: int) -> tuple:
        req = '''SELECT * FROM task_list WHERE id = ?;'''
        cursor = conn.cursor()
        insert = (list_id,)
        curr_list = cursor.execute(req, insert).fetchone()
        cursor.close()
        conn.commit()
        return curr_list

    def get_list_by_user_id(self, user_id: int) -> tuple:
        req = '''SELECT * FROM task_list WHERE user_id = ?;'''
        cursor = conn.cursor()
        insert = (user_id,)
        curr_list = cursor.execute(req, insert).fetchone()
        cursor.close()
        conn.commit()
        return curr_list

    def get_list_by_task_id(self, task_id: int) -> tuple:
        req = '''SELECT * FROM task_list
         WHERE id = (SELECT list_id from task WHERE id = ?);'''
        cursor = conn.cursor()
        insert = (task_id,)
        curr_list = cursor.execute(req, insert).fetchone()
        cursor.close()
        conn.commit()
        return curr_list

    def create_list(self, name, user_id) -> int:
        insert = (name, user_id)
        req = '''INSERT INTO task_list (name,
                                            cnt, 
                                            user_id) 
                                            VALUES (?, 0, ?);'''
        created_list_id = -1
        cursor = conn.cursor()
        cursor.execute(req, insert)
        created_list_id = cursor.lastrowid
        cursor.close()
        conn.commit()
        return created_list_id

    def delete_list(self, list_id) -> int:
        req = '''DELETE FROM task_list
                    WHERE id = ?;'''
        cursor = conn.cursor()
        insert = (list_id,)
        cursor.execute(req, insert).fetchone()
        cursor.close()
        conn.commit()
        return list_id

    def update_list_cnt(self, list_id: int, add: int) -> int:
        req1 = '''SELECT cnt FROM task_list WHERE id = ?;'''
        req2 = '''UPDATE task_list
                              SET cnt = ?
                              WHERE id = ?;'''
        cursor = conn.cursor()
        insert1 = (list_id,)
        curr_cnt = cursor.execute(req1, insert1).fetchone()[0]
        curr_cnt += add
        insert2 = (curr_cnt, list_id)
        cursor.execute(req2, insert2)
        cursor.close()
        conn.commit()
        return curr_cnt
