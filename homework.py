import os
import requests
import time

from dotenv import load_dotenv

from twilio.rest import Client


load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)


def get_status(user_id):
    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    vk_api_v = os.getenv('VK_API_V')
    vk_base_url = os.getenv('VK_BASE_URL')

    params = {
        'user_ids': user_id,
        'v': vk_api_v,
        'access_token': vk_access_token,
        'fields': 'online'
    }
    user_state = requests.post(vk_base_url, params=params)
    user_state = user_state.json().get('response')[0]
    return user_state.get('online')


def send_sms(sms_text):
    number_from = os.getenv('NUMBER_FROM')
    number_to = os.getenv('NUMBER_TO')
    message = client.messages.create(
        body=sms_text,
        from_=number_from,
        to=number_to
    )
    return message.sid


# Проверка связи
if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            send_sms(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
