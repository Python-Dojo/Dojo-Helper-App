import unittest
from funcs.replit_scrapper import ReplitScrapper
# import os
from dotenv import load_dotenv
load_dotenv()


class Test(unittest.TestCase):

    def test_scrapper_raise_value_error_when_replit_url_not_set(self):
        scrapper = ReplitScrapper(login_name=None, login_password=None)
        with self.assertRaises(ValueError) as ctx_manager:
            scrapper.get_replit_url()
        self.assertEqual(str(ctx_manager.exception), 'Missing replit_url')

    def test_scrapper_return_replit_url(self):
        test_url = "https://replit.com/@pythondojoarchi/SlipperyGargantuanDebuggers"

        scrapper = ReplitScrapper(login_name=None, login_password=None)
        scrapper.set_replit_url(test_url)
        self.assertEqual(scrapper.get_replit_url(), test_url)

    # Commented out to avoid replit acount freezes
    # def test_scrapper_login_with_invalid_credentials(self):
    #     scrapper = ReplitScrapper(login_name = os.environ['EMAIL'], login_password = "ThisIsNotTheCorrectPassword")
    #     with self.assertRaises(ValueError) as ctx_manager:
    #         scrapper.run()
    #     self.assertEqual(str(ctx_manager.exception), 'Invalid login credentials')

    # def test_scrapper_download_repo_as_zip(self):
    #     test_url = "https://replit.com/@pythondojoarchi/SlipperyGargantuanDebuggers"
    #     target_zip_name = "SlipperyGargantuanDebuggers.zip"
    #     WDIR = os.path.abspath(os.path.dirname(__name__))
    #     full_target_file_path = os.path.join(WDIR, "screen-shots", target_zip_name)
    #     print(full_target_file_path)

    #     scrapper = ReplitScrapper(login_name=os.environ['EMAIL'], login_password=os.environ['PASSWORD'])
    #     scrapper.set_replit_url(test_url)
    #     scrapper.run()

    #     print(scrapper.get_downloaded_filename())
    #     self.assertTrue(os.path.exists(full_target_file_path))


if __name__ == "__main__":
    unittest.main()
