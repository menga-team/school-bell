import requests
import os
from datetime import datetime, timedelta
import json
import time

ring_at = []

def format_date(date):
    return date.strftime('%Y-%m-%d')


def get_time(obj):
    return str(obj['h']) + ":" + str(obj['m'])


def get_times():
    del ring_at[:]
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
        'Accept': 'application/json, text/plain, */*',
    }
    json_data = {
        'username': os.environ['USER'],
        'password': os.environ['PASS'],
    }
    response = requests.post('https://rgtfo-me.digitalesregister.it/v2/api/auth/login', headers=headers, json=json_data)

    cookies = response.cookies

    now = datetime.now()
    monday = now - timedelta(days=now.weekday())
    formatted = format_date(monday)

    json_data = {
        'startDate': formatted,
    }

    response = requests.post('https://rgtfo-me.digitalesregister.it/v2/api/calendar/student', cookies=cookies,
                             headers=headers, json=json_data)
    calendar = json.loads(response.text)
    today = calendar[format_date(now)]['1']['1']
    for hour_it in today:
        hour = today[hour_it]
        if hour['isLesson'] == 1:
            lesson = hour['lesson']
            if hour_it == '1':
                ring_at.append(get_time(lesson['timeStartObject']))
            ring_at.append(get_time(lesson['timeToEndObject']))


if __name__ == "__main__":
    get_times()
    print(ring_at)
    while True:
        now = datetime.now()
        s_now = now.strftime('%H:%M')
        if s_now in ring_at:
            print("PLAYING...")
            os.system("aplay chime.wav")
            ring_at.remove(s_now)
        time.sleep(1)
        if now.day != datetime.now().day:
            get_times()
            print(ring_at)
