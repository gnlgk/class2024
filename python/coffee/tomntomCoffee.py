from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json
import os

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
folder_path = "tomntoms"
filename = f"{folder_path}/menu-tomntom_{current_date}.json"

# 폴더 생성
os.makedirs(folder_path, exist_ok=True)

# 웹드라이브 설치
options = ChromeOptions()
options.add_argument("--headless")
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)
browser.get("https://www.tomntoms.com/menu/drink")

# 페이지가 완전히 로드될 때까지 대기
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "pb-20"))
)

# "더보기" 버튼을 찾아 클릭
try:
    more_button = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".custom-button.main-tab"))
    )
    if more_button:
        browser.execute_script("arguments[0].click();", more_button)
        print("Clicked '더보기' button.")
        time.sleep(3)  # 페이지가 로드될 시간을 주기 위해 잠시 대기
except Exception as e:
    print("Error clicking '더보기':", e)

# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')

# 데이터 추출
coffee_data = []
tracks = soup.select("#root > .max-w-7xl.p-4.mx-auto.pb-20.w-full > .grid.gap-6.mt-8.grid-cols-1 .relative.w-full")

for track in tracks:
    title_elem = track.select_one(".relative.w-full button > div > div > p > .tracking-wider")
    title = title_elem.text.strip() if title_elem else ""
    
    titleeng_elem = track.select_one(".relative.w-full button > div > div > h3")
    titleeng = titleeng_elem.text.strip() if titleeng_elem else ""
    
    image_url_elem = track.select_one(".relative.w-full button > div > img")
    image_url = image_url_elem.get('src') if image_url_elem else ""

    coffee_data.append({
        "brand": "탐탐",
        "title": title,
        "titleE": titleeng,
        "imageURL": f"{image_url}" if image_url else "",
        "address": "https://www.tomntoms.com/"
    })
    print(f"Added coffee data: {coffee_data[-1]}")

# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(coffee_data, f, ensure_ascii=False, indent=4)

# 브라우저 종료
browser.quit()

print(f"Data successfully saved to {filename}")
