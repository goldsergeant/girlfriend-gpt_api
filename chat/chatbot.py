import abc
import openai
from girlfriend_gpt import settings
from django.db import models

openai.api_key = settings.OPENAI_API_KEY


class ChatBot:
    def __init__(self, character):
        self.character = character

    def send_message(self, username: str, message: str):
        system = self.character.system.replace('{username}', username)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            temperature=0.9,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0.5,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": message},
            ],
        )
        return response['choices'][0]['message']['content']
