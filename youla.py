#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
import os

def get_html(url):
    r = requests.get(url)
    return r.text
    

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)

def write_csv(data):
    with open('youla.csv', 'a') as f:
        writer= csv.writer(f)
        writer.writerow((data['title'],data['price'],data['url'],data['img']))

def get_pages_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('ul', class_='product_list').find_all('li', class_='product_item')
    for ad in ads:
        try:
            title = ad.find('div', class_='product_item__title').text.strip()
        except:
            title = ''
        try:
            url = 'https://youla.ru' + ad.find('a').get('href')
        except:
            url = ''
        try:
            price = ad.find('div', class_='product_item__description ').text.strip()
        except:
            price = ''
        try:
            img = ad.find('div', class_='product_item__head').find('div', class_='product_item__image').find('img').get('src')
        except:
            img = ''                  
        try:
            data = {'title': title,'price': price,'url': url,'img': img}
            #print(data)
            write_csv(data)
        except:
            print('eror')




def main():
    url = 'https://youla.ru/all/uslugi/remont-stroitelstvo?q=демонтаж'
    base_url = 'https://youla.ru/all/uslugi/remont-stroitelstvo?'
    query_part = '&q=демонтаж'
    url_gen = base_url + query_part
    print(url_gen)
    html = get_html(url_gen)
    get_pages_data(html) 
if __name__ == '__main__':
    main()