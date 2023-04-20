import requests
from bs4 import BeautifulSoup
import os



script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "data.txt")




category=input("select category like \"703-pc-portable-pro\"")
url = f"https://www.tunisianet.com.tn/{category}"
response = requests.get(url)
soup = BeautifulSoup(response.content, "lxml")




#get the number of subpages in this category
def page_number():
    pagination = soup.find('ul', {'class':'page-list clearfix'})
    if pagination:
        page_links = pagination.find_all('a')
        return int(page_links[-2].text)
    else: return 1



#get the products of subpages
def get_product(page):
    page_url = f"{url}?page={page}"
    page_response = requests.get(page_url)
    page_soup = BeautifulSoup(page_response.content, 'lxml')
    return page_soup.find_all("div", {"class":"thumbnail-container text-xs-center"})





def main_tunisianet():
    for page in range(1, page_number()+1):
        for laptop in get_product(page):
            name = laptop.find("h2",{"class":"h3 product-title"}).text.strip()
            price = laptop.find("span", class_="price").text.strip()
            image_link = laptop.find("img", {"class":"center-block img-responsive"})['src']
            ref=soup.find('span', {"class":"product-reference"}).text.strip()
            description = laptop.find("p").text.strip()
            with open(file_path, "a", encoding="utf-8") as file:
                file.write(f"name: {name}\nprice: {price}\nimage: {image_link}\nref: {ref}\ndescriping:{description}\n\n")

main_tunisianet()