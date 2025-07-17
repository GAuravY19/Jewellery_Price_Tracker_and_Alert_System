from playwright.sync_api import sync_playwright
import time

PRODUCTS = ['Rings', 'Earrings', 'Solitaires', 'Nosepins', 'Bracelets', 'Bangles',
            'Necklace', 'Pendants', 'Mangalsutras']

PW = sync_playwright().start()
BROWSER = PW.chromium.launch(headless=False)

PAGE = BROWSER.new_page()
PAGE.goto("https://www.caratlane.com/")
PAGE.wait_for_load_state()

PAGE.locator('xpath=//div[contains(@class, "input-wrapper")]//input').fill(PRODUCTS[0])
time.sleep(2)
PAGE.locator('xpath=//div[contains(@class, "input-wrapper")]/span[contains(@class, "search-icon")]').click()
time.sleep(5)

total_prods = PAGE.locator('xpath=//span[contains(@class, "count")]').text_content().strip().split(" ")[0]
total_prods = int(total_prods)
print(total_prods)

i = 0
while i != 50:
# while i != total_prods:
    PAGE.mouse.wheel(0,120)
    print(i)
    i+=1

time.sleep(3)

div_elements = PAGE.locator('.css-17erzg6.e1fkptg30').all()
print("Total Products Found : ", len(div_elements))

for i in div_elements:
    # print(i.text_content())
    prod_name = i.locator('.css-1447zhi a h3').text_content()
    prod_price = i.locator('.css-1wget1y').text_content().split(" ")[0]
    print(prod_name)
    print(prod_price)
    print(" \n ")

time.sleep(10)

BROWSER.close()
