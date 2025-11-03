import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Chrome options
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Launch Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://personal.techforing.com/whatsappgttest"
driver.get(url)

# Wait for JS to load
time.sleep(3)

# === 1. Extract existing data from dataLayer ===
data_layer = driver.execute_script("return window.dataLayer || [];")

# Find the latest formDataReady object
form_data = None
for item in reversed(data_layer):  # iterate from last
    if item.get("event") == "formDataReady":
        form_data = item
        
        break

if form_data:
    print("✅ Extracted from dataLayer:", json.dumps(form_data, indent=2))

    # === 2. Push it back to dataLayer for GTM ===
    driver.execute_script(f"window.dataLayer.push({json.dumps(form_data)});")
    driver.execute_script("window.dispatchEvent(new Event('dataLayerUpdate'));")
    print("✅ Data pushed again to dataLayer for GTM")

else:
    print("⚠️ No formDataReady found in dataLayer")

driver.quit()