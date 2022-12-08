import re
import socket
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

SSTMK_URL = "https://sstmk.ru"


def get_site_status_code(url):
    """Возвращает True если status code < 400

    Args:
        url (_type_): url сайта

    Returns:
        _type_: результат работы
    """
    response_header = requests.head(url)
    return response_header.ok
    


def get_ip(url: str) -> str:
    """Определяет IP адрес

    Args:
        hostname (str): url сайта

    Returns:
        str: IP адрес
    """
    hostname = urlparse(url).hostname
    return socket.gethostbyname(hostname)


def get_html(url: str) -> str:
    """Получает HTML сайта

    Args:
        url (str): url сайта

    Returns:
        str: HTML разметка
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def get_phone_number(url: str) -> str:
    """Получает номер телефона

    Args:
        url (str): url сайта

    Returns:
        str: номер телефона
    """
    soup = BeautifulSoup(get_html(url), "html.parser")
    return soup.find("div", class_="phone-number").text


def check_phone_number_format(phone_number: str) -> bool:
    """Проверка формата телефонного номера

    Args:
        phone_number (str): номер телефона

    Returns:
        bool: результат проверки
    """
    pattern = "^(\+?\d{1,3})?\(?\d{1,}\)(\d{1,})-(\d{1,})-(\d{1,})"
    return re.match(pattern, phone_number)


def main() -> None:
    """Основная функция"""
    try:
        if get_site_status_code(SSTMK_URL):
            print(f"Сайт {SSTMK_URL} доступен")
            print(f"IP адрес сайта {SSTMK_URL}: {get_ip(SSTMK_URL)} ")
            phone_number = get_phone_number(SSTMK_URL)
            if not check_phone_number_format(phone_number):
                print(f"Преобразованный телефонный номер: {phone_number.replace(' ', '')}")
            else:
                print(f"Телефонный номер: {phone_number}")
    except requests.exceptions.ConnectionError:
        print(f"Сайт {SSTMK_URL} недоступен")


if __name__ == "__main__":
    main()
