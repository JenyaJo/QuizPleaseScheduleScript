import requests
import lxml
import os
from bs4 import BeautifulSoup
import csv
def get_games():
    url = 'https://quizplease.ru/schedule'
    header = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44'
    }
    request = requests.request(url=url, method='get', headers=header)
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(request.text)
    with open('index.html', 'r', encoding='utf-8') as file:
        src = file.read()

    schedule = {}
    with open('./Games.csv', 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            [
                '№',
                'Дата',
                'Время',
                'Название',
                'Место',
                'Общее (для копирования)'
            ]
        )

    soup = BeautifulSoup(src, 'lxml')
    all_games = soup.find('div', id='schedule-vue').find_all('div', class_='schedule-column')
    count = 1
    color = ['yellow', 'pink', 'green']
    for game in all_games:
        name = f'{BeautifulSoup(str(game), "lxml").find("div", class_="h2 h2-game-card h2-left").text} {BeautifulSoup(str(game), "lxml").find("div", class_="h2 h2-game-card").text}'
        for i in color:
            try:
                date = f'{BeautifulSoup(str(game), "lxml").find("div", class_=f"h3 h3-{i} h3-mb10").text}'
                if date:
                    break
            except AttributeError:
                pass
        place = " ".join(i for i in BeautifulSoup(str(game), "lxml").find("div", class_="schedule-block-info-bar").text.split("\t")[0:2]).rstrip()
        time = BeautifulSoup(str(game), "lxml").find("div", class_="schedule-info-block").find_all("div", class_="schedule-info")[-2]
        true_time = BeautifulSoup(str(time), 'lxml').find('div', class_='techtext').text
        schedule[count] = [name, date, true_time, place]
        with open('./Games.csv', 'a', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                (
                    count,
                    date,
                    true_time,
                    name,
                    place,
                    f'{name} {date} {true_time}, {place}'
                )
            )
        count += 1
    os.remove('index.html')
get_games()
