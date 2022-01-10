# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
import csv, re


if __name__ == '__main__':
    link=[]
    pageNum=0

    while True:
        pageNum+=1
        try:
            fHand = urllib.request.urlopen('http://books.toscrape.com/catalogue/page-'+str(pageNum)+'.html').read()
            soup=BeautifulSoup(fHand, 'html.parser')
            for p in soup.find_all('article'):
                link.append(p.find('a').get('href'))
        except:
            break

#     make csv file
    with open('output.csv', 'w', encoding='UTF8', newline='') as fi:
        f = csv.writer(fi)
        f.writerow(['title', 'upc', 'type', 'price', 'availability', 'reviews', 'description'])
        for l in link:
            try:
                linkHand = urllib.request.urlopen('http://books.toscrape.com/catalogue/'+str(l)).read()
                iSoup=BeautifulSoup(linkHand,'html.parser').find('article')
                title=iSoup.find('h1').string
                price=iSoup.find('p',{'class': 'price_color'}).string
                description=iSoup.find(id='product_description').find_next_sibling('p').string
                inf=iSoup.find('table')
                upc=inf.find('th', string="UPC").find_next_sibling('td').string
                type=inf.find('th', string="Product Type").find_next_sibling('td').string
                reviews=inf.find('th', string="Number of reviews").find_next_sibling('td').string
                availability=re.search(r'\d+',inf.find('th', string="Availability").find_next_sibling('td').string).group()
                f.writerow([title, upc, type, price, availability, reviews, description])
            except:
                print("Cannot process", l)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
