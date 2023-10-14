from dotenv import load_dotenv
load_dotenv()
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
from selenium.webdriver.common.action_chains import ActionChains

class ReplitScrapper():
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('incognito')
        chrome_options.add_argument("--window-size=1920,1080")
        # chrome_options.add_argument("--headless")
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(options=chrome_options)
        self.driver = driver

    # def login(self) -> None:
    #     self.driver.get(os.environ['LOGINURL'])
    #     wait = WebDriverWait(self.driver, 10)
    #     email = wait.until(EC.visibility_of_element_located((By.ID, "1val-input")))
    #     time.sleep(random.randint(2, 5))
    #     email.send_keys(os.environ['EMAIL'])
    #     password = wait.until(EC.visibility_of_element_located((By.ID, "2val-input")))
    #     time.sleep(random.randint(2, 5))
    #     password.send_keys(os.environ['PASSWORD'])
    #     submit_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@type='submit']")))
    #     time.sleep(random.randint(2, 5))
    #     action = ActionChains(self.driver)
    #     action.move_to_element(submit_button)
    #     action.click()
        
    def get_file_list(self) -> list:
        result = []
        wait = WebDriverWait(self.driver, 10)
        showcode_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='css-148day7']/span[@class='css-36v8q4']/button[@type='button']")))
        time.sleep(random.randint(2, 5))
        action = ActionChains(self.driver)
        action.move_to_element(showcode_button)
        action.click()
        files = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@role='treeitem']/preceding-sibling::div")))
        if len(files) != 0:
            for file in files:
                result.append(file.div.get_attribute('title'))
        else:
            print("File list not found.")
        return result
    
    def cleanup(self) -> None:
        self.driver.quit()