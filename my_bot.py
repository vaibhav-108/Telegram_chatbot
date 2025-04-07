from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart,CommandObject,Command
import asyncio
from dotenv import load_dotenv
import os
import logging
from openai import OpenAI
import deepseek



load_dotenv()
TOKEN = os.getenv("TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")




# Connect with OpenAI
deepseek.api= DEEPSEEK_API_KEY
# print(f"deepseek api {DEEPSEEK_API_KEY}")
MODEL_NAME = "deepseek/deepseek-r1:free"

#Initialize bot 
bot = Bot(token=TOKEN)
dispatcher = Dispatcher()


class Reference:
    def __init__(self) -> None:
        self.response = ""


reference = Reference()


def clear_past():
    reference.response = ""


@dispatcher.message(Command('clear'))
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")




@dispatcher.message(Command('start'))
async def welcome(message: types.Message):
    """This handler receives messages with `/start` or  `/help `command

    Args:
        message (types.Message): _description_
    """
    await message.reply("Hi\nI am a Chat Bot! Created by Vaibhav. How can i assist you?")




@dispatcher.message(Command('help'))
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm a bot created by Vaibhav! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)




@dispatcher.message()
async def main_bot(message: types.Message):
    """
    A handler to process the user's input and generate a response using the openai API.
    """

    print(f">>> USER: \n\t{message.text}")

    client= OpenAI(api_key=DEEPSEEK_API_KEY,
                   base_url= "https://openrouter.ai/api/v1"
                   )
    
    response = client.chat.completions.create(
        model = MODEL_NAME,
        messages = [
            {"role": "assistant", "content": reference.response}, # role assistant
            {"role": "user", "content": message.text} #our query 
        ]
    )
    
    reference.response = response.choices[0].message.content
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response)
    
   
    
async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    # bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    bot = Bot(token=TOKEN)

    # And the run events dispatching
    await dispatcher.start_polling(bot,close_bot_session=False)




if __name__ == "__main__":
    asyncio.run(main())