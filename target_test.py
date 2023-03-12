import requests
import random
# import json
from bs4 import BeautifulSoup

URLs = [
    'https://www.target.com/p/rxbar-chocolate-peanut-butter-nutrition-bars-18-3oz-10pk/-/A-53168635',
    'https://www.target.com/p/rxbar-chocolate-sea-salt-protein-bar-1-83oz/-/A-52051382',
    'https://www.target.com/p/rxbar-peanut-butter-protein-bar-1-83oz/-/A-52051456',
    'https://www.target.com/p/rxbar-chocolate-sea-salt-protein-bars-10ct/-/A-53142575',
    'https://www.target.com/p/rxbar-vanilla-almond-7-32oz-4ct/-/A-79295680',
    'https://www.target.com/p/rxbar-chocolate-sea-salt-protein-bars-4ct/-/A-52051497',
    'https://www.target.com/p/rxbar-peanut-butter-protein-bars-4ct/-/A-52051566',
    'https://www.target.com/p/rxbar-chocolate-peanut-butter-nutrition-bars-18-3oz-10pk/-/A-53168635'
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
    page = requests.get(URL, headers=headers_list[random_header])

    soup = BeautifulSoup(page.content, 'lxml')

    title_box = soup.find('div', {'id': "pageBodyContainer"})
    title = title_box.find('h1')

    prices = soup.find('span', {'class': "dUPDAJ"})

    pattern = "JSON.parse"
    scripts = soup.find_all('script')
    scriptData = str(scripts[len(scripts) - 2]).split('\n')

    for line in scriptData:
        if '__TGT_DATA__' in line:
            prod_data = line[18:].replace('\\', '')
    
    prod_data = prod_data[prod_data.find("current_retail"):]
    prod_amount = prod_data[prod_data.find(":")+1:prod_data.find(",")]

    title = title.text.strip()
    size = 1
    if title.find("10pk") > 0:
        size = 10
    elif title.find('10ct') > 0:
        size = 10
    elif title.find('4ct') > 0:
        size = 4
    
    pricing_data.append([title, size, prod_amount])

print(pricing_data)