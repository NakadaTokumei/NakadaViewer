#!/bin/python3
from Webtoon.Downloader import WebtoonDownloader
from selenium import webdriver
import requests

url = 'https://image-comic.pstatic.net/webtoon/802293/27/20230426222309_70d340529207eac85d1257e30ca4a2e9_IMAG01_'
request_headers = {
    "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

webtoon_downloader = WebtoonDownloader(730656)

if __name__ == '__main__':
    webtoon_downloader.start()
    # for i in range(1, 10):
    #     newUrl = url + str(i) + '.jpg'
    #     r = requests.get(newUrl, headers=request_headers)
    #     with open(newUrl.split('/')[-1], "wb") as outfile:
    #         outfile.write(r.content)
    pass