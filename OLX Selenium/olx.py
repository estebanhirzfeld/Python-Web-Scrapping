import json

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome('./chromedriver.exe')

driver.get('https://www.olx.com.ar/autos_c378')


products_data = []
id = 0

for i in range(3):

    try:
        # Esperamos a que el boton se encuentre disponible a traves de una espera por eventos
        # Espero un maximo de 10 segundos, hasta que se encuentre el boton dentro del DOM
        load_more_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[@data-aut-id="btnLoadMore"]'))
        )
        # le doy click al boton que espere
        load_more_btn.click()
        # 20 anuncios de carga inicial, y luego 20 anuncios por cada click que he dado
        # Espero hasta 10 segundos a que toda la informacion del ultimo anuncio este cargada
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//li[@data-aut-id="itemBox"]//span[@data-aut-id="itemPrice"]'))
        )
        # Luego de que se hallan todos los elementos cargados, seguimos la ejecucion
    except Exception as e:
        print(e)
        # si hay algun error, rompo el lazo. No me complico.
        break

products = driver.find_elements(By.XPATH, '//li[@data-aut-id="itemBox"]')

for product in products:

    product_price = product.find_element(
        By.XPATH, './/span[@data-aut-id="itemPrice"]').text

    product_name = product.find_element(
        By.XPATH, './/span[@data-aut-id="itemTitle"]').text

    id += 1

    products_data.append(
        {
            'name': product_name,
            'price': product_price,
            'id': id
        }
    )

out_file = open('products.json', 'w')
json.dump(products_data, out_file)
out_file.close()

print('Products saved in products.json ;)')
