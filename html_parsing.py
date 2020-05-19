from bs4 import BeautifulSoup
import requests
import re
import json

url = 'https://ru.wowhead.com/npc=162765/%D0%B4%D1%80%D1%83%D0%B6%D0%B5%D0%BB%D1%8E%D0%B1%D0%BD%D0%B0%D1%8F-%D0%B0%D0%BB%D1%8C%D0%BF%D0%B0%D0%BA%D0%B0'

def get_html(url):
    return requests.get(url)

def main():
    html = get_html(url)
    soup = BeautifulSoup(html.content,features="html.parser")
    script_text = soup.find_all('script',text=re.compile(r'^.*\b(g_mapperData)\b.*$',re.M))
    first_line = str(script_text[0].contents[0]).splitlines()[0]
    m = re.compile(r'\"coords.*?}')
    res = m.match(first_line)
    beg = first_line.index('{')
    end = first_line.rindex('}')+1
    print(first_line[beg:end])
    json_obj = json.loads(first_line[beg:end])
    print(json_obj)

    print(script_text)

if __name__ == '__main__':
    main()