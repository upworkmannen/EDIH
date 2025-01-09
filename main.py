from bs4 import BeautifulSoup
import pandas as pd
import requests
from get_mainpage import *

subpage = requests.get("https://european-digital-innovation-hubs.ec.europa.eu/edih-catalogue/addsmart")

def get_table_contents(link):
    """
    :param link:
    give the link to the subpage

    :return:
    returns a dataframe of the table
    :exception:
    returns a string 'no table'
    """
    soup = BeautifulSoup(subpage.text, 'html.parser')



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
        return df
    except (Exception, ):
        return "no table found"

clients = get_clients("clients.xlsx")

print(get_table_contents(subpage))


# for client in clients:
#     sub = requests.get(f"https://european-digital-innovation-hubs.ec.europa.eu/edih-catalogue/{client}")
#     print(get_table_contents(sub))