import requests
from bs4 import BeautifulSoup
import re
from typing import Optional


def get_book_data(book_url: str) -> dict:
    """
    Парсит данные о товарах по ссылке с сайта books.toscrape.com

    Парсит следующие данные:
    - Название (Title)
    - Цена (Price)
    - Рейтинг (Rating)
    - Доступность (Availability)
    - Описание (Description)
    - UPC
    - Тип товара (Product Type)
    - Цена с налогом (Price (excl. tax))
    - Цена без налога (Price (incl. tax))
    - Размер налога (Tax)
    - Количество отзывов (Number of reviews)

    Args
    ----------
    book_url : str
        Ссылка на страницу с товаром

    Returns
    --------
    dict
        Словарь с данными, полученными со страницы
    """
    data = {}
    response = requests.get(book_url)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find('h1').get_text()
        data['Title'] = name

        price = soup.find(attrs={'class': 'price_color'}).get_text()
        data['Price'] = price
        rating = soup.find('p', class_='star-rating')

        text_to_num = {
            'Zero': 0,
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }
        rating_new = rating.get('class')[1]
        data['Rating'] = text_to_num[rating_new]

        avail = soup.find('p', attrs={'class': 'instock availability'})
        availability = avail.get_text(strip=True)
        number_match = re.search(r'\d+', availability)
        if number_match:
            number = int(number_match.group())
        else:
            number = 0
        data['Availability'] = number

        if soup and soup.find('p', class_=False):
            text = soup.find('p', class_=False).get_text()
        else:
            text = ''
        data['Description'] = text

        table_params = soup.find_all('tr')
        for row in table_params:
            key = row.find('th').get_text()
            if key == 'Availability':
                continue
            value = row.find('td').get_text()
            data[key] = value
        return data
    else:
        print('error')
        return None


def scrape_books(is_save: bool = True) -> Optional[list]:
    """
    Производит скрэпинг и парсинг данных с сайта books.toscrape.com

    Производит скрэпинг по 50 страницам каталога. На каждой странице
    по 20 книг

    Args
    ----------
    is_save : bool
        Если TRUE - сохраняет данные в файл books_data.txt
        Если FALSE - выводит в консоль

    Returns
    --------
    list | None
        Зависит от аргумента is_save:
          Если is_save = False - list
          Если is_save = True - None
    """
    all_books_data = []
    for i in range(1, 51):
        book_url = f'http://books.toscrape.com/catalogue/page-{i}.html'
        response = requests.get(book_url)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            book_links = soup.find_all('h3')
            start_url = 'http://books.toscrape.com/catalogue/'
            for link in book_links:
                book_page_url = start_url + link.find('a')['href']
                book_data = get_book_data(book_page_url)
                if book_data:
                    all_books_data.append(book_data)
        else:
            print(f"Ошибка на странице {i}: {response.status_code}")

    if is_save:
        with open('books_data.txt', 'w', encoding='utf-8') as f:
            for book_data in all_books_data:
                f.write(str(book_data) + '\n')
            print('Успешно сохранено в books_data.txt')
    else:
        return all_books_data
