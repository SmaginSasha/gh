from dotenv import load_dotenv
import os
import requests
import argparse
from urllib.parse import urlparse


def shorten_link(headers, link):
    shorten_link_url = 'https://api-ssl.bitly.com/v4/shorten'
    body = {'long_url': link}

    short_link = requests.post(shorten_link_url, headers=headers, json=body)
    short_link.raise_for_status()
    bitlink = short_link.json()['link']
    return bitlink


def count_clicks(headers, netloc_and_path):
    count_clicks_url = f'https://api-ssl.bitly.com/v4/bitlinks/{netloc_and_path}/clicks/summary'
    response = requests.get(count_clicks_url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(headers, netloc_and_path):
    bitlink_url = f'https://api-ssl.bitly.com/v4/bitlinks/{netloc_and_path}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(bitlink_url, headers=headers)
    return response.ok


def get_netloc_and_path(link):
    parset_link = urlparse(link)
    netloc_and_path = parset_link.netloc + parset_link.path
    return netloc_and_path


if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser(
        description='Сокращение ссылок'
    )
    parser.add_argument('link', help='Надо вставить ссылку или битлинк')
    link = parser.parse_args().link
    token = os.getenv('BITLY_TOKEN')
    headers = {'Authorization': f'Bearer {token}'}
    netloc_and_path = get_netloc_and_path(link)
    if is_bitlink(headers, netloc_and_path):
        print('Кликов по ссылке', count_clicks(headers, netloc_and_path))
    else:
        try:
            print('Битлинк',shorten_link(headers, link))
        except requests.exceptions.HTTPError:
            print('Ваша ссылка неверна')
