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


def get_clients(client_list):
    """
    :param client_list:
    This is the .xlsx file with the main page data

    :return:
    returns a list of client names, for use in scraping individual pages
    """
    df = pd.read_excel(f"{client_list}", index_col=None)
    df = df["EDIH Name"].tolist()
    print(df)


if __name__ == '__main__':
# call functions
get_clients('clients.xlsx')
download_list()

