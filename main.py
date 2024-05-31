import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from middlewares import AntiFloodMiddleware
from dotenv import load_dotenv
import os
load_dotenv()
TOKEN = os.getenv('TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')



logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.message.middleware(AntiFloodMiddleware(0.1))

@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.reply("Hello! Send me a message and wait for a publication or response from the administration!")

@dp.message(F.text)
async def echo_text_message(message: types.Message):
    user = message.from_user
    message_text = message.text
    await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f'Message from {user.first_name} (@{user.username}): {message_text}'
    )
    await bot.send_message(user.id, "Thank you for your message, wait for the answer!")

@dp.message(F.photo | F.caption)
async def echo_photo_with_caption(message: types.Message):
    user = message.from_user
    caption = message.caption if message.caption else "Without caption"
    media = message.photo[-1].file_id
    caption = f'Фото от {user.first_name} (@{user.username}): {caption}'
    await bot.send_photo(ADMIN_CHAT_ID, media, caption=caption)
    await bot.send_message(user.id, "Thank you for your message, wait for the answer!")

@dp.message(F.video)
async def echo_video_message(message: types.Message):
    user = message.from_user
    video = message.video.file_id
    caption = message.caption if message.caption else "Without caption"
    await bot.send_video(
        chat_id=ADMIN_CHAT_ID,
        video=video,
        caption=f'Video from {user.first_name} (@{user.username}): {caption}'
    )
    await bot.send_message(user.id, "Thank you for your message, wait for the answer!")

@dp.message(F.media_group_id)
async def echo_media_group_message(message: types.Message):
    user = message.from_user
    media = []
    if message.photo:
        for item in message.photo:
            media.append(types.InputMediaPhoto(media=item.file_id))
    if message.video:
        for item in message.video:
            media.append(types.InputMediaVideo(media=item.file_id))
    media[0].caption = f'Message from {user.first_name} (@{user.username})'
    await bot.send_media_group(
        chat_id=ADMIN_CHAT_ID,
        media=media
    )
    await bot.send_message(user.id, "Thank you for your message, wait for the answer!")

async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())
