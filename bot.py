from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from logger import log

# ✅ FIX IMPORTANT → garder Chrome ouvert
def start_browser(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    log("Navigateur lancé")
    return driver

def select_size(driver, size):
    try:
        btn = driver.find_element(By.XPATH, f"//button[contains(text(),'{size}')]")
        btn.click()
        log(f"Taille {size} sélectionnée")
        return True
    except:
        log(f"Taille {size} indisponible")
        return False

def click_buy(driver):
    try:
        btn = driver.find_element(By.XPATH, "//button[contains(text(),'Acheter')]")
        btn.click()
        log("Click sur acheter")
        return True
    except:
        log("Bouton acheter non trouvé")
        return False

def run_task(url, sizes, retry, delay):
    driver = start_browser(url)
    time.sleep(5)

    for size in sizes:
        if select_size(driver, size):
            break

    for i in range(retry):
        if click_buy(driver):
            log("Tentative d'achat envoyée")
            break
        time.sleep(delay)

    # ✅ IMPORTANT → message final
    log("Bot terminé — navigateur reste ouvert")