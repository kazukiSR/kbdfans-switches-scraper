from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from time import sleep

service = Service("C:\Development\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://kbdfans.com/collections/switches")
action = ActionChains(driver)
sleep(5)

driver.find_element(By.CSS_SELECTOR, ".cc-popup-close").click()
switchList = {}
pageList = driver.find_elements(By.CSS_SELECTOR, ".pagination .page")
for i in range(len(pageList)):
    try:
        productList = driver.find_elements(By.CSS_SELECTOR, "#gf-products .product-block .product-block__title a")
        for n in range(len(productList)):
            action.key_down(Keys.CONTROL).click(productList[n]).key_up(Keys.CONTROL).perform()
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[1])
                try:
                    productNameElement = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "product-detail__title"))
                    )
                    productName = productNameElement.text
                    productPrice = driver.find_element(By.CLASS_NAME, "theme-money").text
                    specs = driver.find_elements(By.CSS_SELECTOR, "#tab1 ul li")
                    productSpecs = [spec.text for spec in specs]

                    switchList[n] = {
                        "name": productName,
                        "price": productPrice,
                        "specs": productSpecs,
                    }
                except:
                    continue
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
        if not (i == len(pageList) - 1):
            driver.find_element(By.CSS_SELECTOR, ".pagination .next a").click()
            sleep(1)
    except NoSuchElementException:
        continue
driver.quit()
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(switchList, f, ensure_ascii=False, indent=4)
