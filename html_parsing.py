import numpy as np
import scipy.linalg
import requests
import re
import json

url = 'https://ru.wowhead.com/npc=162765/%D0%B4%D1%80%D1%83%D0%B6%D0%B5%D0%BB%D1%8E%D0%B1%D0%BD%D0%B0%D1%8F-%D0%B0%D0%BB%D1%8C%D0%BF%D0%B0%D0%BA%D0%B0'

def get_html(url):
    return requests.get(url)

def get_coords(html):
    regex = r"\"coords.*?]]"
    matches = '{' + re.findall(regex, str(html.content), re.M)[0] + '}'
    json_obj = json.loads(matches)
    return np.array(json_obj['coords'], dtype=np.float)

def remove_extra(coords):
    to_remove = set()
    for i in range(len(coords)):
        for j in range(i+1,len(coords)):
            if np.all(np.abs(coords[i] - coords[j]) <= 1.3):
                to_remove.add(j)
    return np.delete(coords,list(to_remove),axis=0)



def main():
    html = get_html(url)
    coord = get_coords(html)
    coord = remove_extra(coord)
    print(coord)


if __name__ == '__main__':
    main()