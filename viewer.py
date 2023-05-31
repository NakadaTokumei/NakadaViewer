from flask import Flask, render_template
import os
import re
from urllib.parse import quote

app = Flask(__name__)

download_folder = 'static/'

@app.route('/')
def main_page():
    webtoon_list = os.listdir(download_folder)
    return render_template('index.html', webtoons = webtoon_list)

@app.route('/<webtoon_name>')
def webtoon_page(webtoon_name):
    episode_list = os.listdir(download_folder+webtoon_name+'/')
    episodes = sorted(episode_list, key=lambda s: int(re.search(r'\d+', s).group()))
    return render_template('episode_list.html', webtoon_name=webtoon_name, episodes=episodes)

@app.route('/<webtoon_name>/<int:episode>')
def viewer_page(webtoon_name, episode):
    episode -= 1
    webtoon_path = download_folder+webtoon_name+'/'
    episode_list = os.listdir(webtoon_path)
    episodes = sorted(episode_list, key=lambda s: int(re.search(r'\d+', s).group()))
    image_list = os.listdir(webtoon_path+episodes[episode]+'/')
    images = sorted(image_list, key=lambda s: int(re.search(r'\d+.jpg', s).group().replace('.jpg', '')))
    print(episodes)
    print(images)
    return render_template('viewer.html', webtoon_name=webtoon_name, episode=quote(episodes[episode].encode("utf8")), images=images)

if __name__ == '__main__':
    app.run()