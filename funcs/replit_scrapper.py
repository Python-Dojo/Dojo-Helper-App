from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync


class ReplitScrapper():
    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/116.0.0.0 "
        "Safari/537.36 "
        "Edg/116.0.1938.81"
    )

    def __init__(self, login_name, login_password):
        self.__login_name = login_name
        self.__login_password = login_password
        self._replit_url = None
        self._downloaded_filename = None

    def set_replit_url(self, replit_url) -> None:
        if replit_url is None:
            raise ValueError
        self._replit_url = replit_url

    def get_replit_url(self) -> str:
        if self._replit_url is None:
            raise ValueError("Missing replit_url")
        return self._replit_url

    def _set_downloaded_filename(self, filename) -> None:
        if filename is None:
            raise ValueError("ReplitScrapper._set_downloaded_filename() argument is None")
        self._downloaded_filename = filename

    def get_downloaded_filename(self) -> str:
        if self._downloaded_filename is None:
            raise ValueError("Missing downloaded_filename")
        return self._downloaded_filename

    def _visit_replit_repo(self, page) -> None:
        response = page.goto(self.get_replit_url(), wait_until="domcontentloaded")
        if response.status != 200:
            if response.status == 404:
                print(f"response.status = {response.status}")
                raise ValueError("Invalid replit_url")
            else:
                print(f"response.status = {response.status}")
                raise ValueError("ReplitScrapper._visit_replit_repo() something other than 404 happened")

    def _login_replit(self, page) -> None:
        # Login
        page.goto('https://replit.com/login', wait_until="domcontentloaded")
        page.screenshot(path="./screen-shots/replit.png")
        url_init = "https://identitytoolkit.googleapis.com/v1/accounts"
        with page.expect_response(lambda response: url_init in response.url) as response_info:
            page.locator(
                "xpath=/html/body/div[1]/div/div[2]/div/main/div[2]/div/form/div[1]/input"
            ).fill(self.__login_name)
            page.locator(
                "xpath=/html/body/div[1]/div/div[2]/div/main/div[2]/div/form/div[2]/div/input"
            ).fill(self.__login_password)
            page.locator(
                "xpath=/html/body/div[1]/div/div[2]/div/main/div[2]/div/form/div[3]/button"
            ).click()
        response = response_info.value
        if response.status != 200:
            print(response)
            if response.status == 400:
                print(f"response.status = {response.status}")
                raise ValueError("Invalid login credentials")
            else:
                print(f"response.status = {response.status}")
                raise ValueError("ReplitScrapper._login_replit() something other than 401 happened")
        page.wait_for_url("https://replit.com/~")
        page.screenshot(path="./screen-shots/replit_after_login.png")

    def _download_as_zip(self, page) -> None:
        # Wait for page load
        page.locator(
            "xpath=/html/body/div[1]/div[1]/div[1]/div[2]/div/div[1]/div/div[3]/div/div[1]/button/div/span"
        ).wait_for()
        while page.locator(
                "xpath=/html/body/div[1]/div[1]/div[1]/div[2]/header/div[2]/button"
                ).text_content() != "Run":
            print(page.locator(
                "xpath=/html/body/div[1]/div[1]/div[1]/div[2]/header/div[2]/button"
                ).text_content())
            page.wait_for_timeout(2000)
        page.screenshot(path="./screen-shots/target_page.png")

        # Begin downloading
        page.locator(
            "xpath=/html/body/div[1]/div[1]/div[1]/div[2]/div/div[1]/div/div[2]/div[1]/div[1]/div/button[3]"
        ).click()
        with page.expect_download() as download_info:
            page.locator(
                "xpath=/html/body/div[@class='css-1o92kwk']//div[@id='item-4']//div[@class='css-1l2rn59']"
            ).click()
        download = download_info.value
        self._set_downloaded_filename(download.suggested_filename)
        download.save_as(f"./screen-shots/{download.suggested_filename}")

    def run(self):
        print("ReplitScrapper: Begin downloading repo files...")
        with sync_playwright() as p:
            # Context setup
            browser = p.chromium.launch(slow_mo=50)
            # browser = p.chromium.launch(headless=False
            #                 , slow_mo=50
            #                 )
            context = browser.new_context(user_agent=ReplitScrapper.user_agent)
            page = context.new_page()
            stealth_sync(page)

            # Login replit
            self._login_replit(page)

            # Download repo files as zip
            self._visit_replit_repo(page)
            self._download_as_zip(page)

            # Clean-up
            context.close()
            browser.close()
        print("ReplitScrapper: Download complete")
