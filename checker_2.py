from pyfiglet import Figlet
from bs4 import BeautifulSoup
from requests import Response
from concurrent.futures import ProcessPoolExecutor
import requests
import datetime
import urllib.parse
import os

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/93.0.4577.63 Safari/537.36"
}

LIST_WORDS = ['SQL',
              'Sql',
              'DBError',
              'Error']


def get_file_lines(filename: str):
    try:
        with open(filename, encoding="utf-8") as f:
            symbols = f.read().split("\n")
            symbols = set(symbols)
            symbols = list(symbols)
            return symbols
    except FileNotFoundError:
        raise SystemExit(f"\n\033[31m\033[1m[ERROR]\033[0m Please check if file "
                         f"\033[31m\033[4m{filename}\033[0m exists\n")


def check_site(site: str):
    tested_urls = []
    try:
        res = requests.get(url=site, headers=HEADERS).text
        soup = BeautifulSoup(res, "lxml")
        forms = soup.find_all("form")

        for form in forms:
            action = form.get('action')
            value = form.find('input').get('name')
            if action and value:
                if 'http' in action:
                    tested_urls.append(f'{action}?{value}=1')
                else:
                    if site[-1] == '/':
                        site = site[0:-1]
                        tested_urls.append(f'{site}{action}?{value}=1')
                    else:
                        tested_urls.append(f'{site}{action}?{value}=1')
        return tested_urls
    except:
        return False
        print(f"\n\033[31m\033[1m[ERROR]\033[0m Please check your url \033[31m\033[4m{site}\033[0m\n")


def error_in_body(response: Response) -> bool:
    for word in LIST_WORDS:
        if word in response.text:
            return True
    return False


def finish(site: str):
    counter = 0
    symbols = get_file_lines('payloads.txt')
    tested_urls = check_site(site)

    if not tested_urls:
        return \
            print(
                f"\033[31m\033[1m[ERROR]\033[0m \033[34m\033[4mURL\033[0m \033[31m\033[4m{site}\033[0m \033[33m\033[1mHASN'T "
                f"\033[34m\033[1m<form>\033[0m \033[33m\033[1mTAG\033[0m")
    else:
        for tested_url in tested_urls:
            for symbol in symbols:
                symbol = urllib.parse.quote_plus(symbol)
                url = f'{tested_url}{symbol}'
                res = requests.get(url)

                cur_time = datetime.datetime.now().strftime("%H:%M:%S")
                print(
                    f"\033[33m\033[1m[{cur_time} - INFO]\033[0m: \033[34m\033[4m{url}\033[0m \033[33m\033[1mIS CHECKING....🤔\033[0m")

                if error_in_body(res):
                    cur_time = datetime.datetime.now().strftime("%H:%M:%S")
                    print(
                        f"\033[32m\033[1m[{cur_time} - GOOD]\033[0m \033[33m\033[1mSQL-INJECTION IS POSSIBLE\033[0m "
                        f"\033[34m\033[4m{url}\033[0m ❗❗❗")
                    counter += 1
                    with open('inj_sites.txt', 'a+', encoding='utf-8') as file:
                        file.write(f'{url}\n')
                else:
                    cur_time = datetime.datetime.now().strftime("%H:%M:%S")
                    print(
                        f"\033[31m\033[1m[{cur_time} - BAD]\033[0m \033[33m\033[1m NOT INJECTION \033[0m "
                        f"\033[34m\033[4m{url}\033[0m")
    return


def main():
    try:
        sites = get_file_lines('sites.txt')
    except FileNotFoundError:
        raise SystemExit(
            f"\n\033[31m\033[1m[ERROR]\033[0m Please check if file \033[31m\033[4msites.txt\033[0m exists\n")

    with ProcessPoolExecutor(max_workers=10) as ex:
        ex.map(finish, sites)

    if os.path.exists('inj_sites.txt'):
        counter = len(get_file_lines('inj_sites.txt'))
        cur_time = datetime.datetime.now().strftime("%H:%M:%S")
        return print(
            f"\n\033[33m\033[1m[GOOD WORK]\033[0m \033[34m\033[4m{counter}\033[0m URLS \033[33m\033[1mMAYBE HAS SQL-VULNERABILITY\033[0m ❗❗❗")
    else:
        cur_time = datetime.datetime.now().strftime("%H:%M:%S")
        return print(
            f"\n\033[33m\033[1m[BAD WORK]\033[0m \033[34m\033[4m0\033[0m MAYBE HAS SQL-VULNERABILITY")


if __name__ == "__main__":
    preview_text = Figlet(font='doom', width=200)
    text = preview_text.renderText('SQL - Injections  Checker  v.2.0')
    print(f'\033[35m\033[1m{text}\033[0m')
    print("\033[35m\033[1m-\033[0m" * 140)

    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\033[36m\033[1m[INFO]\033[0m PROGRAM STOPPED BY USER\n")
