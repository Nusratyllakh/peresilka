from telethon import TelegramClient

api_id = 20455372
api_hash = 'f2263dbe1cdf4ff2ea64dcb08586eb56'
session_name = 'session'

client = TelegramClient(session_name, api_id, api_hash)

async def main():
    async for dialog in client.iter_dialogs():
        if 'Грузы' in dialog.name:  # ищет по части названия
            print(f'{dialog.name} — ID: {dialog.id}')

with client:
    client.loop.run_until_complete(main())
