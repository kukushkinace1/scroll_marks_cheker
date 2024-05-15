import time
import requests
from tqdm import tqdm

# Список адресов из файла
with open('wallet.txt', 'r') as f:
    addresses = [line.strip() for line in f]

total_point = 0

for address in tqdm(addresses, ncols=70):
    params = {
        'walletAddress': address.lower(),
    }
    try:
        attempt = 0
        point = 0
        while attempt < 3 and point == 0:
            response = requests.get('https://kx58j6x5me.execute-api.us-east-1.amazonaws.com/scroll/bridge-balances', params=params)
            for str in response.json():
                if str['points']:
                     attempt += 1
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
