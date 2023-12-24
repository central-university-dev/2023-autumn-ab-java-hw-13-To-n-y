from typing import Optional

from db.db import conn


class UserRepo:
    def get_user_by_id(self, user_id: int) -> Optional[tuple]:
        insert = (user_id,)
        req = '''SELECT * FROM user WHERE id = ?;'''
        cursor = conn.cursor()
        user = cursor.execute(req, insert).fetchone()
        cursor.close()
        conn.commit()
        return user

    def get_user_by_email(self, user_email: str) -> Optional[tuple]:
        insert = (user_email,)
        req = '''SELECT * FROM user WHERE email = ?;'''
        cursor = conn.cursor()
        user = cursor.execute(req, insert).fetchone()
        cursor.close()
        conn.commit()
        return user

    def create_user(
        self, email: str, name: str, role: str, password: str
    ) -> int:
        insert = (email, name, role, password)
        req = '''INSERT INTO user (email,
                            name, 
                            role,
                            password) VALUES (?, ?, ?, ?);'''
        created_user_id = -1
        cursor = conn.cursor()
        cursor.execute(req, insert)
        created_user_id = cursor.lastrowid
        cursor.close()
        conn.commit()
        return created_user_id

    def delete_user(self, user_id: int) -> int:
        req = '''DELETE FROM user
            WHERE id = ?;'''
        cursor = conn.cursor()
        insert = (user_id,)
        cursor.execute(req, insert)
        cursor.close()
        conn.commit()
        return user_id
