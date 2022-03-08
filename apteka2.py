import aiohttp
import asyncio
import time

start_time = time.time()

l = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', 'a-z', '0-9']


async def get_apteka(session, li):
    async with session.get(f'https://apteka.ru/regions/medicines-list/?char={li}') as resp:
        apteka = await resp.text()
        print(li)
        return apteka


async def main():

    async with aiohttp.ClientSession() as session:

        tasks = []
        for li in l:
            tasks.append(asyncio.ensure_future(get_apteka(session, li)))
        respo = await asyncio.gather(*tasks)

while True:
    try:
        asyncio.run(main())
    except:
        print('Restarting')
print("--- %s seconds ---" % (time.time() - start_time))