from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import json

current_date = datetime.now().strftime("%Y-%m-%d")
filename = f"composecoffee-menu_{current_date}.json"

browser = webdriver.Chrome()

urls = [
    'https://composecoffee.com/menu/category/185?page=1',
    'https://composecoffee.com/menu/category/185?page=2'
]

composecoffee_data = []

for url in urls:
    browser.get(url)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    html_source_updated = browser.page_source
    soup = BeautifulSoup(html_source_updated, 'html.parser')

    # 데이터 추출을 위해 클래스 이름으로 변경
    items = soup.select(".itemBox")  # 모든 항목을 선택
    for item in items:
        # 제목 추출
        title = item.select_one(".title").text.strip()
        # 이미지 URL 추출 및 수정
        img_url = item.select_one(".rthumbnailimg").get('src')
        if not img_url.startswith("http"):
            img_url = "https://composecoffee.com" + img_url  # 상대 경로일 경우 절대 경로로 변환

        composecoffee_data.append({
            "title": title,
            "img": img_url
        })

with open(filename, 'w', encoding='utf-8') as f:
    json.dump(composecoffee_data, f, ensure_ascii=False, indent=4)

browser.quit()