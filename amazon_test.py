import requests
import random
# import json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def get_soup_retry(url):
    ua = UserAgent()
    uag_random = ua.random

    header = {
        'User-Agent': uag_random,
        'Accept-Language': 'en-US,en;q=0.9'
    }
    isCaptcha = True
    while isCaptcha:
        page = requests.get(url, headers=header)
        assert page.status_code == 200
        soup = BeautifulSoup(page.content, 'lxml')
        if 'captcha' in str(soup):
            uag_random = ua.random
            print(f'\rBot has been detected... retrying... use new identity: {uag_random} ', end='', flush=True)
        else:
            print('Bot bypassed')
            return soup

URLs = [
    'https://www.amazon.com/RXBAR-Whole-Protein-Chocolate-1-83oz/dp/B07CWXX69K',
    'https://www.amazon.com/RXBAR-Protein-Peanut-Butter-1-83oz/dp/B07D2RHJ4D',
    'https://www.amazon.com/RXBAR-Protein-Peanut-Butter-Chocolate/dp/B07D1SNG9K',
    'https://www.amazon.com/RXBAR-Whole-Protein-Chocolate-Ounce/dp/B07D1T6SN9',
    'https://www.amazon.com/RXBAR-Vanilla-Almond-Protein-Snack/dp/B089L67BMY',
    'https://www.amazon.com/RXBAR-Whole-Protein-Chocolate-Boxes/dp/B01MRU7EWY',
    'https://www.amazon.com/RXBAR-Banana-Chocolate-Protein-Breakfast/dp/B07WRMH1ZB',
    'https://www.amazon.com/RXBAR-Whole-Protein-Chocolate-Ounce/dp/B07D1T6SN9'
]

pricing_data = []

for URL in URLs:

    soup = get_soup_retry(URL)
    try:
        title = soup.find('span', {'id': "productTitle"}).text.strip()
    except:
        print("Error with title")
        print(soup.contents)
        continue
    
    try:
        price_box = soup.find('div', {'id': "variation_size_name"})
        size_options = price_box.find_all('li')
    except:
        print("Error with price")

    for size_option in size_options:
        try:
            size = size_option.find('p', {'class': 'a-size-base'}).text.strip()
            price = size_option.find('p', {'class': "twisterSwatchPrice"}).text.strip()
            item_price = [title, size, price]
            pricing_data.append(item_price)
        except:
            print("Error with loop")

print(pricing_data)