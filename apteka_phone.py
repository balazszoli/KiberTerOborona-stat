import aiohttp
import asyncio
import time
import csv
from time import sleep

start_time = time.time()


def nth_repl(s, sub, repl, n):
    find = s.find(sub)
    # If find is not -1 we have found at least one match for the substring
    i = find != -1
    # loop util we find the nth or we find no match
    while find != -1 and i != n:
        # find + 1 means we start searching from after the last match
        find = s.find(sub, find + 1)
        i += 1
    # If i is equal to n we found nth match so replace
    if i == n:
        return s[:find] + repl + s[find+len(sub):]
    return s

def format_phone_number(number):
    number = nth_repl(number, "-", " (", 1)
    number = nth_repl(number, "-", ") ", 1)
    return number


url = 'https://api.apteka.ru/Auth/Auth_Code?cityId=5e57803249af4c0001d64407'

req = {"phone": "+7 (985) 769-95-66", "u": "U"}

recipients = []
post_template = {"phone": "", "u": "U"}


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
                    recipients.append({"phone": f"{format_phone_number(i)}", "u": "U"})
            else:
                recipients.append({"phone": f"{format_phone_number(t)}", "u": "U"})

async def get_apteka(session, data):
    async with session.post(url, json=data) as resp:
        apteka = await resp.json()
        print(f'{data} > {apteka}')
        return apteka


async def main():

    async with aiohttp.ClientSession() as session:

        tasks = []
        for r in recipients:
            tasks.append(asyncio.ensure_future(get_apteka(session, r)))
        respo = await asyncio.gather(*tasks)


while True:
    try:
        asyncio.run(main())
    except Exception as e:
        print('Exception: {e}')
        
    sleep(480000 / 1000)
    
