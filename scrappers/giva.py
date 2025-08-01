from playwright.async_api import async_playwright
import time
import asyncio
from datetime import datetime
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(host=os.getenv('host'),
                        dbname = os.getenv('dbname_g'),
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
    data = {'Rings': 'RIG',
            'Earrings': 'EAG',
            'Solitaires': 'SOG',
            'Nosepins': 'NOG',
            'Bracelets': 'BRG',
            'Bangles': 'BAG',
            'Necklace': 'NEG',
            'Pendants': 'PEG',
            'Mangalsutras': 'MAG'}

    id = data[prod_name]+str(prod_count)

    return id



PRODUCTS = ['Rings', 'Earrings', 'Solitaires', 'Nosepins', 'Bracelets', 'Bangles',
            'Necklace', 'Pendants', 'Mangalsutras']


async def scrape_giva(cate:str) -> None:
    async with async_playwright() as PW:
        BROWSER = await PW.chromium.launch(headless=False)

        PAGE = await BROWSER.new_page()
        await PAGE.goto(f"https://www.giva.co/search?options%5Bprefix%5D=last&page=1&q=rings", timeout=90000)
        time.sleep(10)

        all_items = await PAGE.locator('#retail-search-result li').all()
        print("collected items")

        for i in all_items:
            price_text = await i.locator(".custom-sale-price").text_content()
            price = price_text.strip()

            prod_name_text = await i.locator(".card__heading.h5").text_content()
            prod_name = prod_name_text.strip()

            checks = await find_product(prod_name, cate)

            if checks is not None:
                print("Prod found")
                pass

            else:
                cur.execute(f"SELECT COUNT(*) FROM {cate.lower()}")
                count = cur.fetchone()[0] + 1
                id = id_generator(PRODUCTS[0], count)
                cur.execute(f"INSERT INTO {cate.lower()} VALUES (%s, %s, %s)", (id, prod_name, price))
                conn.commit()

        print('Done all Jewellery')
        time.sleep(3)
        await BROWSER.close()


if __name__ == "__main__":

    async def main():
        await scrape_giva(PRODUCTS[0].lower())

    asyncio.run(main())
