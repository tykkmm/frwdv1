import os
from telethon import TelegramClient, events, functions, types, Button
from config import *
import logging
import re
logging.basicConfig(level=logging.WARNING)
LOGS = logging.getLogger()
client = TelegramClient('LegendBoy', API_ID, API_HASH).start(bot_token=TOKEN)


# ============== Function ====================
def check_sudo(user_id):
    if user_id in SUDO_USERS:
        return True
    return False


# =================== Button =================
owner_keyboard = [
    [
        Button.url("Owner", url="https://t.me/LegendBoy_OP")
    ]
]

option_keyboard = [
    [
        Button.inline("Join", data="join"),
        Button.inline("Forward", data="forward")
    ]
]


# ===================== Command =================
@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    if not check_sudo(event.sender_id):
        return await event.reply("Hello Sir,\n\nWelcome To Join The List of Group and Forward Your Message in Multiple Group. Contact The Owner to Buy this bot Click Below and Start Talking With My Boss\n\n        Thanks 🙏.", buttons=owner_keyboard) 
    await event.reply("Hello Sir,\n\nWelcome To Join The List of Group and Forward Your Message in Multiple Group.\n There will be 2 Option\n\n1.Join The Group By List\n2.Forward Your Message in Multiple Group.", buttons=option_keyboard)

links = []

@client.on(events.callbackquery.CallbackQuery(data=re.compile(b"join")))
async def users(event):
    async with client.conversation(event.chat_id) as x:
        await x.send_message("GIVE ME TELETHON/PYROGRAM STRING SESSION")
        strses = await x.get_response()
        await x.send_message("GIVE ME THE FILE IN .TEXT EXTENSION FILE")
        grpid = await x.get_response()
        downloaded = await grpid.download_media()
        try:
            with open(downloaded, "r") as f:
                content = f.read()
                print(content)
                new_content = content.split("\n")
                for i in new_content:
                    i.replace("https://t.me/", "@")
                    i.replace(" ", "")
                    links.append(i)
            await event.reply(links)
            os.remove(downloaded)
        except Exception as e:
            await event.reply(f"**Something Error in Downloading File : ** `{e}`", buttons=option_keyboard)
            os.remove(downloaded)


# ==================== Start Client ==================#
client.run_until_disconnected()
