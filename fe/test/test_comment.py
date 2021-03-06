import pytest

from fe import conf
from fe.access.seller import Seller
from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
from fe.access.book import Book
import uuid
import random


class TestComment:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_comment_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_comment_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_comment_buyer_id_{}".format(str(uuid.uuid1()))
        self.comment = "test_comment_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        self.rate = random.randint(0, 5)
        yield

    @pytest.mark.run(order=55)
    def test_ok(self):
        gen_book = GenBook(self.seller_id, self.store_id)
        ok, buy_book_id_list = gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        self.buy_book_info_list = gen_book.buy_book_info_list
        assert ok
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b
        code, self.order_id = b.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        self.total_price = 0
        for item in self.buy_book_info_list:
            book: Book = item[0]
            num = item[1]
            if book.price is None:
                continue
            else:
                self.total_price = self.total_price + book.price * num
        code = self.buyer.add_funds(self.total_price)
        assert code == 200
        s = Seller(conf.URL, self.seller_id, self.password)
        self.seller = s
        code = self.buyer.payment(self.order_id)
        assert code == 200
        code = self.seller.deliver_books(self.store_id, self.order_id)
        assert code == 200
        code = self.buyer.confirm_receipt(self.order_id)
        assert code == 200
        code = self.buyer.add_comment(self.store_id, self.buy_book_info_list[0][0].id, self.comment, self.rate)
        assert code == 200
        code, comments = self.buyer.view_comments(self.store_id, self.buy_book_info_list[0][0].id)
        assert code == 200
        assert comments[0] == self.comment

    @pytest.mark.run(order=56)
    def test_comment_twice(self):
        gen_book = GenBook(self.seller_id, self.store_id)
        ok, buy_book_id_list = gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        self.buy_book_info_list = gen_book.buy_book_info_list
        assert ok
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b
        code, self.order_id = b.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        self.total_price = 0
        for item in self.buy_book_info_list:
            book: Book = item[0]
            num = item[1]
            if book.price is None:
                continue
            else:
                self.total_price = self.total_price + book.price * num
        code = self.buyer.add_funds(self.total_price)
        assert code == 200
        s = Seller(conf.URL, self.seller_id, self.password)
        self.seller = s
        code = self.buyer.payment(self.order_id)
        assert code == 200
        code = self.seller.deliver_books(self.store_id, self.order_id)
        assert code == 200
        code = self.buyer.confirm_receipt(self.order_id)
        assert code == 200
        code = self.buyer.add_comment(self.store_id, self.buy_book_info_list[0][0].id, self.comment, self.rate)
        assert code == 200
        code, comments = self.buyer.view_comments(self.store_id, self.buy_book_info_list[0][0].id)
        assert code == 200
        assert comments[0] == self.comment
        code = self.buyer.add_comment(self.store_id, self.buy_book_info_list[0][0].id, self.comment, self.rate)
        assert code != 200

    @pytest.mark.run(order=57)
    def test_non_exist_book_in_store(self):
        gen_book = GenBook(self.seller_id, self.store_id)
        ok, buy_book_id_list = gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        self.buy_book_info_list = gen_book.buy_book_info_list
        assert ok
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b
        code, self.order_id = b.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        self.total_price = 0
        for item in self.buy_book_info_list:
            book: Book = item[0]
            num = item[1]
            if book.price is None:
                continue
            else:
                self.total_price = self.total_price + book.price * num
        code = self.buyer.add_funds(self.total_price)
        assert code == 200
        s = Seller(conf.URL, self.seller_id, self.password)
        self.seller = s
        code = self.buyer.payment(self.order_id)
        assert code == 200
        code = self.seller.deliver_books(self.store_id, self.order_id)
        assert code == 200
        code = self.buyer.confirm_receipt(self.order_id)
        assert code == 200
        code = self.buyer.add_comment(self.store_id, self.buy_book_info_list[0][0].id+"_x", self.comment, self.rate)
        assert code != 200
        code, comments = self.buyer.view_comments(self.store_id, self.buy_book_info_list[0][0].id+"_x")
        assert code != 200
        assert comments[0] != self.comment

    @pytest.mark.run(order=58)
    def test_non_exist_order(self):
        gen_book = GenBook(self.seller_id, self.store_id)
        ok, buy_book_id_list = gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        self.buy_book_info_list = gen_book.buy_book_info_list
        assert ok
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b
        code = self.buyer.add_comment(self.store_id, self.buy_book_info_list[0][0].id, self.comment, self.rate)
        assert code != 200

    @pytest.mark.run(order=59)
    def test_comment_while_order_is_not_done(self):
        gen_book = GenBook(self.seller_id, self.store_id)
        ok, buy_book_id_list = gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        self.buy_book_info_list = gen_book.buy_book_info_list
        assert ok
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b
        code, self.order_id = b.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        self.total_price = 0
        for item in self.buy_book_info_list:
            book: Book = item[0]
            num = item[1]
            if book.price is None:
                continue
            else:
                self.total_price = self.total_price + book.price * num
        code = self.buyer.add_funds(self.total_price)
        assert code == 200
        s = Seller(conf.URL, self.seller_id, self.password)
        self.seller = s
        code = self.buyer.payment(self.order_id)
        assert code == 200
        code = self.seller.deliver_books(self.store_id, self.order_id)
        assert code == 200
        code = self.buyer.add_comment(self.store_id, self.buy_book_info_list[0][0].id, self.comment, self.rate)
        assert code != 200

    @pytest.mark.run(order=60)
    def test_non_exist_user(self):
        gen_book = GenBook(self.seller_id, self.store_id)
        ok, buy_book_id_list = gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        self.buy_book_info_list = gen_book.buy_book_info_list
        assert ok
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b
        code, self.order_id = b.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        self.total_price = 0
        for item in self.buy_book_info_list:
            book: Book = item[0]
            num = item[1]
            if book.price is None:
                continue
            else:
                self.total_price = self.total_price + book.price * num
        code = self.buyer.add_funds(self.total_price)
        assert code == 200
        s = Seller(conf.URL, self.seller_id, self.password)
        self.seller = s
        code = self.buyer.payment(self.order_id)
        assert code == 200
        code = self.seller.deliver_books(self.store_id, self.order_id)
        assert code == 200
        code = self.buyer.confirm_receipt(self.order_id)
        assert code == 200
        self.buyer.user_id = self.buyer.user_id + "_x"
        code = self.buyer.add_comment(self.store_id, self.buy_book_info_list[0][0].id, self.comment, self.rate)
        assert code != 200
        code, comments = self.buyer.view_comments(self.store_id, self.buy_book_info_list[0][0].id)
        assert code != 200

    @pytest.mark.run(order=61)
    def test_non_exist_store(self):
        gen_book = GenBook(self.seller_id, self.store_id)
        ok, buy_book_id_list = gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        self.buy_book_info_list = gen_book.buy_book_info_list
        assert ok
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b
        code, self.order_id = b.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        self.total_price = 0
        for item in self.buy_book_info_list:
            book: Book = item[0]
            num = item[1]
            if book.price is None:
                continue
            else:
                self.total_price = self.total_price + book.price * num
        code = self.buyer.add_funds(self.total_price)
        assert code == 200
        s = Seller(conf.URL, self.seller_id, self.password)
        self.seller = s
        code = self.buyer.payment(self.order_id)
        assert code == 200
        code = self.seller.deliver_books(self.store_id, self.order_id)
        assert code == 200
        code = self.buyer.confirm_receipt(self.order_id)
        assert code == 200
        code = self.buyer.add_comment(self.store_id+"_x", self.buy_book_info_list[0][0].id, self.comment, self.rate)
        assert code != 200
        code, comments = self.buyer.view_comments(self.store_id+"_x", self.buy_book_info_list[0][0].id)
        assert code != 200
