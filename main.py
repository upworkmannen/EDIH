from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
import random
import time
from get_mainpage import *

url = "https://european-digital-innovation-hubs.ec.europa.eu/edih-catalogue/"

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





# Get list of all base links
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
main_page_data = pd.read_excel(f"{__location__}\\clients.xlsx")
name_column = main_page_data["EDIH Name"]
url_list = [f"{url}{name}" for name in name_column] # Contains a list of all url's to scrape
test_url = "https://european-digital-innovation-hubs.ec.europa.eu/edih-catalogue/4PDIH"


### Initialize requests and soup
response = requests.get(test_url)
soup = BeautifulSoup(response.content, 'html.parser')


# Function to extract the company name (ID)
def get_company_name(soup):
    company_name = soup.find('h1', class_='ecl-page-header__title')
    if company_name:
        return company_name.get_text(strip=True)
    return 'Not found'

# Function to extract the EDIH Title
def get_title(soup):
    EDIH_Title = soup.find('div', class_='field field--name-field-title field--type-string field--label-hidden field__item')
    if EDIH_Title:
        return {'EDIH Title': EDIH_Title.get_text(strip=True)}
    return {'EDIH Title': 'Not found'}

# Function to extract description
def get_description(soup):
    description = soup.find('div', class_='ecl')
    if description:
        return {'Description': description.get_text(strip=True)}
    return {'Description': 'Not found'}

# Function to extract contact info for a given contact type and return it as a dictionary
def extract_contact_info(soup, contact_type, contact_label):
    contact_info = {
        'contact_type': contact_label,
        'name': soup.find('div', class_=f'field--name-field-{contact_type}-contact-name').get_text(strip=True),
        'email': soup.find('div', class_=f'field--name-field-{contact_type}-contact-email').get_text(strip=True)
    }
    if contact_type == 'co':
        contact_info['phone'] = soup.find('div', class_='field--name-field-co-contact-phone').get_text(strip=True)
    return contact_info

# Function to extract coordinator details (address, business name, legal name, department)
def extract_coordinator_info(soup):
    address = soup.find('div', class_='field--name-field-co-location').get_text(strip=True)
    business_name = soup.find('div', class_='field--name-field-co-business-name').get_text(strip=True)
    legal_name = soup.find('div', class_='field--name-field-co-legal-name').get_text(strip=True)
    department = soup.find('div', class_='field--name-field-co-department').get_text(strip=True)
    
    return {
        'contact_type': 'Coordinator information',
        'address': address,
        'business_name': business_name,
        'legal_name': legal_name,
        'department': department
    }

# Function to extract all contact information
def extract_all_contact_info(soup):
    contacts = [extract_contact_info(soup, 'contractual', 'Contractual contact information'),
                extract_contact_info(soup, 'co', 'Operational contact information'), extract_coordinator_info(soup)]
    
    # Add coordinator details to the list of contacts

    return contacts

# Function to combine all extracted data into one single pandas DataFrame
def extract_all_data(soup):
    # Extract Title and Description
    title_data = get_title(soup)
    description_data = get_description(soup)
    
    # Extract contact information
    contact_data = extract_all_contact_info(soup)
    
    # Combine everything into a single dictionary (including title and description)
    all_data = [title_data, description_data] + contact_data
    
    # Convert the combined data into a pandas DataFrame
    all_data_df = pd.DataFrame(all_data)
    
    # Extract the company name (ID)
    company_name = get_company_name(soup)
    
    # Add the 'ID' column with the company name to the DataFrame
    all_data_df['ID'] = company_name
    
    # Reorder columns so 'ID' comes first
    all_data_df = all_data_df[['ID'] + [col for col in all_data_df.columns if col != 'ID']]
    
    return pd.DataFrame(all_data_df)

################################################



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


soup1 = BeautifulSoup(subpage.text, 'html.parser')

# Merge and export DataFrames
df1 = extract_all_data(soup)
df2 = get_table_contents(soup1)

merged_df = pd.concat([df1, df2], axis=0, ignore_index=True)
merged_df.to_csv('merged_data_EDIH.csv', index=False)


soup = BeautifulSoup(subpage.text, 'html.parser')

clients = get_clients_links()

for client in clients:
    print(client)
    headers = random.choice(headers_pool)
    sub = requests.get(f"https://european-digital-innovation-hubs.ec.europa.eu{client}", headers=headers)
    print(sub.status_code)
    if sub.status_code == 429:
        print("Rate limit exceeded. Retrying with a new header...")
        time.sleep(1)  # Optional: Add a small delay before retrying
        continue  # Skip to the next iteration
    soup = BeautifulSoup(sub.text, 'html.parser')
    print(get_table_contents(soup))
