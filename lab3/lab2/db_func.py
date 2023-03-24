import sqlite3 as sq


class DBInteraction:

    def __init__(self, db_path="users.db"):
        self.con = sq.connect(db_path)
        self.con.row_factory = sq.Row
        self.cur = self.con.cursor()

    def __del__(self):
        if self.con:
            self.con.close()

    def get_users(self):
        self.cur.execute("SELECT * FROM users")
        return self.cur.fetchall()

    def get_all_login(self):
        self.cur.execute("SELECT login FROM users")
        return self.cur.fetchall()

    def get_user(self, login: str):
        self.cur.execute("""SELECT * FROM users WHERE login = ?""", (login, ))
        return self.cur.fetchall()

    def add_user(self, value_dict):
        self.cur.execute("""
        INSERT INTO users(login, password_hash, is_admin, 
        is_block, is_new, is_pwd_rules, re_pwd, text_pwd_rules) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                         (value_dict["login"], value_dict["password_hash"],
                          value_dict["is_admin"], value_dict["is_block"],
                          value_dict["is_new"], value_dict["is_pwd_rules"],
                          value_dict["re_pwd"], value_dict["text_pwd_rules"]))
        self.con.commit()

    def update_user_by_login(self, login, value_dict):
        self.cur.execute("""
            UPDATE users SET 
            password_hash = ?, is_admin = ?, 
            is_block = ?,is_new = ?,is_pwd_rules = ?, 
            re_pwd = ?, text_pwd_rules = ? WHERE login = ?""",
                         (value_dict["password_hash"],
                          value_dict["is_admin"], value_dict["is_block"],
                          value_dict["is_new"], value_dict["is_pwd_rules"],
                          value_dict["re_pwd"], value_dict["text_pwd_rules"],
                          login
                          ))
        self.con.commit()

    def update_user_is_new_by_login(self, value_status, login):
        self.cur.execute("""UPDATE users SET is_new = ? WHERE login = ?""",
                         (value_status, login)
                         )
        self.con.commit()

    def get_password_hash_by_login(self, login):
        self.cur.execute("""
        SELECT password_hash FROM users WHERE login = ?
        """, login)
        return self.cur.fetchall()

    def update_password_hash_by_login(self, login, pwd_hash):
        self.cur.execute(
            """UPDATE users SET password_hash = ? WHERE login = ?""",
            (pwd_hash, login)
        )
        self.con.commit()

    def delete_user_by_login(self, login):
        self.cur.execute(
            """DELETE FROM users WHERE login = ?""", (login, )
        )
        self.con.commit()

    def db_init(self):
        with open("db_init.sql", "r") as f:
            sql = f.read()
            self.cur.executescript(sql)
