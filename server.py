import time
from datetime import datetime

from flask import Flask, request
import git

app = Flask(__name__)

server_start = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
app_name = 'Pocegram'
messages = [
    {
        'username': app_name,
        'text': 'Добро пожаловать в наш чат!\n\nПолезные команды:\n/status - '
                'покажет состояние сервера\n',
        'timestamp': time.time()
    },
    {'username': 'John', 'text': 'Hello everyone!', 'timestamp': time.time()},
    {'username': 'Jack', 'text': 'Hello, John!', 'timestamp': time.time()},
]

users = {
    'John': '12345',
    'Jack': '12345',
}


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8"/>
    <title>My Messenger</title>

    <style>
        .h1 {
            margin: 80px auto 5px auto;
            padding: 50px 10px;
            text-align: center;
            color: navy;
            background-color: lightgrey;
            animation-name: fadein;
            animation-duration: .8s;
        }

        @keyframes fadein {
            0% {opacity: 0;}
            25% {opacity: 0.3;}
            50% {opacity:0.5;}
            75% {opacity:0.7;}
            100% {opacity:1;}
        }

        .link {
            display: block;
            padding: 50px;
            text-align: center;
            font-size: 2em;
        }
    </style>
</head>
<body>

    <h1 class="h1">Welcome to My Messenger!</h1>
    <a class="link" href="/status/">Server status</a>

</body>
</html>'''


@app.route('/status', methods=['GET'])
@app.route('/status/')
def status():
    return {
        'status': 'OK',
        'name': app_name,
        'server_start_time': server_start,
        'server_current_time': datetime.now().strftime('%H:%M:%S %d.%m.%Y'),
        'current_time_seconds': time.time(),
        'total_messages': len(messages),
        'total_users': len(users),
    }


@app.route('/send_message/', methods=['POST'])
def send_message():
    username = request.json['username']
    password = request.json['password']
    text = request.json['text']

    if username in users:
        if users[username] != password:
            return {'ok': False}
    else:
        users[username] = password

    messages.append({'username': username, 'text': text, 'timestamp': time.time()})

    # Отправка в чат сервисного сообщения о состоянии сервера
    print(text, len(text))
    if text.replace(' ', '').replace('\n', '') in '/status':
        str_status = (f'Статус сервера: "{status()["status"]}"\n'
                      f'Название приложения: "{status()["name"]}"\n'
                      f'Время старта сервера: "{status()["server_start_time"]}'
                      f'Текущее время на сервере: "{status()["server_current_time"]}"\n'
                      f'Всего сообщений: "{status()["total_messages"]}"\n'
                      f'Зарегистрированных пользователей: "{status()["total_users"]}"\n')
        messages.append({
            'username': 'SERVER_INFO',
            'password': 'root',
            'text': str_status,
            'timestamp': time.time()
        })

    return {'ok': True}


@app.route('/get_messages')
def get_messages():
    after = float(request.args['after'])

    result = []

    for message in messages:
        if message['timestamp'] > after:
            result.append(message)

    return {
        'messages': result
    }


if __name__ == '__main__':
    app.run(debug=True)
