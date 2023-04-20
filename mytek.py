import requests
from bs4 import BeautifulSoup
import os


script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "data.txt")



category=input("select category like \"informatique/ordinateurs-portables.html\"")
url = f"https://www.mytek.tn/informatique/{category}"
response = requests.get(url)
soup = BeautifulSoup(response.content, "lxml")




#get the number of subpages in this category
def page_number():
    pagination = soup.find('ul', {'class':'items pages-items'})
    if pagination:
        last_page_link = pagination.find_all('a')[-2]['href']
        return int(last_page_link.split('=')[-1])
    else: return 1






#get the products of subpages
def get_product(page):
    page_url = url +"?p="+str(page)
    page_response = requests.get(page_url)
    soup = BeautifulSoup(page_response.content, 'lxml')
    return soup.find_all('li', {'class': 'item product product-item'})







def main_mytek():
    for page in range(1, page_number()+1):
        for container in get_product(page):
            name = container.find('a', {'class': 'product-item-link'}).text.strip()
            price = container.find('div', {'class': 'price-box price-final_price'}).text.strip()
            image_link = container.find('img')['src']
            ref=soup.find('div', {"class":"skuDesktop"}).text.strip()
            description = container.find('p').text.strip()
            with open(file_path, "a", encoding="utf-8") as file:
                file.write(f"name: {name}\nprice: {price}\nimage: {image_link}\nref: {ref}\ndescriping:{description}\n\n")
main_mytek()