import requests
import random
import json
from bs4 import BeautifulSoup

URLs = [
    'https://www.kroger.com/p/rxbar-chocolate-sea-salt-protein-bars/0085777700430',
    'https://www.kroger.com/p/rxbar-peanut-butter-protein-bar/0085777700420',
    'https://www.kroger.com/p/rxbar-protein-bar-peanut-butter/0019390800504',
    'https://www.kroger.com/p/rxbar-chocolate-sea-salt-protein-bars/0085803000841',
    'https://www.kroger.com/p/rxbar-peanut-butter-chocolate-protein-bars/0085803000842',
    'https://www.kroger.com/p/rxbar-chocolate-sea-salt-protein-bar/0085777700423',
    'https://www.kroger.com/p/rxbar-peanut-butter-chocolate-protein-bar/0085777700468',
    'https://www.kroger.com/p/rxbar-vanilla-almond-protein-bar/0019390800178',
    'https://www.kroger.com/p/rxbar-chocolate-sea-salt-protein-bar/0085777700423'
]

# Header list for header rotation
headers_list = [
    {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
        "Accept-Encoding": "gzip, deflate", 
        "Accept-Language": "en-US,en;q=0.9", 
        "Upgrade-Insecure-Requests": "1", 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }, {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
        "Accept-Encoding": "gzip, deflate", 
        "Accept-Language": "en-US,en;q=0.9", 
        "Upgrade-Insecure-Requests": "1", 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69", 
    }, {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", 
        "Accept-Encoding": "gzip, deflate", 
        "Accept-Language": "en-US,en;q=0.5", 
        "Upgrade-Insecure-Requests": "1", 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0", 
    }, {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
        "Accept-Encoding": "gzip, deflate", 
        "Accept-Language": "en-US,en;q=0.9", 
        "Upgrade-Insecure-Requests": "1", 
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
]

pricing_data = []

for URL in URLs:

    random_header = random.randint(0, len(headers_list) - 1)

    isBlank = True
    while isBlank:
        page = requests.get(URL, headers=headers_list[random_header])
        soup = BeautifulSoup(page.content, 'lxml')

        scripts = soup.find_all('script')
        # scriptData = str(scripts[len(scripts) - 2]).split('\n')

        for scr in scripts:
            if str(scr).find("window.__INITIAL_STATE__") > 0:
                product_info = str(scr)
        product_start = product_info.find("\"price\":{\"displayTemplate\":")
        product_end = product_info.find("\"nutrition\":{\"allergens\"")
        title_start = product_info.find("\"customerFacingSize\":")
        title_end = product_info.find("\"dimensions\"")
        if product_start > 0 and product_end > 0:
            isBlank = False

    product_info = product_info.replace("\"", "'")
    product_info = product_info.replace("\\\\", "\\")
    product_info = product_info.replace("false", "False")
    product_info = product_info.replace("true", "True")
    product_dict = eval('{' + product_info[product_start:product_end-1] + '}')
    title_dict = eval('{' + product_info[title_start:title_end-1] + '}')
    title = title_dict['description']
    size = title_dict['customerFacingSize']
    if str(product_dict['price']).find('promo') > 0:
        price = product_dict['price']['storePrices']['promo']['unitPrice']
    else:
        price = product_dict['price']['storePrices']['regular']['unitPrice']
    pricing_data.append([title, size, price])

print(pricing_data)

