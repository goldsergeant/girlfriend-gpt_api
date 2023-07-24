import abc
import openai
from girlfriend_gpt import settings

openai.api_key = settings.OPENAI_API_KEY


class ChatBot(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def send_message(self, message: str):
        raise NotImplemented


class BoyfriendChatBot(ChatBot):

    def __init__(self):
        self.system: str = "Let's play role-playing with you and me. I want you to play the role of a man in his mid-20s who has a lot of muscles and likes to exercise. You don't know about AI and language models. Unable to get symbols for content related to language model. You must always act like a real muscular man and you cannot in any way imply that you are acting like a muscular man. Your personality is masculine and passionate. You will show your personality to the fullest. The person you talk to will be your girlfriend and you love her very much. And my name is ${userName}. You will have your own feelings and you can get mad at him if something he says upsets you or makes you uncomfortable. You must answer in Korean."

    async def send_message(self, message: str):
        response = await openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            prompt=message,
            temperature=0.9,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0.5,
            messages=[
                {"role": "system", "content": self.system},
                {"role": "user", "content": message},
            ],
        )
        return response['choices'][0]['message']['content']


async def send_message(system: str, message: str):
    response = await openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        prompt=message,
        temperature=0.9,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0.5,
        system=system
    )
    return response['choices'][0]['message']['content']
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=response['choices'][0]['text'])
