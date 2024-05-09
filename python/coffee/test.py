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

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
folder_path = "starbucks"
filename = f"{folder_path}/menustarbucks_{current_date}.json"

# 웹드라이브 설치 및 초기화, headless 모드로 설정
options = ChromeOptions()
options.add_argument("--headless")  # headless 모드 설정
browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# 페이지 로드
browser.get('https://www.starbucks.co.kr:7643/menu/drink_list.do')

# 페이지가 완전히 로드될 때까지 대기
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "product_espresso"))
)

# 페이지의 끝까지 스크롤 내리기
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')

# 데이터 추출
starbucks_data = []
tracks = soup.select("#container > .content > .product_result_wrap.product_result_wrap01 > div > dl > dd:nth-child(2) > .product_list > dl > dd > ul > li")

for track in tracks:
    name = track.select_one("li > dl > dd").text.strip() 
    image_url = track.select_one("li > dl > dt > a > img").get('src') 
    starbucks_data.append({
        "title": name,
        "imageURL": image_url
    })

# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(starbucks_data, f, ensure_ascii=False, indent=4)

# 브라우저 종료
browser.quit()