from requests_html import HTMLSession
from bs4 import BeautifulSoup

class WebtoonDownloader:
    def __init__(self, titleId : int) -> None:
        self.titleIdUrl = "https://comic.naver.com/webtoon/list?titleId="
        self.titleId = titleId
        self.request_headers = {
            "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        }
        self.session = HTMLSession()
        pass

    def start(self) -> None:
        req = self.session.get(
            self.titleIdUrl + str(self.titleId),
            headers=self.request_headers
        )

        req.html.render()

        print(self.titleIdUrl + str(self.titleId))

        parse = BeautifulSoup(req.content, features='html.parser')
        
        print(parse.find_all('div'))
        
        pass
