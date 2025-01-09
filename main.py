from bs4 import BeautifulSoup
import pandas as pd
import requests
from get_mainpage import *
import time
import random

headers_pool = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:45.0) Gecko/20100101 Firefox/45.0"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"},
    {"User-Agent": "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko"},
    {"User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; Nexus 5 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"},
    {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"}
]


subpage = requests.get("https://european-digital-innovation-hubs.ec.europa.eu/edih-catalogue/4pdih")

def get_table_contents(link):
    """
    :param link:
    give the link to the subpage

    :return:
    returns a dataframe of the table
    :exception:
    returns a string 'no table'
    """



    names = []
    try:
        categories = soup.find("tr", {"class": "ecl-table__row"})
        for th in categories:
            col_name = th.text.strip()
            if col_name != '':
                names.append(col_name)


        table_list = []
        for row in soup.table.find_all("tr", {"class": "ecl-table__row"})[1:]:
            individual_list = []
            for td in row:
                cont = td.text.strip()
                if cont != '':
                    individual_list.append(cont)
            table_list.append(individual_list)


        data  = table_list
        df = pd.DataFrame(data, columns=names)
        df.insert(0, 'ID', soup.find("h1", {"class": "ecl-page-header__title"}).text)

        return df
    except (Exception, ):
        return "no table found"

# clients = get_clients("clients.xlsx")


soup = BeautifulSoup(subpage.text, 'html.parser')

print(get_table_contents(soup))


# for client in clients:
#     headers = random.choice(headers_pool)
#     # sub = requests.get(f"https://european-digital-innovation-hubs.ec.europa.eu/edih-catalogue/{client}", headers=headers)
#     print(sub.status_code)
#     if sub.status_code == 429:
#         print("Rate limit exceeded. Retrying with a new header...")
#         time.sleep(1)  # Optional: Add a small delay before retrying
#         continue  # Skip to the next iteration
#     soup = BeautifulSoup(sub.text, 'html.parser')
#     print(client)
#     print(get_table_contents(soup))