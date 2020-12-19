from be.model import store

''' 调用 be.model.store 中的 get_db_conn() 方法连接数据库 '''
''' 提供 id 是否存在的判断操作 '''


class DBConn:
    def __init__(self):
        self.conn = store.get_db_conn()

    def user_id_exist(self, user_id):
        cursor = self.conn.cursor().execute("SELECT user_id FROM user WHERE user_id = %s;", (user_id,))
        row = cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def book_id_exist(self, store_id, book_id):
        cursor = self.conn.cursor().execute("SELECT book_id FROM store WHERE store_id = %s AND book_id = %s;", (store_id, book_id))
        row = cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def store_id_exist(self, store_id):
        cursor = self.conn.cursor().execute("SELECT store_id FROM user_store WHERE store_id = %s;", (store_id,))
        row = cursor.fetchone()
        if row is None:
            return False
        else:
            return True
