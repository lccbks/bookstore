import time

import pytest
from fe.access.new_seller import register_new_seller
from fe.access.book import Book
from fe.access import book
from fe.access import auth
from fe import conf
import uuid
import random


class TestSearch:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.auth = auth.Auth(conf.URL)
        self.author = "test_author_{}".format(str(uuid.uuid1()))
        self.book_intro = "test_book_intro_{}".format(str(uuid.uuid1()))
        self.tags = "test_tags_{}".format(str(uuid.uuid1()))
        self.title = "test_title_{}".format(str(uuid.uuid1()))
        self.store_id = "test_store_id_{}".format(str(uuid.uuid1()))
        self.page = random.randint(1, 10)
        yield

    def test_search(self):
        assert self.auth.search_author(self.author, self.page) == 200
        assert self.auth.search_book_intro(self.book_intro, self.page) == 200
        assert self.auth.search_tags(self.tags, self.page) == 200
        assert self.auth.search_title(self.title, self.page) == 200
        assert self.auth.search_author_in_store(self.author, self.store_id, self.page) == 200
        assert self.auth.search_book_intro_in_store(self.book_intro, self.store_id, self.page) == 200
        assert self.auth.search_tags_in_store(self.title, self.store_id, self.page) == 200
        assert self.auth.search_title_in_store(self.tags, self.store_id, self.page) == 200

    def test_search_example(self):
        self.store_id = "test_books_store_id_e324ffs1-214d-13rg-f27g-abdf24671235"
        assert self.auth.search_author("鲁迅", 1) == 200
        assert self.auth.search_book_intro("茴香豆", 1) == 200
        assert self.auth.search_tags("小说", 1) == 200
        assert self.auth.search_title("呐喊", 1) == 200
        assert self.auth.search_author_in_store("鲁迅", self.store_id, 1) == 200
        assert self.auth.search_book_intro_in_store("茴香豆", self.store_id, 1) == 200
        assert self.auth.search_tags_in_store("小说", self.store_id, 1) == 200
        assert self.auth.search_title_in_store("呐喊", self.store_id, 1) == 200