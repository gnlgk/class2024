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
filename = f"menu-starbucks_{current_date}.json"

# 웹드라이브 설치
options = ChromeOptions()
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)
browser.get("https://www.starbucks.co.kr:7643/menu/drink_list.do")

# 페이지가 완전히 로드될 때까지 대기
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "product_espresso"))
)

# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')

# 데이터 추출
coffee_data = []
tracks = soup.select("#container > .content > .product_result_wrap.product_result_wrap01 > div > dl > dd:nth-child(2) > .product_list > dl > dd > .product_espresso > li")

for track in tracks:
    # 각 커피 항목의 링크(Anchor 태그)를 찾습니다.
    coffee_link_element = track.select_one("a")
    if coffee_link_element:
        coffee_link = coffee_link_element.get('prod')
    
        # 상세 페이지로 이동하여 추가 데이터를 가져옵니다.
        browser.get(f"https://www.starbucks.co.kr:7643/menu/drink_view.do?product_cd={coffee_link}")
            
        # 페이지가 완전히 로드될 때까지 대기
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product_view_detail"))
        )

        # 상세 페이지의 소스를 변수에 저장
        detail_page_source = browser.page_source
        detail_soup = BeautifulSoup(detail_page_source, 'html.parser')

        title_element = soup.select_one(".myAssignZone h4")
        if title_element:
            title = title_element.contents[0].strip() if title_element.contents else "No Title"
            titleE = title_element.select_one("span").text.strip() if title_element.select_one("span") else "No English Title"
        else:
            title = "No Title"
            titleE = "No English Title"

        image_url = detail_soup.select_one(".product_big_pic img").get('src')
        descrition = detail_soup.select_one(".myAssignZone p.t1").text.strip()


        # 영양 정보 표를 가져옵니다.
        information = {}
        for row in soup.select(".product_view_info ul li"):
            print("Nutrition Table:", row)
            
            key = row.select_one("dt").text.strip()
            value = row.select_one("dd").text.strip()
            # print("Key:", key, "Value:", value)  # key와 value가 제대로 가져와지는지 확인
            information[key] = value


        coffee_data.append({
            "brand": "스타벅스",
            "title": title,
            "titleE": titleE,
            "imageURL": image_url,
            "desction": descrition,
            "information": information,
            "address": "https://www.starbucks.co.kr:7643/menu/drink_list.do?CATE_CD=product_espresso"
        })


# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(coffee_data, f, ensure_ascii=False, indent=4)

# # 브라우저 종료
# browser.quit()