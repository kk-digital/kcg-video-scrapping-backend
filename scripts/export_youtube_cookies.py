# prerequiesties
# pip install selenium
# sudo apt install chromium-browser chromium-chromedriver

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json

def export_youtube_cookies(username, password, filename):
    # Set options for headless browsing
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Set up the Chrome driver
    service = Service('/usr/bin/chromedriver')  # Adjust if necessary
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Open YouTube
        driver.get('https://www.youtube.com')

        # Wait for the page to load
        time.sleep(3)

        # Click on the sign-in button
        driver.find_element("xpath", '//*[@id="buttons"]/ytd-button-renderer').click()
        time.sleep(3)

        # Enter email
        email_input = driver.find_element("xpath", '//*[@type="email"]')
        email_input.send_keys(username)
        driver.find_element("xpath", '//*[@id="identifierNext"]').click()
        time.sleep(3)

        # Enter password
        password_input = driver.find_element("xpath", '//*[@type="password"]')
        password_input.send_keys(password)
        driver.find_element("xpath", '//*[@id="passwordNext"]').click()
        time.sleep(5)  # Wait for login to complete

        # Get cookies
        cookies = driver.get_cookies()

        # Write cookies to file
        with open(filename, 'w') as f:
            json.dump(cookies, f)

        print(f"Cookies exported to {filename}")

    finally:
        driver.quit()

if __name__ == "__main__":
    # Replace with your YouTube credentials
    youtube_username = 'your_email@example.com'
    youtube_password = 'your_password'
    export_youtube_cookies(youtube_username, youtube_password, 'youtube_cookies.json')
