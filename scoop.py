import requests
import urllib3
from bs4 import BeautifulSoup
import os
urllib3.disable_warnings()




script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "data.txt")



category=input("select category like \"90-composants-pc\"")
url = f'https://www.scoopgaming.com.tn/{category}'
response = requests.get(url, verify=False)
soup = BeautifulSoup(response.content, 'lxml')



#get the number of subpages in this category
def page_number():
    pagination = soup.find('div', {'class':'pagination'})
    if pagination:
        page_links = pagination.find_all('a')
        return int(page_links[-2].text)
    else: return 1




#get the products of subpages
def get_product(page):
    page_url = f'{url}/page-{page}'
    page_response = requests.get(page_url,verify=False)
    page_soup = BeautifulSoup(page_response.content, 'lxml')
    return page_soup.find_all('li', {'class': 'ajax_block_product'})




def main_scoop():

    for page in range(1, page_number()+1):
        for product in get_product(page):
            name = product.find('h5').text.strip()
            price = product.find('span', {'class': 'price'}).text.strip()
            image_link = product.find('img').text.strip()
            ref= product.find('span', {'class': 'ref-listeprod'}).text.strip()
            description = product.find("p",{"class":"product-desc"}).text.strip()
            with open(file_path, "a", encoding="utf-8") as file:
                file.write(f"name: {name}\nprice: {price}\nimage: {image_link}\nref: {ref}\ndescriping:{description}\n")


