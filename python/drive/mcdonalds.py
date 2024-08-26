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
folder_path = "macs"
os.makedirs(folder_path, exist_ok=True)  # 폴더가 없으면 생성
filename = f"{folder_path}/macs_{current_date}.json"

# 웹드라이브 설치 및 초기화, headless 모드로 설정
options = ChromeOptions()
options.add_argument("--headless")  # headless 모드 설정
browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# 페이지 로드
print("페이지 로드 중...")
browser.get('https://www.mcdonalds.co.kr/kor/store/list.do')

# 페이지가 완전히 로드될 때까지 대기
WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.ID, "searchForm"))
)

# 드라이브스루 누르기
print("드라이브스루 선택...")
browser.find_element(By.CSS_SELECTOR, "#searchForm > div > div > div > span:nth-child(2)").click()

# 모든 구의 이름을 직접 저장했습니다
real_gu = ["강남구","강동구","강북구","강서구","관악구","광진구","구로구","금천구","노원구","도봉구","동대문구","동작구","마포구","서대문구","서초구","성동구","성북구","송파구","양천구","영등포구","용산구","은평구","종로구","중구","중랑구"]

macs = []
for gu in real_gu:
    print(f"현재 구: {gu}")
    try:
        browser.find_element(By.CSS_SELECTOR, "#searchWord").clear()
    except Exception as e:
        print(f"검색어 입력 필드 지우기 오류: {e}")
        pass
    browser.find_element(By.CSS_SELECTOR, "#searchWord").send_keys(gu)
    browser.find_element(By.CSS_SELECTOR, "#searchForm > div > div > div > span:nth-child(2) > label").click()
    browser.find_element(By.CSS_SELECTOR, "#searchForm > div > fieldset > div > button").click()
    time.sleep(1)

    # 페이지의 끝까지 스크롤 내리기
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # 업데이트된 페이지 소스를 변수에 저장
    html_source_updated = browser.page_source
    soup = BeautifulSoup(html_source_updated, 'html.parser')

    # 데이터 추출
    dt_list = browser.find_elements(By.CSS_SELECTOR, "#container > div.content > div.contArea > div > div > div.mcStore > table > tbody > tr")

    for data in dt_list:
        try:
            tmp = data.find_element(By.CSS_SELECTOR, "td.tdName > dl > dt > strong > a")
            lat, lng = tmp.get_attribute("href")[19:-2].split(",")
            # 원문이 javascript:moveMap(37.5667729,126.9794809);
            # 형식이기 때문에 앞에 구문을 지워주고, ","를 기준으로 split해서 저장.
            title = tmp.text
            text = data.text
            address = data.find_element(By.CSS_SELECTOR, "td.tdName > dl > dd.road").text

            if "서울" in text and "맥드라이브" in text:
                macs.append({
                    "title": title,
                    "lat": lat,
                    "lng": lng,
                    "address": address
                })
                print(f"추가된 데이터: {title}, {lat}, {lng},{address}")
        except Exception as e:
            print(f"데이터 추출 오류: {e}")

# 데이터를 JSON 파일로 저장
print("데이터 저장 중...")
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(macs, f, ensure_ascii=False, indent=4)

# 브라우저 종료
print("브라우저 종료 중...")
browser.quit()

print("스크립트 완료")
