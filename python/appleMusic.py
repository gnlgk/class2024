import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd

res = req.get("https://music.apple.com/kr/playlist/%EC%98%A4%EB%8A%98%EC%9D%98-top-100-%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD/pl.d3d10c32fbc540b38e266367dc8cb00c")

soup = bs(res.text, "lxml")

# 데이터 선택
ranking = soup.select(".section-content.svelte-gla0uw")
title = soup.select(".title>a")
artist = soup.select(".artist>a:nth-child(1)")

print(ranking)
# 데이터 저장
rankingList = [r.text.strip() for r in ranking]
titleList = [t.text.strip() for t in title]
artistList = [a.text.strip() for a in artist]

# 데이터 프레임 생성
chart_df = pd.DataFrame({
    'Ranking' : rankingList,
    'Title' : titleList,
    'Artist' : artistList
})

# JSON 파일로 저장
chart_df.to_json("bugsChart100.json", force_ascii=False, orient="records")