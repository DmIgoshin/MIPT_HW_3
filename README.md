# Домашнее задание 3


## Цель

Выполнить домашнее задание, а также предоставить возможность всем желающим парсить данные с сайта [books.toscrape.com](http://books.toscrape.com)

## Инструкции по запуску

Открыть файл **scraper.py**, где есть 2 функции: 
```
get_book_data(book_url: str) -> dict
``` 
(производит парсинг данных одного товара по ссылке). В качестве аргумента указывается ссылка на страницу с товаром.
```
 scrape_books(is_save: bool = True) -> list | None
 ``` 
 (производит скрэпинг и парсинг 50 страниц каталога с 20 товарами на каждой странице). Если **is_save=True**, то результат сохраняется в файл **books_data.txt** 

### Пример вызова первой функции: 
```
book_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
get_book_data(book_url)
```
### Пример вызова второй функции
```
scrape_books(is_save=True)
#результат сохранится в books_data.txt
```

## Список используемых библиотек
```
beautifulsoup4==4.14.2
bs4==0.0.2
certifi==2025.10.5
charset-normalizer==3.4.4
colorama==0.4.6
idna==3.11
iniconfig==2.3.0
packaging==25.0
pluggy==1.6.0
Pygments==2.19.2
pytest==9.0.0
requests==2.32.5
schedule==1.2.2
soupsieve==2.8
typing==3.7.4.3
typing_extensions==4.15.0
urllib3==2.5.0
```
