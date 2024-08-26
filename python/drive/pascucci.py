from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os
import time

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
folder_path = "pascucci"
filename = f"{folder_path}/pascucci_{current_date}.json"

# 폴더 경로가 없다면 생성
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# 웹드라이버 초기화 (Chrome 사용)
options = ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# 방문할 URL 리스트
urls = [
    "https://www.caffe-pascucci.co.kr/store/storeList.asp?searchDrivethrough=Y&page=1",
    "https://www.caffe-pascucci.co.kr/store/storeList.asp?searchDrivethrough=Y&page=2",
]

# 데이터 추출을 위한 빈 리스트 생성
pascucci_data = []

for url in urls:
    # 페이지 로드
    browser.get(url)
    
    # 페이지의 끝까지 스크롤 내리기
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # 잠시 대기 (로딩 완료를 위해)
    time.sleep(3)

    # 업데이트된 페이지 소스를 변수에 저장
    html_source_updated = browser.page_source
    soup = BeautifulSoup(html_source_updated, 'html.parser')

    # 데이터 추출
    items = soup.select("#container > div.contents > div.schResultWr.schStoreResult > table > tbody > tr")

    for item in items:
        detail_button = item.select_one("td.detailInfoView > span.detailInfo > a")
        if detail_button:
            # 요소를 찾습니다.
            element = browser.find_element(By.CSS_SELECTOR, "td.detailInfoView > span.detailInfo > a")
            if element:
                element.click()
                print("클릭 성공")
                time.sleep(1)

                # 업데이트된 페이지 소스를 변수에 저장
                detail_html_source = browser.page_source
                detail_soup = BeautifulSoup(detail_html_source, 'html.parser')

                title = detail_soup.select_one("#modalStoreInfo > div > div.storeDetailInfo > h2")
                title = title_element.text.strip() if title_element else "No Title"
                
                address_element = detail_soup.select_one("#modalStoreInfo > div > div.storeDetailInfo > table > tbody > tr > td")
                address = address_element.text.strip() if address_element else "No Address"

                image_element = detail_soup.select_one("#modalStoreInfo > div > div.storeImgWr > ul > li.on > a > img")
                image_url = image_element.get('src').replace('/upload', 'https://www.caffe-pascucci.co.kr/upload') if image_element else "No Image URL"
                
                pascucci_data.append({
                    "title": title,
                    "address": address,
                    "imageURL": image_url,
                })
                print(f"추가된 데이터: {title}, {address}, {image_url}")

# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(pascucci_data, f, ensure_ascii=False, indent=4)

# 브라우저 종료
browser.quit()
