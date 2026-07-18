import pytesseract
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from io import BytesIO
import random
import os
import time

# Update this line with your Tesseract installation path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\kulitesh\ML-CaPsule\Dark Pattern Detection\Tesseract-OCR\tesseract.exe'

# URL to analyze
url_to_analyze = "https://www.myntra.com/"

def take_screenshot_and_analyze(url, num_screenshots=4):
    options = Options()
    options.headless = True 

    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        WebDriverWait(driver, 20).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

        # Create a directory to store screenshots if it doesn't exist
        if not os.path.exists("Screenshots"):
            os.makedirs("Screenshots")

        for i in range(num_screenshots):
            # Scroll down a random amount
            scroll_amount = random.randint(500, 1000)  # Adjust as needed
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(1)  # Adjust scroll time as needed

            # Capture screenshot
            screenshot = driver.get_screenshot_as_png()
            image = Image.open(BytesIO(screenshot))

            # Save screenshot to file
            screenshot_path = f"Screenshots/screenshot_{i + 1}.png"
            image.save(screenshot_path)

            # Use Tesseract OCR to extract text
            extracted_text = pytesseract.image_to_string(image)
            print(f"Extracted Text from screenshot {i + 1}:", extracted_text)

            # Analyze the extracted text for dark patterns
            pattern_counts = detect_dark_pattern_keywords(extracted_text)

            print(f"Dark Patterns Detected in screenshot {i + 1}:")
            for category, count in pattern_counts.items():
                print(f"{category}: {count} occurrences")

    except TimeoutException:
        print("Timed out waiting for page to load")

    finally:
        if 'driver' in locals():
            driver.quit()

def detect_dark_pattern_keywords(text):
    # List of groups of keywords to check against
    keyword_groups = [
        ["40%", "off"], ["50%", "off"], ["sale"], ["80%", "off"], ["70%", "off"], ["discount", "code"],
        ["clearance", "sale"],
        ["limited", "time", "offer"],
        # ... (rest of your keyword groups)
    ]
    
    # Initialize dark pattern counters
    pattern_counts = {keyword_group[0]: 0 for keyword_group in keyword_groups}

    # Iterate through keywords and check for matches
    for keyword_group in keyword_groups:
        for keyword in keyword_group[1:]:
            if keyword.lower() in text.lower():
                pattern_counts[keyword_group[0]] += 1

    return pattern_counts

# Perform screenshot and analysis for multiple screenshots
take_screenshot_and_analyze(url_to_analyze)