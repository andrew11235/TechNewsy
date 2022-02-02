######
# Cool Tech Newsy Item of the Day Generator
# Source: https://ctnid.blogspot.com/ 
#
# Andrew W
#####

import random
import requests
from re import sub
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
                            line = sub(r"http\S+", "", line)
                            line = sub(r"\.(?=[\S])", ". ", line)
                            line = line.replace('"', "").replace('(', "").replace(')', "")
                            body += line
                    text_file.write(body + "\n")

                link = soup.find("a", attrs={'class': 'blog-pager-older-link'})['href']
                print(link)
            except (TypeError, ConnectionError):
                break


def generate_text():
    with open("TechNewsy.txt", "r", encoding="UTF-8") as corpus:
        gram_dict = dict(FreqDist(list(ngrams(corpus.read().split(), 3))))

    with open("PostList.txt", "a", encoding="UTF-8") as f:
        f.write("[")
        for i in range(500):
            try:
                while True:
                    starting = random.choice(list(gram_dict.keys()))

                    if "." not in starting:
                        txt_list = [starting[i] for i in range(3)]
                        break

                while len(txt_list) < 100 or txt_list[-1][-1] not in [".", "!", "?"]:
                    lis = {k[-1]: gram_dict[k] for k in gram_dict if k[0] == txt_list[-2] and k[1] == txt_list[-1]}

                    next_word = random.choices(list(lis.keys()), list(lis.values()))[0]

                    txt_list.append(next_word)

            except IndexError:
                i -= 1
                continue

            body = " ".join(txt_list).capitalize()
            body = ". ".join(map(lambda s: s.strip().capitalize(), body.split('.')))
            print(i)
            print(body)

            f.write(f', "{body}"' if i > 0 else f'"{body}"')
        f.write("]")


def main():
    get_corpus()
    generate_text()


if __name__ == '__main__':
    main()
