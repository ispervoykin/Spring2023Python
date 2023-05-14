import time

from flask import Flask, request, abort
import requests
import random
from bs4 import BeautifulSoup
from datetime import datetime
app = Flask(__name__)
db = [
    {
        'time': time.time(),
        'name': 'AnimeBot',
        'text': 'Привет! Меня зовут AnimeBot, я могу предложить вам случайное аниме из подборки "MyAnimeList Top 50". Введите "/anime" в сообщении, чтобы я подобрал вам аниме.',
    },
]

@app.route("/")
def hello():
    return "Hello, World!"

def users():
    users = set()
    for message in db:
        users.add(message["name"])
    return list(users)

@app.route("/status")
def status():
    return {
        "number of users": len(users()),
        "list of users": users(),
        "number of messages": len(db),
        "status": True,
        "big brother mode": db,
        "time": datetime.now().astimezone().strftime("%H:%M:%S %d/%m/%Y")
    }

@app.route("/send", methods=["POST"])
def send_message():
    data = request.json

    if not isinstance(data, dict):
        return abort(400)
    if 'name' not in data or 'text' not in data:
        return abort(400)

    name = data["name"]
    text = data["text"]

    if not isinstance(name, str) or \
            not isinstance(text, str) or \
            name == '' or text == '':
        return abort(400)

    anime_numbers = []
    right_bound = 50    # maximum number of anime in a list

    if text == '/anime':

        if len(anime_numbers) == right_bound:   # clear the list to enable more anime requests
            anime_numbers.clear()

        page = requests.get('https://myanimelist.net/topanime.php')

        soup = BeautifulSoup(page.text, "html.parser")
        rand_number = random.randint(1, right_bound)
        while rand_number in anime_numbers:       # discard the already shown anime
            rand_number = random.randint(1, 50)

        movies = soup.find_all('tr', {'class': 'ranking-list'})
        title = movies[rand_number].find('div', {'class': 'di-ib clearfix'}).find('a').contents[0]
        score = movies[rand_number].find('td', {'class': 'score ac fs14'}).find('span').contents[0]
        link = movies[rand_number].find('a')['href']

        answer = f'Аниме: {title}\nМесто: {rand_number}\nРейтинг: {score}\nУзнать подробнее: {link}'


        message = {
            'time': time.time(),
            'name': 'AnimeBot',
            'text': answer,
        }
        """

        page = requests.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250')
        IMDb_url = 'https://www.imdb.com'
        soup = BeautifulSoup(page.text, "html.parser")
        movies = soup.find_all('tr')
        random_number = random.randint(1, 250)
        choosen_movie = movies[random_number]
        print(choosen_movie)
        """
    else:
        message = {
            'time': time.time(),
            'name': name,
            'text': text,
        }

    db.append(message)
    return {"ok": True}

@app.route("/messages")
def get_messages():
    """messages from db after given timestamp"""
    try:
        after = float(request.args['after'])
    except:
        return abort(400)

    result = []
    for message in db:
        if message['time'] > after:
            result.append(message)
            if len(result) >= 100:
                break

    return {"messages": result}

app.run()
