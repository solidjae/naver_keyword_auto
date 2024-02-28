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
from selenium.common.exceptions import TimeoutException
import pyperclip
import os
options = ChromeOptions()
# options.add_argument("--headless=new")

class NaverLogin:
    def __init__(self):
        self.id = "sofsysbrand"
        self.pw = "Sofmd2755!"
        self.service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(options=options, service=self.service)

    def scroll_for_buttons(self):
        desired_count = 50  # The specific number of rows you're waiting for
        seen_buttons = set()  # Set to track buttons that have been seen
        timeout = 30  # Timeout in seconds
        start_time = time.time()
        driver = self.driver
        
        while len(seen_buttons) < desired_count:
            try:
                # Wait for at least one element to ensure we have something to count
                WebDriverWait(driver, timeout).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), '자세히보기')]"))
                )
                buttons = driver.find_elements(By.XPATH, "//button[contains(text(), '자세히보기')]")

                for button in buttons:
                    seen_buttons.add(button)
                    
                current_count = len(seen_buttons)
                print(f"Current count: {current_count}")
                driver.find_element(By.XPATH, '/html/body/ui-view[1]/div[3]/div/div[3]/div/ui-view/div/div/div[2]/div[3]/div/div/div/div/div[3]/div[2]/div/div/div[7]/div[2]').click()  # Click on a random box
                # Scroll down to load more elements
                ActionChains(driver).key_down(Keys.PAGE_DOWN).perform()


                # Break the loop if the desired count is reached
                if current_count >= desired_count:
                    break
                
                # Wait a bit for new elements to load
                time.sleep(2)  # Adjust sleep time based on how quickly your page loads new elements
                
                # Check for timeout to avoid an infinite loop
                if time.time() - start_time > timeout:
                    print("Timed out waiting for more elements to load.")
                    break
            except TimeoutException:
                print("Timed out waiting for elements to be present.")
                break

        # Optionally, interact with buttons here or return the set of unique identifiers
        return list(seen_buttons)

    def load_page(self):
        
        current_directory = os.path.dirname(os.path.abspath(__file__))
        prefs = {"download.default_directory": current_directory}
        options.add_experimental_option("prefs", prefs)
        driver = self.driver

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

        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ui-view[1]/div[3]/div/div[2]/div[1]/div/div[1]/ul/li[14]/a')))
        driver.get('https://sell.smartstore.naver.com/#/search-popular/inflow')

        try: 
            WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/button'))) # wait till close button appears
            driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/button').click()
            print('successfully closed modal')
        except TimeoutException as ex:
            print(ex)
            pass
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="seller-content"]/ui-view/div/div/div[2]/div[3]/div/div/div/div/div[3]/div[2]/div/div/div[2]')))
        
        buttons = NaverLogin.scroll_for_buttons(self)

        time.sleep(5)
        # WebDriverWait(driver, 99).until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), '자세히보기')]")))

        print(len(buttons))
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="seller-content"]/ui-view/div/div/div[2]/div[3]/div/div/div/div/div[3]/div[2]/div/div/div[2]')))

        for button in buttons:
            button_id = button.get_attribute('id')
            driver.find_element(By.ID, button_id).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div[2]/div[1]/div[2]/div/div/button/span[1]')))
            driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[2]/div[1]/div[2]/div/div/button/span[1]').click()
            driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/button').click()
            print(button)

        driver.quit()

if __name__ == '__main__':
    naver = NaverLogin()
    naver.load_page()
