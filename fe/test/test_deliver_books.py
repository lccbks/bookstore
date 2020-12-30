import pytest

from fe.access.seller import Seller
from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
from fe.access.book import Book
from fe.access.new_seller import register_new_seller
from fe import conf
from fe.access import seller, auth
import uuid


class TestDeliverBooks:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_deliver_books_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_deliver_books_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_deliver_books_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
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
        yield

    def test_ok(self):
        code = self.buyer.payment(self.order_id)
        assert code == 200
        code = self.seller.deliver_books(self.store_id, self.order_id)
        assert code == 200

    def test_unpaid_order(self):
        code = self.seller.deliver_books(self.store_id, self.order_id)
        assert code != 200

    def test_deliver_twice(self):
        code = self.buyer.payment(self.order_id)
        assert code == 200
        code = self.seller.deliver_books(self.store_id, self.order_id)
        assert code == 200
        code = self.seller.deliver_books(self.store_id, self.order_id)
        assert code != 200

    def test_error_non_exist_store_id(self):
        code = self.buyer.payment(self.order_id)
        assert code == 200
        code = self.seller.deliver_books(self.store_id+"_x", self.order_id)
        assert code != 200

    def test_error_non_exist_user_id(self):
        code = self.buyer.payment(self.order_id)
        assert code == 200
        self.seller.seller_id = self.seller.seller_id + "_x"
        code = self.seller.deliver_books(self.store_id, self.order_id)
        assert code != 200

    def test_error_non_exist_order_id(self):
        code = self.buyer.payment(self.order_id)
        assert code == 200
        code = self.seller.deliver_books(self.store_id, self.order_id+"_x")
        assert code != 200
