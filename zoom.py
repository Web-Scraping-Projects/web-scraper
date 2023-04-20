import requests
from bs4 import BeautifulSoup
import os



script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "data.txt")
print(file_path)



category=input("select category like \"914-pc-portables\"")
url = f'https://www.zoom.com.tn/{category}'
print(url)
response = requests.get(url)
soup = BeautifulSoup(response.content, 'lxml')


#get the number of subpages in this category
def page_number():
    pagination = soup.find('ul', {'class':'pagination'})
    if pagination:
        page_links = pagination.find_all('a')
        return int(page_links[-2].text)
    else: return 1


#get the products of subpages
def get_product(page):
    page_url = f"{url}/page-{page}"
    page_response = requests.get(page_url)
    page_soup = BeautifulSoup(page_response.content, 'lxml')
    return page_soup.find_all("div", class_='product-container')

#get the content of products in this category
def get_product_content(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    name = soup.find('h1', itemprop="name").text.strip()
    price = soup.find('span', id="our_price_display").text.strip()
    image_link = soup.find('img',{'itemprop':"image"})['src']
    ref=soup.find('span', {"class":"editable"}).text.strip()
    description = soup.find('div',id="short_description_block").text.strip()
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(f"name: {name}\nprice: {price}\nimage: {image_link}\nref: {ref}\ndescriping:{description}\n\n")




def main_zoom():

    for page in range(1, page_number()+1):
        for product in get_product(page):
            link = product.find("a", {"class":"product_img_link"})['href']
            get_product_content(link)

main_zoom()