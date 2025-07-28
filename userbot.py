from telethon import TelegramClient, events
import re

api_id = 20455372
api_hash = 'f2263dbe1cdf4ff2ea64dcb08586eb56'
session_name = 'session'

SOURCE_CHANNEL = 1001864647136
TARGET_CHAT_ID = -1002647201593

client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    original_text = event.message.text or ''
    lines = original_text.split('\n')

    # Удаляем строку с хэштегом
    lines = [line for line in lines if not line.strip().startswith('#LoadTenderOpenedPublic')]

    # Удаляем блок "Дать ставку"
    filtered_lines = []
    skip_block = False
    for line in lines:
        if 'или самостоятельно принять участие' in line:
            skip_block = True
            continue
        if 'Дать ставку' in line:
            skip_block = False
            continue

        if not skip_block:
            # Удаляем хэштег вида #xxxxx
            line = re.sub(r'#\w+', '', line).replace('  ', ' ').strip()

            # Обработка маршрута
            if '📍' in line and '→' in line:
                route_text = re.sub(r'^.*📍', '', line).strip()  # убираем всё до 📍
                route_parts = [part.strip() for part in route_text.split('→')]

                if len(route_parts) == 3:
                    # Оставляем только первую и последнюю
                    new_route = f"📍 {route_parts[0]} → {route_parts[2]}"
                    line = new_route
                elif len(route_parts) == 2:
                    # Просто добавляем 📍 обратно
                    line = f"📍 {route_parts[0]} → {route_parts[1]}"
                # иначе не трогаем

            filtered_lines.append(line)

    # Объединяем и заменяем номер
    cleaned_text = '\n'.join(filtered_lines)
    cleaned_text = cleaned_text.replace('+998555118001', '+998951288881 --- +998958188882 ')

    # Добавляем ссылку в конце
    link = "https://t.me/NUSLOGGRUZ"
    cleaned_text += f"\n\nСсылка: {link}"

    print('Отправляю:\n', cleaned_text)
    await client.send_message(TARGET_CHAT_ID, cleaned_text)

print('Запускаю userbot...')
client.start()
client.run_until_disconnected()
