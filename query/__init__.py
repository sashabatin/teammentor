import logging
import os
import requests
import azure.functions as func
from telegram import Bot

app = func.FunctionApp()

@app.route(route="query", auth_level=func.AuthLevel.ANONYMOUS)
def main(req: func.HttpRequest) -> func.HttpResponse:
    telegram_data = req.get_json()
    chat_id = telegram_data.get('message', {}).get('chat', {}).get('id')
    user_message = telegram_data.get('message', {}).get('text', '')

    if chat_id and user_message:
        response_text = query_assistant(user_message)
        send_message_to_telegram(chat_id, response_text)

    return func.HttpResponse(status_code=200)

def query_assistant(message):
    api_url = os.environ['ASSISTANT_API_URL']
    response = requests.post(api_url, json={'query': message})
    return response.json().get('response', "Sorry, I couldn't understand your request.")

def send_message_to_telegram(chat_id, message):
    telegram_token = os.environ['TELEGRAM_BOT_TOKEN']
    telegram_api_url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'
    requests.post(telegram_api_url, json={
        'chat_id': chat_id,
        'text': message
    })
