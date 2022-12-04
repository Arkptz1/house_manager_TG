import sqlite3 as sl
from config import db_path
import os


class UsersDatabaseConnector:
    """connector to database w/ users"""

    def __init__(self, connect: sl.Connection, cursor: sl.Cursor):
        self.db = connect
        self.cursor = cursor

    def create_table(self):
        """Creates table if not exists."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS User (
                                name TEXT,
                                id int,
                                admin BOOLEAN,
                                it BOOLEAN,
                                electrical BOOLEAN,
                                fireman BOOLEAN,
                                engineer BOOLEAN
                                )''')
        self.db.commit()

    async def get_columns_names(self,) -> list[str]:
        cols = self.cursor.execute('''PRAGMA table_info(User) ''').fetchall()
        cols_res = []
        for i in cols:
            col_name = i[1]
            if not col_name in ['name', 'id']:
                cols_res.append(col_name)
        return cols_res

    async def get_admins(self,) -> list[tuple]:
        ans = self.cursor.execute('SELECT * FROM User WHERE admin').fetchall()
        return ans

    async def add_admins(self, list_id: list) -> None:
        for user_id in list_id:
            data = self.cursor.execute(
                'SELECT * FROM User WHERE id=?', [user_id]).fetchall()
            if len(data) == 0:
                self.cursor.execute(
                    'INSERT INTO User (id, admin) VALUES(?,?)', [user_id, True])
            else:
                self.cursor.execute(
                    f'UPDATE User set admin = {True} WHERE id=?', [user_id])
        self.db.commit()

    async def add_user(self, user_info: dict):
        self.cursor.execute('INSERT INTO User VALUES(?,?,?,?,?,?,?)',
                            list(user_info.values()))
        self.db.commit()

    async def delete_user(self, user_id: int):
        self.cursor.execute('DELETE FROM User WHERE id = ?', [user_id])
        self.db.commit()

    async def get_all_users(self,) -> list[tuple]:
        ans = self.cursor.execute(
            'SELECT * FROM User').fetchall()
        return ans

    async def get_user(self, user_id) -> tuple:
        ans = self.cursor.execute(
            'SELECT * FROM User WHERE id=?', [user_id]).fetchone()
        return ans

    async def update_user(self, user_info: dict):
        _str = 'UPDATE User SET'
        for key in user_info.keys():
            if not (key in ['id', 'name']):
                _str += f' {key}={user_info[key]},'
        _str = _str[:-1]
        _str += f" WHERE id = {user_info['id']}"
        self.cursor.execute(_str)
        self.db.commit()


class FullBd:

    def __init__(self,) -> None:
        self.connect = sl.connect(db_path)
        self.cursor = sl.Cursor(self.connect)
        self.db_users = UsersDatabaseConnector(self.connect, self.cursor)
        self.db_users.create_table()


db = FullBd()
db_users = db.db_users
