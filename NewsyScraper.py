######
# Cool Tech Newsy Item of the Day Generator
# Source: https://ctnid.blogspot.com/ 
# Web: https://sites.google.com/cusd.me/tech-newsy-generator/newsy-generator
# 
# 2022 Andrew Wang
#####

import requests
from random import choice, choices
from re import sub, split

from bs4 import BeautifulSoup
from nltk import FreqDist, ngrams


def get_corpus():
    link = "https://ctnid.blogspot.com/search?max-results=999"

    with open("TechNewsy.txt", "w", encoding="UTF=8") as text_file:
        while True:
            try:
                res = requests.get(link)
                soup = BeautifulSoup(res.content, 'html.parser')
                posts = soup.find_all("div", attrs={"class": 'post-body'})

                for p in posts:
                    body = ""
                    p = p.text.split("\n")
                    for line in p:
                        if not (line.startswith("https:") or line.startswith("Credit")):
                            line = sub(r"http\S+", "", line)
                            line = sub(r"\.(?=[\S])", ". ", line)
                            line = line.replace('"', "").replace('(', "").replace(')', "")
                            body += line
                    text_file.write(body + "\n")

                link = soup.find("a", attrs={'class': 'blog-pager-older-link'})['href']
                print(link)
            except (TypeError, ConnectionError):
                break


def gen_grams() -> dict:
    with open("TechNewsy.txt", "r", encoding="UTF-8") as corpus:
        return dict(FreqDist(list(ngrams(corpus.read().split(), 3))))


def gen_text(g_dict: dict, itters: int = 1_000_000):
    with open("PostList.txt", "w", encoding="UTF-8") as f:
        for i in range(itters):
            try:
                while True:
                    starting = choice(list(g_dict.keys()))

                    if "." not in starting:
                        txt_list = [starting[i] for i in range(3)]
                        break

                while len(txt_list) < 100 or txt_list[-1][-1] not in [".", "!", "?"]:
                    lis = {k[-1]: g_dict[k] for k in g_dict if k[0] == txt_list[-2] and k[1] == txt_list[-1]}

                    next_word = choices(list(lis.keys()), list(lis.values()))[0]

                    txt_list.append(next_word)

            except IndexError:
                i -= 1
                
            else:
                body = " ".join(txt_list).capitalize()
                body = ". ".join(map(lambda s: s.strip().capitalize(), split(r'\.(?=[\D])', body)))
                print(i, body)

                f.write(f', "{body}"' if i > 0 else f'"{body}"')


if __name__ == '__main__':
    get_corpus()
    gen_text(gen_grams(), 100)
