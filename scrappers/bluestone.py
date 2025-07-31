from playwright.async_api import async_playwright
import time
import asyncio
from datetime import datetime
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(host=os.getenv('host'),
                        dbname = os.getenv('dbname_b'),
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


PRODUCTS = ['Rings', 'Earrings', 'Solitaires', 'Nosepins', 'Bracelets', 'Bangles',
            'Necklace', 'Pendants', 'Mangalsutras']

def id_generator(prod_name, prod_count):
    data = {'Rings': 'RIB',
            'Earrings': 'EAB',
            'Solitaires': 'SOB',
            'Nosepins': 'NOB',
            'Bracelets': 'BRB',
            'Bangles': 'BAB',
            'Necklace': 'NEB',
            'Pendants': 'PEB',
            'Mangalsutras': 'MAB'}

    id = data[prod_name]+str(prod_count)

    return id


async def scrape_bluestone(cate:str) -> None:
    async with async_playwright() as PW:
        BROWSER = await PW.chromium.launch(headless=False)

        PAGE = await BROWSER.new_page()
        await PAGE.goto("https://www.bluestone.com/", timeout=90000)

        await PAGE.locator('.deny-btn').click()
        await PAGE.locator('xpath=//input[@id="search_query_top_elastic_search"]').fill(cate)

        time.sleep(3)

        await PAGE.locator('.button').click()

        time.sleep(5)

        total_designs_text = await PAGE.locator("xpath =//span[@class='total-designs']").text_content()
        total_designs = total_designs_text.split(" ")[0]
        total_designs = int(total_designs)

        i = 1
        while i != 1:
            await PAGE.mouse.wheel(0,100)
            time.sleep(0.5)
            i += 1

        time.sleep(3)

        ui_elements = await PAGE.locator("#product_list_ui li").all()

        for i in ui_elements:
            selling_price = await i.get_attribute("data-sellingprice")
            prod_name = await i.get_attribute('data-pname')
            checks = await find_product(prod_name, cate)

            if checks is not None:
                print('Prod found')
                break

            else:
                cur.execute(f'SELECT COUNT(*) FROM {cate.lower()}')
                count = cur.fetchone()[0]+1
                id = id_generator(cate, count)
                cur.execute(f'INSERT INTO {cate.lower()} VALUES {id, prod_name, selling_price}')
                conn.commit()
                break


        print('Done All Jewellery')

        time.sleep(3)
        await BROWSER.close()


if __name__ == "__main__":

    async def main():
        for i in PRODUCTS:
            await scrape_bluestone(i)
            break

    asyncio.run(main())
