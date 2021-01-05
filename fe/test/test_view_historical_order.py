import pytest
import time
from fe import conf
from fe.access.seller import Seller
from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
from fe.access.book import Book
import uuid


class TestViewHistoricalOrder:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_view_historical_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_view_historical_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_view_historical_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        gen_book = GenBook(self.seller_id, self.store_id)
        ok, buy_book_id_list = gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        self.buy_book_info_list = gen_book.buy_book_info_list
        assert ok
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b
        code, self.order_id = b.new_order(self.store_id, buy_book_id_list)
        self.time = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.localtime(time.time()))
        yield

    @pytest.mark.run(order=62)
    def test_ok(self):
        orders_test = [{"order_id": self.order_id, "store_id": self.store_id, "order_time": self.time, "state": "unpaid"}]
        code, orders = self.buyer.view_historical_order()
        assert code == 200
        assert orders == orders_test

    @pytest.mark.run(order=63)
    def test_non_exist_user(self):
        orders_test = [
            {"order_id": self.order_id, "store_id": self.store_id, "order_time": self.time, "state": "unpaid"}]
        self.buyer.user_id = self.buyer.user_id + "_x"
        code, orders = self.buyer.view_historical_order()
        assert code != 200
