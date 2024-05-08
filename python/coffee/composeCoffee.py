import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

current_date = datetime.now().strftime("%Y-%m-%d")
filename = f"compose-menu_{current_date}.json"

def get_coffee_data(url):
    # 사용자 에이전트 설정
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
    
    # 웹 페이지로부터 데이터 요청 및 수신
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")

    # 데이터 선택
    coffee_data = []
    rows = soup.select("tbody > tr.list")

    for row in rows:
        title = row.select_one(".title").text.strip()
        image_url = row.select_one("td a.cover img").get('src').replace('//', 'https://')

        coffee_data.append({
            "title": title,
            "imageUrl": image_url
        })

    return coffee_data

# 두 페이지의 URL
urls = [
    'https://composecoffee.com/menu/category/185?page=1',
    'https://composecoffee.com/menu/category/185?page=2'
]

# 모든 페이지에서 차트 데이터 가져오기
all_coffee_data = []
for url in urls:
    coffee_data = get_coffee_data(url)
    all_coffee_data.extend(coffee_data)

# JSON 파일로 저장
file_name = f"coffee_genie100_{current_date}.json"

with open(file_name, 'w', encoding='utf-8') as file:
    json.dump(all_coffee_data, file, ensure_ascii=False, indent=4)