from playwright.sync_api import sync_playwright
import time

pw = sync_playwright().start()
browser = pw.chromium.launch(headless=False)

page = browser.new_page()
page.goto("https://www.bluestone.com/")
page.wait_for_load_state()

page.locator('.deny-btn').click()

products = ['Rings', 'Earrings', 'Solitaires', 'Nosepins', 'Bracelets', 'Bangles',
            'Necklace', 'Pendants', 'Mangalsutras']

page.locator('xpath=//input[@id="search_query_top_elastic_search"]').fill(products[0])
time.sleep(3)
page.locator('.button').click()

time.sleep(5)
prod = []

print("INside page scrolling page")
i = 0
data_page = 0
while i != 50:
    page.mouse.wheel(0,90)
    i+=1
    time.sleep(1)
    try:
        list_of_prices = page.locator(f'xpath=//li[@data-position="{i}"]//h2[@class="p-name"]')
        print(list_of_prices.text_content())
    except:
        break

print("outside of page scrolling page")


# time.sleep(5)

# for i in list_of_prices:
#     prod = i.text_content()
# print(len(prod))
# print(list_of_prices.text_content())

print('Done All Jewellery')






























time.sleep(100)
browser.close()
