# -*- coding: utf-8 -*-
# @Time    : 2024/4/29 10:56
# @Author  : Xianmu Wang 122113096
# @FileName: Joker_UR_Scrape.py
# @Software: PyCharm
# !/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import xlwt
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}
base_url = "https://www.imdb.com/"
url = 'https://www.imdb.com/title/tt7286456/reviews/?ref_=tt_ql_2'

f = xlwt.Workbook()
sheet1 = f.add_sheet('Movie Reviews', cell_overwrite_ok=True)
row = ["Title", "Author", "Date", "Up Vote", "Total Vote", "Rating（Out of 10）", "Review"]
for i in range(0, len(row)):
    sheet1.write(0, i, row[i])

MAX_CNT = 100
cnt = 1

print("url = ", url)
res = requests.get(url, headers=headers)
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, "lxml")


for item in soup.select(".review-container"):
    title = item.select(".title")[0].text
    author = item.select(".display-name-link")[0].text
    date = item.select(".review-date")[0].text
    votetext = item.select(".text-muted")[0].text
    upvote = int(re.findall(r"\d*\,?\d+",votetext)[0].replace(",", ""))
    totalvote = int(re.findall(r"\d*\,?\d+", votetext)[1].replace(",", ""))
    rating = item.select("span.rating-other-user-rating > span")
    if len(rating) == 2:
        rating = rating[0].text
    else:
        rating = "Not rated"
    review = item.select(".text")[0].text
    row = [title, author, date, upvote, totalvote, rating, review]
    for i in range(0, len(row)):
        sheet1.write(cnt, i, row[i])
    cnt += 1

load_more = soup.select(".load-more-data")
if len(load_more):
    ajaxurl = load_more[0]['data-ajaxurl']
    base_url = base_url + ajaxurl + "?ref_=undefined&paginationKey="
    key = load_more[0]['data-key']
    flag = True
else:
    flag = False

while flag:
    url = base_url + key
    print("url = ", url)
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, "lxml")
    for item in soup.select(".review-container"):
        title = item.select(".title")[0].text
        author = item.select(".display-name-link")[0].text
        date = item.select(".review-date")[0].text
        votetext = item.select(".text-muted")[0].text
        upvote = int(re.findall(r"\d+", votetext)[0].replace(",", ""))
        totalvote = int(re.findall(r"\d+", votetext)[1].replace(",", ""))
        rating = item.select("span.rating-other-user-rating > span")
        if len(rating) == 2:
            rating = rating[0].text
        else:
            rating = "Not rated"
        review = item.select(".text")[0].text
        row = [title, author, date, upvote, totalvote, rating, review]
        for i in range(0, len(row)):
            sheet1.write(cnt, i, row[i])
        cnt = cnt + 1
        if cnt > MAX_CNT:
            break
    if cnt > MAX_CNT:
        break
    load_more = soup.select(".load-more-data")
    if len(load_more):
        key = load_more[0]['data-key']
    else:
        flag = False

f.save('Review_Joker.xls')
print(cnt-1, "reviews saved.")
