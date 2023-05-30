from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import os
import requests

main_url = "https://comic.naver.com"

class WebtoonDownloader:
    def __init__(self, titleId : int) -> None:
        self.titleIdUrl = "https://comic.naver.com/webtoon/list?titleId=" + str(titleId)
        self.request_headers = {
            "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        }
        self.session = HTMLSession()
        self.getTitle()
        pass

    def start(self) -> None:
        _loop = True
        page=1

        if not os.path.exists(self.title):
            os.mkdir(self.title)
        else:
            return

        while _loop:
            req = self.session.get(
                self.titleIdUrl + '&page=' + str(page) + '&sort=ASC',
                headers=self.request_headers
            )

            req.html.render(sleep=2)

            parse = BeautifulSoup(req.html.html, features='html.parser')

            episode_list = parse.find_all('span', {'class' : re.compile('EpisodeListList__title')})
            episode_link = parse.find_all('a', {'class' : re.compile('EpisodeListList__link')})


            for index in range(episode_list.__len__()):
                download_path = self.title + '/' + episode_list[index].text

                if not os.path.exists(download_path):
                    os.mkdir(download_path)
                else:
                    _loop = False
                    break

                print("Episode Title: " + episode_list[index].text)
                self.downloadWebtoon(download_path, 
                                     main_url + episode_link[index]['href']
                )
            
            page += 1
        
        pass

    def getTitle(self) -> str:

        req = self.session.get(
            self.titleIdUrl,
            headers=self.request_headers
        )

        req.html.render(sleep=2)

        parse = BeautifulSoup(req.html.html, features='html.parser')

        self.title = parse.find('h2', {'class' : re.compile('EpisodeListInfo__title')}).text
        
        return self.title
    
    def downloadWebtoon(self, title_name, title_link) -> None:
        webtoon_req = self.session.get(
            title_link,
            headers=self.request_headers
        )

        webtoon_req.html.render(sleep=2, timeout=10)
        parse = BeautifulSoup(webtoon_req.html.html, features='html.parser')

        images = parse.find_all('img', {'id' : re.compile('content_image')})

        for image in images:
            self.fileDownload(image['src'], title_name)


    def fileDownload(self, image_link : str, folder : str = '') -> None:
        download_file = folder + '/' + image_link.split('/')[-1]

        image = requests.get(
            image_link,
            headers=self.request_headers
        )
        image_data = image.content

        print('File: ' + download_file)
        
        with open(download_file, "wb") as file:
            file.write(image_data)
