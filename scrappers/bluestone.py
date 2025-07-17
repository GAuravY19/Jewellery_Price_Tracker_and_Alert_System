from playwright.sync_api import sync_playwright
import time

PRODUCTS = ['Rings', 'Earrings', 'Solitaires', 'Nosepins', 'Bracelets', 'Bangles',
            'Necklace', 'Pendants', 'Mangalsutras']

PW = sync_playwright().start()
BROWSER = PW.chromium.launch(headless=False)

PAGE = BROWSER.new_page()
PAGE.goto("https://www.bluestone.com/")
PAGE.wait_for_load_state()

PAGE.locator('.deny-btn').click()
PAGE.locator('xpath=//input[@id="search_query_top_elastic_search"]').fill(PRODUCTS[0])

time.sleep(3)

PAGE.locator('.button').click()

time.sleep(5)

total_designs = PAGE.locator("xpath =//span[@class='total-designs']").text_content().split(" ")[0]
total_designs = int(total_designs)
print(total_designs)

prod = []

i = 1
while i != 50:
    PAGE.mouse.wheel(0,200)
    print(i)
    i += 1

time.sleep(3)

ui_elements = PAGE.locator("#product_list_ui li").all()

count = len(ui_elements)

print('Total products found : ', count)
for i in ui_elements:
    selling_price = i.get_attribute("data-sellingprice")
    prod_name = i.get_attribute('data-pname')
    print(selling_price)
    break

print('Done All Jewellery')

time.sleep(180)
BROWSER.close()
