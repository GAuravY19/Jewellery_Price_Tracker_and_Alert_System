from playwright.async_api import async_playwright
import time
import asyncio
from datetime import datetime
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(host=os.getenv('host'),
                        dbname = os.getenv('dbname_c'),
                        user=os.getenv('user'),
                        password = os.getenv('password'),
                        port=os.getenv('port'))

cur = conn.cursor()

async def find_product(prod_name,cate:str, cur=cur):
    cur.execute(f'''SELECT id
                    FROM {cate.lower()}
                    WHERE product_name=%s''', (str(prod_name),))
    check = cur.fetchone()

    return check

def id_generator(prod_name, prod_count):
    data = {'Rings': 'RIC',
            'Earrings': 'EAC',
            'Solitaires': 'SOC',
            'Nosepins': 'NOC',
            'Bracelets': 'BRC',
            'Bangles': 'BAC',
            'Necklace': 'NEC',
            'Pendants': 'PEC',
            'Mangalsutras': 'MAC'}

    id = data[prod_name]+str(prod_count)

    return id

PRODUCTS = ['Rings', 'Earrings', 'Solitaires', 'Nosepins', 'Bracelets', 'Bangles',
            'Necklace', 'Pendants', 'Mangalsutras']

async def scrape_caratlane(cate:str) -> None:
    async with async_playwright() as PW:
        BROWSER = await PW.chromium.launch(headless=False)

        PAGE = await BROWSER.new_page()
        await PAGE.goto("https://www.caratlane.com/", timeout=90000)

        await PAGE.locator('xpath=//div[contains(@class, "input-wrapper")]//input').fill(PRODUCTS[0])
        time.sleep(2)
        await PAGE.locator('xpath=//div[contains(@class, "input-wrapper")]/span[contains(@class, "search-icon")]').click()
        time.sleep(2)

        total_prods_text = await PAGE.locator('xpath=//span[contains(@class, "count")]').text_content()
        total_prods = total_prods_text.strip().split(" ")[0]
        total_prods = int(total_prods)

        i = 0
        while i != 50:
        # while i != total_prods:
            await PAGE.mouse.wheel(0,120)
            time.sleep(0.5)
            i+=1

        time.sleep(3)

        div_elements = await PAGE.locator('.css-17erzg6.e1fkptg30').all()

        for i in div_elements:
            prod_name = await i.locator('.css-1447zhi a h3').text_content()
            prod_price_text = await i.locator('.css-1wget1y').text_content()
            prod_price = prod_price_text.split(" ")[0]
            checks = await find_product(prod_name, cate)

            if checks is not None:
                print('prod found')


            else:
                cur.execute(f'SELECT COUNT(*) FROM {cate.lower()}')
                count = cur.fetchone()[0] + 1
                id = id_generator(cate, count)
                cur.execute(f'INSERT INTO {cate.lower()} VALUES {id, prod_name, prod_price}')
                conn.commit()



        time.sleep(10)

        await BROWSER.close()


if __name__ == "__main__":

    async def main():
        for i in PRODUCTS:
            await scrape_caratlane(i)
            break

    asyncio.run(main())
