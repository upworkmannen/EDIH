from bs4 import BeautifulSoup
import pandas as pd
import requests
import openpyxl



def download_list():
    """
    uses link and bs4 to download xlsx with main page info

    :return:
    main page .xlsx file with the main page data
    """

    output_file = "clients.xlsx"
    mainpage = requests.get("https://european-digital-innovation-hubs.ec.europa.eu/edih-catalogue/")
    soup = BeautifulSoup(mainpage.text, "html.parser")
    link = soup.find('a', string='Download Data')['href']
    response = requests.get(link)
    response.raise_for_status()


    try:
        with open(output_file, "wb") as file:
            file.write(response.content)
        print(f"File successfully downloaded and saved as '{output_file}'.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading the file: {e}")


def get_clients_links():
    """
    :param client_list:
    This is the .xlsx file with the main page data

    :return:
    returns a list of client links, for use in scraping individual pages
    """
    links = []
    mainpage = requests.get("https://european-digital-innovation-hubs.ec.europa.eu/edih-catalogue/")
    soup = BeautifulSoup(mainpage.text, "html.parser")
    page_count = soup.find('li', {"class": "ecl-pagination__item ecl-pagination__item--last"})


    for i in range(int(page_count.text)):
        mainpage = requests.get(f"https://european-digital-innovation-hubs.ec.europa.eu/edih-catalogue?page={i}")
        soup = BeautifulSoup(mainpage.text, "html.parser")
        links_raw = soup.find_all('td', {"class":"views-field ecl-table__cell views-field-title"})
        links_temp = [link.find('a')['href'] for link in links_raw]
        links.extend(links_temp)
    return links

