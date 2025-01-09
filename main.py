from bs4 import BeautifulSoup
import pandas as pd
import requests
from get_mainpage import *

subpage = requests.get("https://european-digital-innovation-hubs.ec.europa.eu/edih-catalogue/addsmart")

### Extract title and print
def get_title():
    EDIH_Title = soup.find('div', class_='field field--name-field-title field--type-string field--label-hidden field__item')
    if EDIH_Title:
        return {'EDIH Title': EDIH_Title.get_text(strip=True)}
    return {'EDIH Title': 'Not found'}
print(get_title())

### Extract description and return it in a dictionary
def get_description():
    description = soup.find('div', class_='ecl')
    if description:
        return {'Description': description.get_text(strip=True)}
    return {'Description': 'Not found'}
print(get_description())

### Extract coordinator information
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
    contacts = [
        extract_contact_info(soup, 'contractual', 'Contractual contact information'),
        extract_contact_info(soup, 'co', 'Operational contact information')
    ]
    
    # Add coordinator details to the list of contacts
    contacts.append(extract_coordinator_info(soup))
    
    return contacts

print(extract_all_contact_info(soup))

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
