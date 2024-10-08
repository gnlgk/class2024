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
filename = f"menu-ediya_{current_date}.json"

# 웹드라이버 초기화 (Chrome 사용)
options = ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# 페이지 로드
browser.get('https://www.ediya.com/contents/drink.html?chked_val=12,&skeyword=#blockcate')

# '더보기' 버튼이 나타날 때까지 기다림 (최대 20초)
while True:
    try:
        more_button = WebDriverWait(browser, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".line_btn"))
        )
        if more_button:
            more_button.click()  # '더보기' 버튼 클릭
            print("Clicked '더보기' button.")
            time.sleep(2)  # 페이지 로딩 대기
    except Exception as e:
        print("더보기 버튼을 찾을 수 없음:", e)
        break

# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')

# 데이터 추출
coffee_data = []

# 위 데이터 추출
tracks = soup.select("#menu_ul li")
for track in tracks:
    name = track.select_one(".menu_tt > a > span").text.strip()
    image_url = track.select_one("a > img").get('src').replace('/images', 'https://www.ediya.com/files')
    titleE = track.select_one(".detail_con > h2 > span").text.strip()
    desction = track.select_one(".detail_con > p").text.strip()

    nutrition_info = {}
    tbody = track.select_one(".pro_nutri")
    if tbody:
        rows = tbody.find_all("dl")
        for row in rows:
            key = row.find("dt").text.strip()
            value = row.find("dd").text.strip()
            nutrition_info[key] = value

    coffee_data.append({
        "title": name,
        "imageURL": image_url,
         "brand": "이디아",
        "titleE": titleE,
        "desction": desction,
        "information": nutrition_info,
        "address": "https://www.coffine.co.kr/"
    })

# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(coffee_data, f, ensure_ascii=False, indent=4)

# 브라우저 종료
browser.quit()