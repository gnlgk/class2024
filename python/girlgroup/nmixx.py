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
filename = f"menu-nmixx_{current_date}.json"

# 웹드라이브 설치
options = ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)
browser.get("https://twitter.com/NMIXX_official")

# 페이지가 완전히 로드될 때까지 대기
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "css-175oi2r.r-1pi2tsx.r-13qz1uu.r-18u37iz"))
)

# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')

# 데이터 추출
nmixx_data = []
tracks = soup.select("#id__l44kxshw2td > div > div > div > div > div > .r-1p0dtai.r-1pi2tsx.r-u8s1d.r-1d2f490.r-ipm5af.r-13qz1uu")
#id__ggi2kbnfj0h > div > div > div > div > div > div.r-1p0dtai.r-1pi2tsx.r-u8s1d.r-1d2f490.r-ipm5af.r-13qz1uu > div > div.css-175oi2r.r-1iusvr4.r-16y2uox.r-bnwqim.r-a5pmau > div > a > div > div > img
#id__vkntqvgpcj > div > div > div > div > div > div > a > div > div.r-1p0dtai.r-1pi2tsx.r-u8s1d.r-1d2f490.r-ipm5af.r-13qz1uu > div > img
#id__lbka8062gai > div > div > div > div > div > div > a > div > div.r-1p0dtai.r-1pi2tsx.r-u8s1d.r-1d2f490.r-ipm5af.r-13qz1uu > div > img
for track in tracks:
    image_url = track.select_one(".r-1p0dtai.r-1pi2tsx.r-u8s1d.r-1d2f490.r-ipm5af.r-13qz1uu > div > img").get('src')
    nmixx_data.append({
        "imageURL": image_url,
    })

# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(nmixx_data, f, ensure_ascii=False, indent=4)

# # 브라우저 종료
# browser.quit()