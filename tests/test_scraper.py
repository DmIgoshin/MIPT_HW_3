import pytest
import os
import sys

# Добавляет родительскую директорию в sys.path чтобы импортировать scraper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper import get_book_data, scrape_books


def test_get_book_data_returns_dict():
    """Проверяет, что функция get_books_data возвращает словарь"""
    url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
    data = get_book_data(url)
    assert isinstance(data, dict)


def test_get_book_data_has_expected_keys():
    """Проверяет, что присутствуют все необходимые ключи """
    url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
    data = get_book_data(url)
    expected_keys = ['Title', 'Price', 'Rating', 'Availability', 'Description', 'UPC', 'Product Type', 'Price (excl. tax)', 'Price (incl. tax)', 'Tax', 'Number of reviews']
    assert all(key in data for key in expected_keys)


def test_get_book_data_correct_title():
    """Проверяет, что заголовок соответствует необходимому"""
    url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
    data = get_book_data(url)
    assert data['Title'] == 'A Light in the Attic'


def test_scrape_books_returns_list_when_not_saving():
    """Проверяет, что scrape_books возвращает список, когда is_save=False"""
    data = scrape_books(is_save=False)
    assert isinstance(data, list)


def test_books_data_file_has_1000_lines():
    """Проверяет, что books_data.txt содержит ровно 1000 строк"""
    file_path = 'books_data.txt'
    if not os.path.exists(file_path):
        scrape_books(is_save=True)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            i = 0
            for line in f:
                i += 1
            assert i == 1000
    except FileNotFoundError:
        pytest.fail(f"File {file_path} not found.")
