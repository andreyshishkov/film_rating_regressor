import requests

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from dotenv import load_dotenv

import os
from random import choice
import time


load_dotenv()


def get_soup(url: str) -> BeautifulSoup:
    """return soup for current url"""
    # choose proxy
    with open('proxy_file.txt') as file:
        proxy_file = file.read().split('\n')
    ip = choice(proxy_file).strip()
    login = os.environ.get('login')
    password = os.environ.get('password')
    proxy = {
        'http': f'http://{login}:{password}@{ip}',
        'https': f'http://{login}:{password}@{ip}',
    }

    # make fake user agent
    ua = UserAgent()
    fake_ua = {'user-agent': ua.random}

    # make response
    response = requests.get(url=url, headers=fake_ua, proxies=proxy, timeout=30)
    soup = BeautifulSoup(response.text, 'lxml')
    time.sleep(4)
    return soup
