import unittest
from funcs.replit_scrapper import ReplitScrapper
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Test(unittest.TestCase):

    # def test_scrapper_quit(self):
    #     scrapper = ReplitScrapper()
    #     scrapper.driver.get('https://www.google.com/')
    #     scrapper.cleanup()
    #     self.assertFalse(scrapper.driver.service.is_connectable())
        
    # def test_scrapper_login_replit_homepage(self):
    #     scrapper = ReplitScrapper()
    #     scrapper.login()
    #     WebDriverWait(scrapper.driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, "//div[@data-cy='home-page']"))
    #     )
    #     self.assertEqual(scrapper.driver.current_url, 'https://replit.com/~')
    #     scrapper.cleanup()

    # def test_scrapper_get_given_url_after_login(self):
    #     scrapper = ReplitScrapper()
    #     scrapper.login()
    #     scrapper.driver.get('https://replit.com/@JustCallMeRay/Group2-Aug-23')
    #     self.assertEqual(scrapper.driver.current_url, 'https://replit.com/@JustCallMeRay/Group2-Aug-23')
    #     scrapper.cleanup()

    # def test_scrapper_returns_list_given_empty_input(self):
    #     scrapper = ReplitScrapper()
    #     scrapper.login()
    #     file_list = scrapper.get_file_list()
    #     self.assertIsInstance(file_list, list)
    #     scrapper.cleanup()
    
    def test_scrapper_returns_file_list_given_non_empty_input(self):
        scrapper = ReplitScrapper()
        # scrapper.login()
        scrapper.driver.get('https://replit.com/@JustCallMeRay/Group2-Aug-23')
        file_list = scrapper.get_file_list()
        expected = ['main.py']
        self.assertListEqual(file_list, expected)
        scrapper.cleanup()


if __name__ == "__main__":
    unittest.main()
