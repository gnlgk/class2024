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

# 웹드라이브 설치(수동)
# browser = webdriver.Chrome()
# webdriver.get("https://www.music-flo.com/browse")

# 웹드라이브 설치
options = ChromeOptions()
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://www.music-flo.com/browse')

# 페이지가 완전히 로드될 때까지 대기
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "chart_lst"))
)

# time.sleep(10)

# "더보기" 버튼을 찾아 클릭
try:
    more_button = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".btn_list_more"))
    )
    if more_button:
        browser.execute_script("arguments[0].click();", more_button)
        print("Clicked '더보기' button.")
        time.sleep(3)
except Exception as e:
    print("Error clicking '더보기':", e)

# 업데이트된 페이지 소스를 변수에 저장
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')

print(soup)