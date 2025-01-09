from bs4 import BeautifulSoup
import pandas as pd
import request

url = "https://european-digital-innovation-hubs.ec.europa.eu/edih-catalogue/"

# Main page data file:
main_page_data = pd.read_xls("export-edihs.xls")

name_column = main_page_data["EDIH Name"]

def get_links(name_column):
  for i in len(name_column):
    new_list = url.append(i)
    return new_list


