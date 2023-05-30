#!/bin/python3
from Webtoon.Downloader import WebtoonDownloader
import requests

if __name__ == '__main__':
    print('Welcome Nakada\'s Naver Webtoon Downloader!')
    titleid=int(input('titleid: '))
    webtoon_downloader = WebtoonDownloader(titleid)
    print('Webtoon Name : ' + webtoon_downloader.title)
    webtoon_downloader.start()
    pass