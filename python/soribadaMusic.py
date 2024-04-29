import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pdSongListWithTools

head = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
res = req.get("https://www.soribada.com/music/chart", headers=head)

soup = bs(res.text, "lxml")

ranking = soup.select(".SongListWithTools")
title = soup.select(".music-list-cont .music-list .link-type1>.song-title")
artist = soup.select("tbody .wrap_song_info .ellipsis.rank02 span>a:nth-child(1)")

print(ranking)

rankingList = [r.text.strip() for r in ranking]
titleList = [t.text.strip() for t in title]
artistList = [a.text.strip() for a in artist]


# 데이터 프레임 생성
chart_df = pd.DataFrame({
    'Ranking' : rankingList,
    'Title' : titleList,
    'Artist' : artistList
})

