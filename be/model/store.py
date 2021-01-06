import logging
import os
import pymysql


class Store:

    def __init__(self):
        try:
            db = self.get_db_conn()
            db.commit()
        except pymysql.Error as e:
            logging.error(e)
            exit(-1)

    ''' 连接数据库 '''
    def get_db_conn(self):
        db = pymysql.connect(host='127.0.0.1', port=3306, user='bookstore', password='Bookstore@2020',
                             db='bookstore', charset='utf8')
        return db


database_instance: Store = None


def init_database():
    global database_instance
    database_instance = Store()


def get_db_conn():
    global database_instance
    return database_instance.get_db_conn()


if __name__ == '__main__':
    init_database()
