import logging
import os
import sqlite3 as sqlite
import pymysql


class Store:
    # database: str

    def __init__(self):
        # self.database = os.path.join(db_path, "be.db")  # 数据库路径
        self.init_tables()

    ''' 如果不存在对应的表则创建 '''
    def init_tables(self):
        try:
            db = self.get_db_conn()
            cursor = db.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS user ("
                "user_id VARCHAR(100) PRIMARY KEY, "
                "password TEXT NOT NULL, "
                "balance INTEGER NOT NULL, "
                "token TEXT, "
                "terminal TEXT"
                ");"
            )

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS store( "
                "store_id VARCHAR(100), "
                "book_id VARCHAR(10), "
                "book_info TEXT, "
                "stock_level INTEGER,"
                "PRIMARY KEY(store_id, book_id))"
            )

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS user_store("
                "user_id VARCHAR(100), "
                "store_id VARCHAR(100), "
                "PRIMARY KEY(user_id, store_id), "
                "FOREIGN KEY(user_id) REFERENCES user(user_id) ON DELETE CASCADE ON UPDATE CASCADE, "
                "FOREIGN KEY(store_id) REFERENCES store(store_id) ON DELETE CASCADE ON UPDATE CASCADE"
                ");"
            )

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS new_order( "
                "order_id VARCHAR(100) PRIMARY KEY, "
                "user_id VARCHAR(100), "
                "store_id VARCHAR(100), "
                "order_time DATETIME, "
                "state ENUM('dont', 'doing', 'done'), "
                "message TEXT, "
                "FOREIGN KEY(user_id) REFERENCES user(user_id) ON DELETE CASCADE ON UPDATE CASCADE, "
                "FOREIGN KEY(store_id) REFERENCES store(store_id) ON DELETE CASCADE ON UPDATE CASCADE"
                ");"
            )

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS unpay_order("
                "order_id VARCHAR(100), "
                "order_time DATETIME"
                ");"
            )

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS new_order_detail( "
                "order_id VARCHAR(100), "
                "book_id VARCHAR(10), "
                "count INTEGER, "
                "price INTEGER, "
                "PRIMARY KEY(order_id, book_id), "
                "FOREIGN KEY(order_id) REFERENCES new_order(order_id) ON DELETE CASCADE ON UPDATE CASCADE"
                ");"
            )

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS book_comment("
                "user_id VARCHAR(100), "
                "store_id VARCHAR(100), "
                "book_id VARCHAR(10), "
                "comment TEXT, "
                "rate int, "
                "PRIMARY KEY(user_id, store_id, book_id), "
                "FOREIGN KEY(user_id) REFERENCES user(user_id) ON DELETE CASCADE ON UPDATE CASCADE, "
                "FOREIGN KEY(store_id) REFERENCES store(store_id) ON DELETE CASCADE ON UPDATE CASCADE"
                ");"
            )

            db.commit()
        except sqlite.Error as e:
            logging.error(e)
            db.rollback()

    ''' 连接数据库 '''
    def get_db_conn(self):
        db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='1234zxcv',
                             db='bookstore', charset='utf8')
        # return sqlite.connect(self.database)
        return db


database_instance: Store = None


def init_database():
    global database_instance
    database_instance = Store()


def get_db_conn():
    global database_instance
    return database_instance.get_db_conn()


# if __name__ == '__main__':
#     init_database()
