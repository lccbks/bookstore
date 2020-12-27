from be.model import store

''' 调用 be.model.store 中的 get_db_conn() 方法连接数据库 '''
''' 提供 id 是否存在的判断操作 '''


class DBConn:
    def __init__(self):
        self.conn = store.get_db_conn()
        self.cursor = self.conn.cursor()

    def user_id_exist(self, user_id):
        self.cursor.execute("SELECT user_id FROM user WHERE user_id = %s;", (user_id,))
        row = self.cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def book_id_exist(self, store_id, book_id):
        self.cursor.execute("SELECT book_id FROM store WHERE store_id = %s AND book_id = %s;", (store_id, book_id))
        row = self.cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def store_id_exist(self, store_id):
        self.cursor.execute("SELECT store_id FROM user_store WHERE store_id = %s;", (store_id,))
        row = self.cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def order_id_exist(self, order_id):
        self.cursor.execute("SELECT order_id FROM new_order WHERE order_id= %s;", (order_id,))
        row = self.cursor.fetchone()
        if row is None:
            return False
        else:
            return True
