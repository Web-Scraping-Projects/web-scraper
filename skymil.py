import requests
from bs4 import BeautifulSoup
import os



script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "data.txt")




category=input("select category like \"170-pc-portable-pro\"")
url = f'https://skymil-informatique.com/{category}'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')




#get the number of subpages in this category
def page_number():
    pagination = soup.find('ul', {'class':'page-list clearfix text-sm-center'})
    if pagination:
        page_links = pagination.find_all('a')
        return int(page_links[-2].text)
    else: return 1



#get the products of subpages
def get_product(page):
    page_url = f"{url}?page={page}"
    page_response = requests.get(page_url)
    page_soup = BeautifulSoup(page_response.content, 'lxml')
    return page_soup.find_all('div', {'class': 'product-description thumbnail-description'})

#get the content of products in this category
def get_product_content(link):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    name = soup.find('h1', {'class': 'product-name'}).text.strip() 
    price = soup.find('span', {'itemprop': 'price'}).text.strip() 
    if soup.find('span', {'itemprop': 'sku'}) is not None:ref=soup.find('span', {'itemprop': 'sku'}).text.strip() 
    else:ref=""
    description = soup.find('div', {'class': 'product-short-description'}).text.strip() 
    image_link = soup.find('img', {'class': 'js-qv-product-cover'})['src']
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(f"name: {name}\nprice: {price}\nimage: {image_link}\nref: {ref}\ndescriping:{description}\n")




def main_skymil():
    for page in range(1,page_number()+1):
        for product_div in get_product(page):
            url = product_div.find("a")['content']
            get_product_content(url)


