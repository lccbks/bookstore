import pytest

from fe import conf
from fe.access.seller import Seller
from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
from fe.access.book import Book
import uuid
import random


class TestCart:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller1_id = "test_cart_seller1_id_{}".format(str(uuid.uuid1()))
        self.seller2_id = "test_cart_seller2_id_{}".format(str(uuid.uuid1()))
        self.store1_id = "test_cart_store1_id_{}".format(str(uuid.uuid1()))
        self.store2_id = "test_cart_store2_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_cart_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller1_id
        yield

    @pytest.mark.run(order=51)
    def test_ok(self):
        gen_book_1 = GenBook(self.seller1_id, self.store1_id)
        gen_book_2 = GenBook(self.seller2_id, self.store2_id)
        ok, buy_book_id_list_1 = gen_book_1.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        ok, buy_book_id_list_2 = gen_book_2.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        self.buy_book_info_list_1 = gen_book_1.buy_book_info_list
        self.buy_book_info_list_2 = gen_book_2.buy_book_info_list
        assert ok
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b
        buy_book_id_list_1 = list(list(items) for items in list(buy_book_id_list_1))
        buy_book_id_list_2 = list(list(items) for items in list(buy_book_id_list_2))
        cart_test = {self.store1_id: buy_book_id_list_1, self.store2_id: buy_book_id_list_2}
        for i in self.buy_book_info_list_1:
            code = self.buyer.add_into_cart(self.store1_id, i[0].id, i[1])
            assert code == 200
        for i in self.buy_book_info_list_2:
            code = self.buyer.add_into_cart(self.store2_id, i[0].id, i[1])
            assert code == 200
        code, cart = self.buyer.view_cart()
        assert code == 200
        assert cart == cart_test

    @pytest.mark.run(order=52)
    def test_non_exist_book_in_store(self):
        gen_book_1 = GenBook(self.seller1_id, self.store1_id)
        ok, buy_book_id_list_1 = gen_book_1.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        self.buy_book_info_list_1 = gen_book_1.buy_book_info_list
        assert ok
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b
        for i in self.buy_book_info_list_1:
            code = self.buyer.add_into_cart(self.store1_id, i[0].id+"_x", i[1])
            assert code != 200

    @pytest.mark.run(order=53)
    def test_non_exist_user(self):
        gen_book_1 = GenBook(self.seller1_id, self.store1_id)
        ok, buy_book_id_list_1 = gen_book_1.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        self.buy_book_info_list_1 = gen_book_1.buy_book_info_list
        assert ok
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b
        self.buyer.user_id = self.buyer.user_id + "_x"
        for i in self.buy_book_info_list_1:
            code = self.buyer.add_into_cart(self.store1_id, i[0].id, i[1])
            assert code != 200
        code, cart = self.buyer.view_cart()
        assert code != 200

    @pytest.mark.run(order=54)
    def test_non_exist_store(self):
        gen_book_1 = GenBook(self.seller1_id, self.store1_id)
        ok, buy_book_id_list_1 = gen_book_1.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        self.buy_book_info_list_1 = gen_book_1.buy_book_info_list
        assert ok
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b
        for i in self.buy_book_info_list_1:
            code = self.buyer.add_into_cart(self.store1_id+"_x", i[0].id, i[1])
            assert code != 200
