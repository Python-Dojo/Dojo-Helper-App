from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import os
from dotenv import load_dotenv
load_dotenv()

ua = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/69.0.3497.100 Safari/537.36"
    )

test_url = "https://replit.com/@pythondojoarchi/SlipperyGargantuanDebuggers"

with sync_playwright() as p:
    # browser = p.chromium.launch(headless=False
    #                             , slow_mo=50
    #                             )
    browser = p.chromium.launch()
    context = browser.new_context(user_agent=ua)
    page = context.new_page()
    stealth_sync(page)
    page.goto(os.environ['LOGINURL'], wait_until="domcontentloaded")
    page.screenshot(path="./screen-shots/replit.png")

    # Login
    page.locator("xpath=/html/body/div[1]/div/div[2]/div/main/div[2]/div/form/div[1]/input").fill(os.environ['EMAIL'])
    page.locator("xpath=/html/body/div[1]/div/div[2]/div/main/div[2]/div/form/div[2]/div/input").fill(os.environ['PASSWORD'])
    page.locator("xpath=/html/body/div[1]/div/div[2]/div/main/div[2]/div/form/div[3]/button").click()
    page.wait_for_url("https://replit.com/~")
    page.screenshot(path="./screen-shots/replit_after_login.png")

    # Download repo files as zip
    page.goto(test_url, wait_until="domcontentloaded")
    page.locator("xpath=/html/body/div[1]/div[1]/div[1]/div[2]/div/div[1]/div/div[3]/div/div[1]/button/div/span").wait_for()
    while page.locator("xpath=/html/body/div[1]/div[1]/div[1]/div[2]/header/div[2]/button").text_content() != "Run":
        print(page.locator("xpath=/html/body/div[1]/div[1]/div[1]/div[2]/header/div[2]/button").text_content())
        page.wait_for_timeout(2000)
    page.screenshot(path="./screen-shots/target_page.png")
    
    page.locator("xpath=/html/body/div[1]/div[1]/div[1]/div[2]/div/div[1]/div/div[2]/div[1]/div[1]/div/div[3]/button").click()
    with page.expect_download() as download_info:
        page.locator("xpath=/html/body/div[@class='css-1o92kwk']//div[@id='item-4']//div[@class='css-1l2rn59']").click()
    download = download_info.value
    download.save_as(f"./screen-shots/{download.suggested_filename}")

    # Clean-up
    context.close()
    browser.close()



