import pymysql
import uuid
import json
import logging
from be.model import db_conn
from be.model import error

''' buyer 与数据库交互操作的定义 '''


class Buyer(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)
        self.cursor = self.conn.cursor()

    ''' 增加新订单 '''

    def new_order(self, user_id: str, store_id: str, id_and_count: [(str, int)]) -> (int, str, str):
        try:
            num = len(id_and_count)
            id = [i[0] for i in id_and_count]
            ids = '&'.join(id) + '&'
            count = [str(i[1]) for i in id_and_count]
            counts = '&'.join(count) + '&'
            order_id = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))
            self.cursor.callproc('new_order', (user_id, store_id, order_id, ids, counts, str(num), 'flag', 'msg'))
            self.conn.commit()
            # data = self.cursor.fetchall()
            self.cursor.execute("select @_new_order_6,@_new_order_7")
            return_value = self.cursor.fetchone()
            # print(return_value)
            if return_value[0] == 0:
                return 200, "ok", order_id
            if return_value[0] == 1:
                return error.error_non_exist_user_id(return_value[1]) + (order_id,)
            if return_value[0] == 2:
                return error.error_non_exist_store_id(return_value[1]) + (order_id,)
            if return_value[0] == 3:
                return error.error_non_exist_book_id(return_value[1]) + (order_id,)
            if return_value[0] == 4:
                return error.error_stock_level_low(return_value[1]) + (order_id,)
            if return_value[0] == 5:
                logging.info("528, {}".format(return_value[1]))
                return 528, "{}".format(return_value[1]), ""
        except pymysql.Error as e:
            logging.info("528, {}".format(str(e)))
            return 528, "{}".format(str(e)), ""
        except BaseException as e:
            logging.info("530, {}".format(str(e)))
            return 530, "{}".format(str(e)), ""

        return 200, "ok", order_id
    #     order_id = ""
    #     try:
    #         if not self.user_id_exist(user_id):
    #             return error.error_non_exist_user_id(user_id) + (order_id,)
    #         if not self.store_id_exist(store_id):
    #             return error.error_non_exist_store_id(store_id) + (order_id,)
    #         uid = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))
    #
    #         for book_id, count in id_and_count:
    #             self.cursor.execute(
    #                 "SELECT book_id, stock_level, book_info FROM store "
    #                 "WHERE store_id = %s AND book_id = %s;",
    #                 (store_id, book_id))
    #             row = self.cursor.fetchone()
    #             if row is None:
    #                 return error.error_non_exist_book_id(book_id) + (order_id,)
    #
    #             stock_level = row[1]
    #             book_info = row[2]
    #             book_info_json = json.loads(book_info)
    #             price = book_info_json.get("price")
    #
    #             if stock_level < count:
    #                 return error.error_stock_level_low(book_id) + (order_id,)
    #
    #             self.cursor.execute(
    #                 "UPDATE store set stock_level = stock_level - %s "
    #                 "WHERE store_id = %s and book_id = %s and stock_level >= %s; ",
    #                 (count, store_id, book_id, count))
    #             if self.cursor.rowcount == 0:
    #                 return error.error_stock_level_low(book_id) + (order_id,)
    #
    #             self.cursor.execute(
    #                 "INSERT INTO new_order_detail(order_id, book_id, count, price) "
    #                 "VALUES(%s, %s, %s, %s);",
    #                 (uid, book_id, count, price))
    #
    #         self.cursor.execute(
    #             "INSERT INTO new_order(order_id, store_id, user_id) "
    #             "VALUES(%s, %s, %s);",
    #             (uid, store_id, user_id))
    #         self.conn.commit()
    #         order_id = uid
    #     except pymysql.Error as e:
    #         logging.info("528, {}".format(str(e)))
    #         return 528, "{}".format(str(e)), ""
    #     except BaseException as e:
    #         logging.info("530, {}".format(str(e)))
    #         return 530, "{}".format(str(e)), ""
    #
    #     return 200, "ok", order_id

    def payment(self, user_id: str, password: str, order_id: str) -> (int, str):
        try:
            self.cursor.callproc('payment', (user_id, password, order_id, 'flag', 'msg'))
            self.conn.commit()
            self.cursor.execute("select @_payment_3,@_payment_4")
            return_value = self.cursor.fetchone()
            # print(return_value)
            if return_value[0] == 0:
                return 200, "ok"
            if return_value[0] in [1, 5, 9]:
                return error.error_invalid_order_id(return_value[1])
            if return_value[0] == 2 or return_value[0] == 4:
                return error.error_authorization_fail()
            if return_value[0] == 3 or return_value[0] == 6:
                return error.error_non_exist_user_id(return_value[1])
            if return_value[0] == 7:
                return error.error_not_sufficient_funds(return_value[1])
            if return_value[0] == 8:
                return 528, ""
        except pymysql.Error as e:
            return 528, "{}".format(str(e))

        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"
        # conn = self.conn
        # try:
        #     self.cursor.execute("SELECT order_id, user_id, store_id FROM new_order WHERE order_id = %s", (order_id,))
        #     row = self.cursor.fetchone()
        #     if row is None:
        #         return error.error_invalid_order_id(order_id)
        #
        #     order_id = row[0]
        #     buyer_id = row[1]
        #     store_id = row[2]
        #
        #     if buyer_id != user_id:
        #         return error.error_authorization_fail()
        #
        #     self.cursor.execute("SELECT balance, password FROM user WHERE user_id = %s;", (buyer_id,))
        #     row = self.cursor.fetchone()
        #     if row is None:
        #         return error.error_non_exist_user_id(buyer_id)
        #     balance = row[0]
        #     if password != row[1]:
        #         return error.error_authorization_fail()
        #
        #     self.cursor.execute("SELECT store_id, user_id FROM user_store WHERE store_id = %s;", (store_id,))
        #     row = self.cursor.fetchone()
        #     if row is None:
        #         return error.error_non_exist_store_id(store_id)
        #
        #     seller_id = row[1]
        #
        #     if not self.user_id_exist(seller_id):
        #         return error.error_non_exist_user_id(seller_id)
        #
        #     self.cursor.execute("SELECT book_id, count, price FROM new_order_detail WHERE order_id = %s;", (order_id,))
        #     total_price = 0
        #     for row in self.cursor:
        #         count = row[1]
        #         price = row[2]
        #         total_price = total_price + price * count
        #
        #     if balance < total_price:
        #         return error.error_not_sufficient_funds(order_id)
        #
        #     self.cursor.execute("UPDATE user set balance = balance - %s WHERE user_id = %s AND balance >= %s",
        #                         (total_price, buyer_id, total_price))
        #     if self.cursor.rowcount == 0:
        #         return error.error_not_sufficient_funds(order_id)
        #
        #     self.cursor.execute("UPDATE user set balance = balance + %s WHERE user_id = %s",
        #                         (total_price, buyer_id))
        #
        #     if self.cursor.rowcount == 0:
        #         return error.error_non_exist_user_id(buyer_id)
        #
        #     self.cursor.execute("DELETE FROM new_order WHERE order_id = %s", (order_id,))
        #     if self.cursor.rowcount == 0:
        #         return error.error_invalid_order_id(order_id)
        #
        #     self.cursor.execute("DELETE FROM new_order_detail where order_id = %s", (order_id,))
        #     if self.cursor.rowcount == 0:
        #         return error.error_invalid_order_id(order_id)
        #
        #     conn.commit()
        #
        # except pymysql.Error as e:
        #     print(str(e))
        #     return 528, "{}".format(str(e))
        #
        # except BaseException as e:
        #     return 530, "{}".format(str(e))
        #
        # return 200, "ok"

    def add_funds(self, user_id, password, add_value) -> (int, str):
        try:
            self.cursor.execute("SELECT password  from user where user_id=%s", (user_id,))
            row = self.cursor.fetchone()
            if row is None:
                return error.error_authorization_fail()

            if row[0] != password:
                return error.error_authorization_fail()

            self.cursor.execute(
                "UPDATE user SET balance = balance + %s WHERE user_id = %s",
                (add_value, user_id))
            if self.cursor.rowcount == 0:
                return error.error_non_exist_user_id(user_id)

            self.conn.commit()
        except pymysql.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"

    def confirm_receipt(self, user_id: str, order_id: str) -> (int, str):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.order_id_exist(order_id):
                return error.error_non_exist_order_id(order_id)
            self.cursor.execute("SELECT state FROM new_order "
                                "WHERE order_id = %s",
                                order_id)
            row = self.cursor.fetchone()
            if row[0] != 'delivering':
                return error.error_order_state(order_id)
            self.cursor.execute("UPDATE new_order SET state = 'done' "
                                "WHERE order_id = %s",
                                order_id)
            self.conn.commit()
        except pymysql.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def query_order_state(self, user_id: str, order_id: str) -> (int, str):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id) + ("null",)
            if not self.order_id_exist(order_id):
                return error.error_non_exist_order_id(order_id) + ("null",)
            self.cursor.execute("SELECT state FROM new_order "
                                "WHERE order_id = %s",
                                order_id)
            row = self.cursor.fetchone()
            state = row[0]
        except pymysql.Error as e:
            # print(str(e))
            return 528, "{}".format(str(e)), "null"

        except BaseException as e:
            return 530, "{}".format(str(e)), "null"

        return 200, "ok", state

    def cancel_order(self, user_id: str, password: str, order_id: str) -> (int, str):
        try:
            self.cursor.callproc('man_cancel', (user_id, password, order_id, 'flag', 'msg'))
            self.conn.commit()
            self.cursor.execute("select @_man_cancel_3,@_man_cancel_4")
            return_value = self.cursor.fetchone()
            # print(return_value)
            if return_value[0] == 0:
                return 200, "ok"
            if return_value[0] == 1:
                return error.error_non_exist_user_id(return_value[1])
            if return_value[0] == 2:
                return error.error_authorization_fail()
            if return_value[0] in [3, 4, 5, 6]:
                return error.error_invalid_order_id(order_id)
            if return_value[0] == 7:
                return 528, "{}".format(return_value[1])
        except pymysql.Error as e:
            # print(str(e))
            return 528, "{}".format(str(e))

        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"

    def add_comment(self, user_id: str, store_id: str, book_id: str, comment: str, rate: int) -> (int, str):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            self.cursor.execute("SELECT comment FROM book_comment "
                                "WHERE store_id = %s AND book_id = %s",
                                (store_id, book_id))
            row = self.cursor.fetchone()
            if row is not None:
                return error.error_exist_comment()
            self.cursor.execute("SELECT * FROM store "
                                "WHERE store_id = %s AND book_id = %s",
                                (store_id, book_id))
            row = self.cursor.fetchone()
            if row is None:
                return error.error_non_exist_book_in_store(store_id)
            self.cursor.execute("SELECT state FROM new_order, new_order_detail "
                                "WHERE user_id = %s AND "
                                "store_id = %s AND "
                                "book_id = %s AND "
                                "new_order.order_id = new_order_detail.order_id",
                                (user_id, store_id, book_id))
            row = self.cursor.fetchone()
            if row is None:
                return error.error_non_exist_order_id("null")
            if row[0] != "done":
                return error.error_order_state("null")
            self.cursor.execute("INSERT INTO book_comment"
                                "(user_id, store_id, book_id, comment, rate)"
                                "VALUES"
                                "(%s, %s, %s, %s, %s)",
                                (user_id, store_id, book_id, comment, rate))
            self.conn.commit()
        except pymysql.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def view_comments(self, user_id: str, store_id: str, book_id: str) -> (int, str, [str]):
        try:
            comments = []
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id) + ("null",)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id) + ("null",)
            self.cursor.execute("SELECT * FROM store "
                                "WHERE store_id = %s AND book_id = %s",
                                (store_id, book_id))
            row = self.cursor.fetchone()
            if row is None:
                return error.error_non_exist_book_in_store(store_id) + ("null",)
            self.cursor.execute("SELECT comment FROM book_comment "
                                "WHERE store_id = %s AND book_id = %s",
                                (store_id, book_id))
            row = self.cursor.fetchall()
            for i in row:
                comments.append(i[0])
        except pymysql.Error as e:
            return 528, "{}".format(str(e)), "null"
        except BaseException as e:
            return 530, "{}".format(str(e)), "null"
        return 200, "ok", comments
