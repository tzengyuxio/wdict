#!/usr/local/bin/python3

import sys
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import urlopen

from bs4 import BeautifulSoup

LANGS = ['ja', 'zh']
LANG_NAMES = {'ja': '日本語', 'zh': '中文', 'zh-tw': '中文-台灣正體', 'zh-cn': '中文-大陆简体'}


def main():
    if len(sys.argv) < 2:
        print("Usage: %s title_in_english_wiki" % sys.argv[0])
        sys.exit(1)

    word = sys.argv[1]
    request_url = "https://en.wikipedia.org/wiki/" + word
    try:
        u = urlopen(request_url)
    except HTTPError as e:
        print('%s: %s' % (e.code, e.msg))
        sys.exit(1)
    soup = BeautifulSoup(u, 'html.parser')
    list_items = soup.find(id='p-lang').find('ul').find_all('li')
    for item in list_items:
        a_node = item.find('a')
        lang = a_node.attrs['lang']
        if lang not in LANGS:
            continue
        if lang == 'zh':
            title = a_node.attrs['title'].split(' ')[0]
            for key in ['zh-cn', 'zh-tw']:
                req_url = "https://zh.wikipedia.org/%s/%s" %(key, quote(title, safe=''))
                soup = BeautifulSoup(urlopen(req_url), 'html.parser')
                loc_title = soup.find(id='firstHeading').text
                print('%s: %s' % (LANG_NAMES[key], loc_title))
        else:
            print('%s: %s' %
                  (LANG_NAMES[lang], a_node.attrs['title'].split(' ')[0]))


main()
