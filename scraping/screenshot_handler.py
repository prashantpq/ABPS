import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def capture_screenshot(url, output_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        screenshot_path = os.path.join(output_path, "screenshot.png")
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
    finally:
        driver.quit()
