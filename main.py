from bs4 import BeautifulSoup
import pandas as pd
import requests

url = "https://european-digital-innovation-hubs.ec.europa.eu/edih-catalogue/"

# Main page data file:
main_page_data = pd.read_excel("/Users/gui/Desktop/Upwork/EDIH/export-edihs.xls")
name_column = main_page_data["EDIH Name"]

url_list = [f"{url}{name}" for name in name_column]

print(url_list)


