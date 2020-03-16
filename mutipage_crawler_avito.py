import requests
from bs4 import BeautifulSoup
import csv

# План:
# 1. Выяснить количество страниц
# 2. Сформировать список урлов на страницы выдачи
# 3. Собрать данные

def get_html(url):
    r = requests.get(url)
    return r.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    total_pages = soup.find('div', class_='pagination-root-2oCjZ').find_all('span', class_='pagination-item-1WyVp')[-2].text.strip()
    return int(total_pages)

def write_csv(data):
    with open('avito.csv', 'a', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow((data['title'],
                         data['price'],
                         data['metro'],
                         data['url']) )

def get_page_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    ads = soup.find('div', class_='js-catalog_serp').find_all('div', class_='item_table')
    for ad in ads:
        name = ad.find('a', class_='snippet-link').text.strip()
        if 'htc' in name:
            try:
                url = 'https://www.avito.ru' + ad.find('a', class_='snippet-link').get('href')
            except:
                url = ''

            try:
                price = ad.find('span', class_ = 'snippet-price').text.strip()
            except:
                price = ''

            try:
                metro = ad.find('div', class_='item-address').text.strip()
            except:
                metro = ''

            # print(title)
            # print(url)
            # print(price)
            # print(metro)
            data = {'title': name,
                    'url': url,
                    'price': price,
                    'metro': metro}

            write_csv(data)
        else:
            continue


def main():
    url = 'https://www.avito.ru/moskva/telefony?q=htc&p=1'
    base_url = 'https://www.avito.ru/moskva/telefony?q=htc&'
    page_part = 'p='

    total_pages = get_total_pages(get_html(url))

    for i in range(1, total_pages+1):
        url_gen = base_url + page_part + str(i)
        # print(url_gen)
        html = get_html(url_gen)
        get_page_data(html)

if __name__ == '__main__':
    main()