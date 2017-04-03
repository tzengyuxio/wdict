#!/usr/local/bin/python3

import sys
from urllib.request import urlopen

from bs4 import BeautifulSoup

LANGS = ['ja', 'zh']
LANG_NAMES = {'ja': '日本語', 'zh': '中文'}


def main():
    if len(sys.argv) < 2:
        print("Usage: %s title_in_english_wiki" % sys.argv[0])
        sys.exit(1)

    word = sys.argv[1]
    request_url = "https://en.wikipedia.org/wiki/" + word
    soup = BeautifulSoup(urlopen(request_url), 'html.parser')
    list_items = soup.find(id='p-lang').find('ul').find_all('li')
    for item in list_items:
        a_node = item.find('a')
        lang = a_node.attrs['lang']
        if lang not in LANGS:
            continue
        print('%s: %s' %
              (LANG_NAMES[lang], a_node.attrs['title'].split(' ')[0]))


main()
