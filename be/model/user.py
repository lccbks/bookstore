import jwt
import time
import logging
import pymysql
from be.model import error
from be.model import db_conn
import base64

''' 用户共有的与数据库之间的操作 '''


# encode a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }


def jwt_encode(user_id: str, terminal: str) -> str:
    encoded = jwt.encode(
        {"user_id": user_id, "terminal": terminal, "timestamp": time.time()},
        key=user_id,
        algorithm="HS256",
    )
    return encoded.decode("utf-8")


# decode a JWT to a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }
def jwt_decode(encoded_token, user_id: str) -> str:
    decoded = jwt.decode(encoded_token, key=user_id, algorithms="HS256")
    return decoded


class User(db_conn.DBConn):
    token_lifetime: int = 3600  # 3600 second

    def __init__(self):
        db_conn.DBConn.__init__(self)
        self.cursor = self.conn.cursor()

    def __check_token(self, user_id, db_token, token) -> bool:
        try:
            if db_token != token:
                return False
            jwt_text = jwt_decode(encoded_token=token, user_id=user_id)
            ts = jwt_text["timestamp"]
            if ts is not None:
                now = time.time()
                if self.token_lifetime > now - ts >= 0:
                    return True
        except jwt.exceptions.InvalidSignatureError as e:
            logging.error(str(e))
            return False

    def register(self, user_id: str, password: str):
        try:
            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)
            self.cursor.execute(
                "INSERT into user(user_id, password, balance, token, terminal) "
                "VALUES (%s, %s, %s, %s, %s);",
                (user_id, password, 0, token, terminal), )
            self.conn.commit()
        except pymysql.Error:
            return error.error_exist_user_id(user_id)
        return 200, "ok"

    def check_token(self, user_id: str, token: str) -> (int, str):
        self.cursor.execute("SELECT token from user where user_id=%s", (user_id,))
        row = self.cursor.fetchone()
        if row is None:
            return error.error_authorization_fail()
        db_token = row[0]
        if not self.__check_token(user_id, db_token, token):
            return error.error_authorization_fail()
        return 200, "ok"

    def check_password(self, user_id: str, password: str) -> (int, str):
        self.cursor.execute("SELECT password from user where user_id=%s", (user_id,))
        row = self.cursor.fetchone()
        if row is None:
            return error.error_authorization_fail()

        if password != row[0]:
            return error.error_authorization_fail()

        return 200, "ok"

    def login(self, user_id: str, password: str, terminal: str) -> (int, str, str):
        token = ""
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message, ""

            token = jwt_encode(user_id, terminal)
            self.cursor.execute(
                "UPDATE user set token= %s , terminal = %s where user_id = %s",
                (token, terminal, user_id), )
            if self.cursor.rowcount == 0:
                return error.error_authorization_fail() + ("",)
            self.conn.commit()
        except pymysql.Error as e:
            return 528, "{}".format(str(e)), ""
        except BaseException as e:
            return 530, "{}".format(str(e)), ""
        return 200, "ok", token

    def logout(self, user_id: str, token: str) -> (int, str):
        try:
            code, message = self.check_token(user_id, token)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            dummy_token = jwt_encode(user_id, terminal)

            self.cursor.execute(
                "UPDATE user SET token = %s, terminal = %s WHERE user_id=%s",
                (dummy_token, terminal, user_id), )
            if self.cursor.rowcount == 0:
                return error.error_authorization_fail()

            self.conn.commit()
        except pymysql.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def unregister(self, user_id: str, password: str) -> (int, str):
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message

            self.cursor.execute("DELETE from user where user_id=%s", (user_id,))
            if self.cursor.rowcount == 1:
                self.conn.commit()
            else:
                return error.error_authorization_fail()
        except pymysql.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def change_password(self, user_id: str, old_password: str, new_password: str) -> (int, str):
        try:
            code, message = self.check_password(user_id, old_password)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)
            self.cursor.execute(
                "UPDATE user set password = %s, token= %s , terminal = %s where user_id = %s",
                (new_password, token, terminal, user_id), )
            if self.cursor.rowcount == 0:
                return error.error_authorization_fail()

            self.conn.commit()
        except pymysql.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def search_author(self, author: str, page: str) -> int:
        self.cursor.execute(
            "select book_id from search_author where author='%s' and search_id BETWEEN %d and %d" % (
                author, 10 * int(page) - 10, 10 * int(page) - 1))
        return 200

    def search_book_intro(self, book_intro: str, page: int) -> int:
        self.cursor.execute(
            "select book_id from search_book_intro where book_intro='%s' and search_id BETWEEN %d and %d" % (
                book_intro, 10 * page - 10, 10 * page - 1))
        return 200

    def search_tags(self, tags: str, page: int) -> int:
        self.cursor.execute(
            "select book_id from search_tags where tags='%s' and search_id BETWEEN %d and %d" % (
                tags, 10 * page - 10, 10 * page - 1))
        return 200

    def search_title(self, title: str, page: int) -> int:
        self.cursor.execute(
            "select book_id from search_title where title='%s' and search_id BETWEEN %d and %d" % (
                title, 10 * page - 10, 10 * page - 1))
        return 200

    def search_author_in_store(self, author: str, store_id: str, page: int) -> int:
        self.cursor.execute(
            "select book_id from search_author where author='%s' and "
            "book_id in (select book_id from store where store_id='%s')"
            "LIMIT 10 OFFSET %d" % (
                author, store_id, 10 * page - 10))
        return 200

    def search_book_intro_in_store(self, book_intro: str, store_id: str, page: int) -> int:
        self.cursor.execute(
            "select book_id from search_book_intro where book_intro='%s' and "
            "book_id in (select book_id from store where store_id='%s')"
            "LIMIT 10 OFFSET %d" % (
                book_intro, store_id, 10 * page - 10))
        return 200

    def search_tags_in_store(self, tags: str, store_id: str, page: int) -> int:
        self.cursor.execute(
            "select book_id from search_tags where tags='%s' and "
            "book_id in (select book_id from store where store_id='%s')"
            "LIMIT 10 OFFSET %d" % (
                tags, store_id, 10 * page - 10))
        return 200

    def search_title_in_store(self, title: str, store_id: str, page: int) -> int:
        self.cursor.execute(
            "select book_id from search_title where title='%s' and "
            "book_id in (select book_id from store where store_id='%s')"
            "LIMIT 10 OFFSET %d" % (
                title, store_id, 10 * page - 10))
        return 200
