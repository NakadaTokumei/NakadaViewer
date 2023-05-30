from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import re
import os
import requests

main_url = "https://comic.naver.com"
downloaded_folder = "Download/"

class WebtoonDownloader:
    def __init__(self, titleId : int) -> None:

        if not os.path.exists(downloaded_folder):
            os.mkdir(downloaded_folder)

        user_data_dir_file = open('user_data_dir.dat', 'r')
        user_data_dir = user_data_dir_file.read()

        options = webdriver.ChromeOptions()
        options.add_argument("--user-data-dir=" + user_data_dir) 
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        
        self.titleIdUrl = "https://comic.naver.com/webtoon/list?titleId=" + str(titleId)
        self.request_headers = {
            "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        }

        self.session = webdriver.Chrome(chrome_options=options)
        self.timeout_wait = WebDriverWait(self.session, 5)
        self.getTitle()
        pass

    def start(self) -> None:
        _loop = True
        page=1

        if not os.path.exists(self.title):
            os.mkdir(self.title)
        else:
            return
        
        downloadUrl = self.titleIdUrl + '&page=' + str(page) + '&sort=ASC'

        page_source = self.getHtml(
            downloadUrl,
            'content',
            True
        )

        # print(self.session.page_source)

        while _loop:
            parse = BeautifulSoup(page_source, features='html.parser')

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
        source_page = self.getHtml(
            self.titleIdUrl,
            'content',
            True
        )

        parse = BeautifulSoup(self.session.page_source, features='html.parser')

        self.title = parse.find('h2', {'class' : re.compile('EpisodeListInfo__title')}).text
        
        return self.title
    
    def downloadWebtoon(self, title_name, title_link) -> None:

        source_page = self.getHtml(
            title_link,
            'comic_view_area',
            True
        )

        parse = BeautifulSoup(source_page, features='html.parser')

        images = parse.find_all('img', {'id' : re.compile('content_image')})

        for image in images:
            self.fileDownload(image['src'], downloaded_folder + title_name)


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

    def getHtml(self, target_link : str, wait_element_id : str = '', use_wait : bool = False) -> str:
        self.session.get(
            target_link
        )
        if use_wait:
            self.timeout_wait.until(EC.presence_of_element_located((By.ID, wait_element_id)))
        
        return self.session.page_source
