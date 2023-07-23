import openai

from girlfriend_gpt import settings

openai.api_key=settings.OPENAI_API_KEY

async def echo(system:str, message:str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
            prompt=message,
            temperature=0.9,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0.5,
    )
    print(response['choices'][0]['text'])
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=response['choices'][0]['text'])