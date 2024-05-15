import time
import requests
from tqdm import tqdm
from fake_useragent import UserAgent

# Список адресов из файла
with open('wallet.txt', 'r') as f:
    addresses = [line.strip() for line in f]

headers = {
    'accept': '*/*',
    'accept-language': 'en-GB,en;q=0.9',
    'origin': 'https://scroll.io',
    'priority': 'u=1, i',
    'referer': 'https://scroll.io/',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': UserAgent().random,
}
total_point = 0

for address in tqdm(addresses, ncols=70):
    params = {
        'walletAddress': address.lower(),
    }
    try:
        attempt = 0
        point = 0
        while attempt < 3 and point == 0:
            response = requests.get('https://kx58j6x5me.execute-api.us-east-1.amazonaws.com/scroll/bridge-balances', params=params, headers=headers)
            for str in response.json():
                if str['points']:
                    point += int(str['points'])
                    total_point += int(str['points'])
                else:
                    time.sleep(3)
                    attempt += 1
        with open('stats.txt', 'a') as output:
            print(f"{address}: {point}", file=output)
    except:
        pass
    time.sleep(2)

print(f'{total_point} всего поинтов')