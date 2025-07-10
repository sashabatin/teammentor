import logging
from flask import Flask, request, jsonify
from telegram import Bot

app = Flask(__name__)

@app.route('/api/query', methods=['POST'])
def handle_telegram_update():
    telegram_data = request.get_json()
    chat_id = telegram_data.get('message', {}).get('chat', {}).get('id')
    user_message = telegram_data.get('message', {}).get('text', '')

    if chat_id and user_message:
        response_text = query_assistant(user_message)
        send_message_to_telegram(chat_id, response_text)

    return '', 200

def query_assistant(message):
    api_url = app.config['ASSISTANT_API_URL']
    response = requests.post(api, json={'query': message}).json()
    return response.get('response', "Sorry, I couldn't understand your request.")

def send_message_to_telegram(chat_id, message):
    telegram_api_url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    response = requests.post(telegram_api_url, json={
        'chat_id': chat_id,
        'text': message
    })
