import urllib.request
from pip._vendor import requests
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import pyperclip
import os
options = ChromeOptions()
options.add_argument("--headless=new")

class NaverLogin:
    def __init__(self):
        self.id = "sofsysbrand"
        self.pw = "Sofmd2755!"

    def load_page(self):
        
        service = ChromeService(executable_path=ChromeDriverManager().install())
        current_directory = os.path.dirname(os.path.abspath(__file__))
        
        prefs = {"download.default_directory": current_directory}
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=options, service=service)

        url = 'https://sell.smartstore.naver.com/#/home/about'

        driver.get(url)

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/ui-view[1]/div[2]/div[2]/div/div[1]/div[2]/button[1]"))) # login button
        driver.find_element(By.XPATH, "/html/body/ui-view[1]/div[2]/div[2]/div/div[1]/div[2]/button[1]").click()

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[1]/div/div/div[4]/div[1]/ul/li[2]/button'))) # login with naver button
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/div/div[4]/div[1]/ul/li[2]/button').click()

        driver.switch_to.window(driver.window_handles[-1])

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'id')))
        
        temp_user_input = pyperclip.paste()

        pyperclip.copy(self.id)
        driver.find_element(By.ID, 'id').click()    # id input
        time.sleep(3)
        ActionChains(driver).key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform()

        pyperclip.copy(temp_user_input)

        pyperclip.copy(self.pw)
        driver.find_element(By.ID, 'pw').click() # password input
        ActionChains(driver).key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform()
        
        driver.find_element(By.CLASS_NAME, "btn_login").click() # login button

        driver.switch_to.window(driver.window_handles[0]) # switch back to original window
        
        WebDriverWait(driver, 999).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/button'))) # wait till close button appears
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/button').click()

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="seller-lnb"]/div/div[1]/ul/li[14]/a'))) # click on statistics
        driver.find_element(By.XPATH, '//*[@id="seller-lnb"]/div/div[1]/ul/li[14]/a').click()

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ui-view[1]/div[3]/div/div[2]/div[1]/div/div[1]/ul/li[14]/ul/li[9]/a'))) # click on keyword tab
        driver.find_element(By.XPATH, '/html/body/ui-view[1]/div[3]/div/div[2]/div[1]/div/div[1]/ul/li[14]/ul/li[9]/a').click()
        
        hover_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="seller-content"]/ui-view/div/div/div[2]/div[3]/div/div/div/div/div[3]/div[2]/div/div/div[2]')))
        
        action = ActionChains(driver)
        action.click(hover_element).perform()
        for i in range(0, 30):
            action.key_down(Keys.PAGE_DOWN).perform()

        time.sleep(5)
        rows = WebDriverWait(driver, 99).until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), '자세히보기')]")))

        for row in rows:
            print(row)

        driver.quit()

if __name__ == '__main__':
    naver = NaverLogin()
    naver.load_page()
