import json
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36')

driver = webdriver.Chrome('./chromedriver.exe', options=opts)

driver.get('https://www.google.com/travel/hotels/google%20places%20caesars%20palace%20hotel/entity/CgoI9_-8laqe8uR3EAE/reviews?q=google%20places%20caesars%20palace%20hotel&g2lb=2502548%2C2503771%2C2503781%2C4258168%2C4270442%2C4284970%2C4291517%2C4306835%2C4524133%2C4597339%2C4649665%2C4680677%2C4722900%2C4723331%2C4733969%2C4757164%2C4758493%2C4762561%2C4762570%2C4770372&hl=es-AR&gl=ar&cs=1&ssta=1&rp=EPf_vJWqnvLkdxD3_7yVqp7y5Hc4AkAASAHAAQI&ictx=1&sa=X&ved=0CAAQ5JsGahcKEwiQ-be0xsD3AhUAAAAAHQAAAAAQAg&utm_campaign=sharing&utm_medium=link&utm_source=htls&ts=CAESABpJCisSJzIlMHg4MGM4YzQzYzQ0Y2FlMDk1OjB4NzdjOWM4ZjJhMmFmM2ZmNxoAEhoSFAoHCOYPEAUYAxIHCOYPEAUYBBgBMgIQACoJCgU6A0FSUxoA')

scrollingScript = """ document.getElementsByClassName('')[0].scroll(0,10000)"""

sleep(3)

scrolls_counter = 0

while scrolls_counter < 3:
    scrolls_counter += 1
    driver.find_element(By.XPATH, '//body').send_keys(Keys.CONTROL+Keys.END)
    print("scrolled")
    sleep(random.uniform(2, 3))

reviews_links = driver.find_elements(
    By.XPATH, '//div//div[1]//span[1]//a[1][contains(@href,"maps/contrib")]')

links_to_scrap = []

scrapped_reviews = []

for link in reviews_links:
    links_to_scrap.append(link.get_attribute('href'))

for link in links_to_scrap:
    try:
        driver.get(link)

    except:
        print("cannot get link")

    try:
        review_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[text()="Opiniones"]')))
        review_btn.click()

    except:
        print("No Review button")

    scrolls_counter = 0
    while (scrolls_counter < 5):

        try:
            sleep(3)
            review_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@aria-label,'Contribuciones')]/div[@data-js-log-root][last()]")))
            review_container.send_keys(Keys.CONTROL+Keys.END)
            scrolls_counter += 1
            sleep(random.uniform(2, 3))
            print("scrolled container")
        except:
            print("cannot scroll container")

    try:
        reviews = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located(
            (By.XPATH, '//div[contains(@aria-label,"Contribuciones")]/div[@data-js-log-root][last()]/div[2]/div[@aria-label]')))
    except:
        print("The user has no reviews or the reviews are private")
        continue

    author = driver.find_element(
        By.XPATH, '//div[@aria-label="Foto de perfil"]/ancestor::div[1]/div/h1').text

    for review in reviews:

        url = driver.current_url
        place = review.find_element(
            By.XPATH, './/img[contains(@alt,"Foto de")]/ancestor::div[1]/ancestor::div[1]/div[2]/div[2]/div/div[1]/div[1]/span').text
        stars = review.find_element(
            By.XPATH, './/span[contains(@aria-label,"estrella")]').get_attribute("aria-label")

        try:
            review_text = review.find_element(
                By.XPATH, './/div[@id]/span[last()]').text
        except:
            review_text = "No review"

        scrapped_reviews.append(
            {
                "author": author,
                "place": place,
                "stars": stars,
                "review": review_text,
                "url": url
            }
        )

    sleep(5)
    print("next review")

out_file = open("reviews.json", "w")
json.dump(scrapped_reviews, out_file)
out_file.close()

print('Reviews saved in reviews.json ;)')
