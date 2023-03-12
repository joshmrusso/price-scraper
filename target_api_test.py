import requests

s = requests.session()
s.get('https://www.target.com')

key = s.cookies['visitorId']
location = s.cookies['GuestLocation'].split('|')[0]

store_id = requests.get('https://redsky.target.com/v3/stores/nearby/%s?key=%s&limit=1&within=100&unit=mile' %(location, key)).json()
store_id = store_id[0]['locations'][0]['location_id']

product_id = '52190951'
url = 'https://redsky.target.com/web/pdp_location/v1/tcin/%s' %product_id
payload = {
    'pricing_store_id': store_id,
    'key': key
}

jsonData = requests.get(url, params=payload)
print(jsonData)