import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd

head = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
res = req.get("https://www.melon.com/chart/index.htm", headers=head)

soup = bs(res.text, "lxml")

ranking = soup.select("tbody .t_center >.rank")
title = soup.select("tbody .wrap_song_info .ellipsis.rank01 span>a")
artist = soup.select("tbody .wrap_song_info .ellipsis.rank02 span>a:nth-child(1)")

print(ranking)

rankingList = [r.text.strip() for r in ranking]
titleList = [t.text.strip() for t in title]
artistList = [a.text.strip() for a in artist]

print(len(rankingList))
print(len(titleList))
print(len(artistList))

# 데이터 프레임 생성
chart_df = pd.DataFrame({
    'Ranking' : rankingList,
    'Title' : titleList,
    'Artist' : artistList
})

# JSON 파일로 저장
chart_df.to_json("melonChart100.json", force_ascii=False, orient="records")