from bs4 import BeautifulSoup
import pandas as pd
import requests
import openpyxl


link = requests.get( "https://european-digital-innovation-hubs.ec.europa.eu/edih-catalogue/4pdih/")


def download_list():
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
    df = pd.read_excel(f"{client_list}", index_col=None)
    df = df["EDIH Name"].tolist()
    print(df)



get_clients('clients.xlsx')

download_list()

