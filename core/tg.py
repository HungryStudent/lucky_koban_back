from pyrogram import Client
from pyrogram.errors.exceptions.bad_request_400 import UsernameNotOccupied

api_id = 8
api_hash = "7245de8e747a0d6fbe11f7cc14fcc0bb"


async def send_code(username):
    async with Client("my_session", api_id, api_hash) as app:
        try:
            await app.send_message(username, 'Ваш код - HBARN. Никому не сообщайте этот код!')
        except UsernameNotOccupied:
            pass

# from telethon import TelegramClient
#
# # These example values won't work. You must get your own api_id and
# # api_hash from https://my.telegram.org, under API Development.
# api_id = 14810761
# api_hash = '0fb4484730101a277254efc978dd2a1e'
#
# client = TelegramClient('lucky_ses', api_id, api_hash)
# client.start()
