from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart,CommandObject,Command
from dotenv import load_dotenv
import os
import logging
import asyncio


load_dotenv()
API_TOKEN = os.getenv("TOKEN")

# print(API_TOKEN)

# #configure logging
logging.basicConfig(level=logging.INFO)


#Initialize bot 

dp = Dispatcher()


@dp.message(Command('start','help')) #--> customize command we can give any
async def command_start_handler(message: types.Message):
    """This handler receives messages with `/start` or  `/help `command

    Args:
        message (types.Message): _description_
    """
    await message.reply("Hi!\n I am an Echo Bot!\n Powered by Aiogram")



@dp.message()
async def echo(message: types.Message):
    """This will return echo message

    Args:
        message (types.Message): _description_
    """

    await message.reply(message.text)
    # await message.reply("Got it")

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    # bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    bot = Bot(token=API_TOKEN)

    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    # executor.start_polling(dp, skip_updates=True)
    asyncio.run(main())