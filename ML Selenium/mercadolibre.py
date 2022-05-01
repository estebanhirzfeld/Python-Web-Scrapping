import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36')

driver = webdriver.Chrome('./chromedriver.exe', options=opts)

driver.get('https://listado.mercadolibre.com.ec/repuestos-autos-camionetas-bujias')

cookies = driver.find_element_by_xpath('//button[text()="Entendido"]')
cookies.click()

preferences = driver.find_element_by_xpath('//button[@class="cookie-consent-snackbar__close"]')
preferences.click()

products = []
id = 0

while True:
    links_to_scrap = []

    products_links = driver.find_elements(
        By.XPATH, '//li[@class="ui-search-layout__item"]/div/div/div/a')

    print(len(products_links))

    for link in products_links:
        links_to_scrap.append(link.get_attribute('href'))

    last_driver = driver.current_url

    for link in links_to_scrap:
        try:
            driver.get(link)
            product_title = driver.find_element(By.XPATH, '//h1[@class="ui-pdp-title"]').text
            product_price = driver.find_element(By.XPATH, '//div[@class="ui-pdp-price__second-line"]//span[@class="andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact"]//span[@class="andes-visually-hidden"]').text
            
            products.append({
                'title': product_title,
                'price': product_price,
                'url': link,
                "id": id
            })
            id += 1
            
            # driver.back()
        except:
            driver.back()

    driver.get(last_driver)

    try:
        next_btn = driver.find_element(By.XPATH, '//span[text()="Siguiente"]')
        next_btn.click()
    except:
        print('Not more pages')
        break


out_file = open('products.json', 'w')
json.dump(products, out_file)
out_file.close()

print('Products saved in products.json ;)')





