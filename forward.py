from telethon import TelegramClient, events, functions, types, Button
from config import *
import logging

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
        return event.reply("Hello Sir,\n\nWelcome To Join The List of Group and Forward Your Message in Multiple Group. Contact The Owner to Buy this bot Click Below and Start Talking With My Boss\n\n        Thanks 🙏.", buttons=owner_keyboard) 
    await event.reply("Hello Sir,\n\nWelcome To Join The List of Group and Forward Your Message in Multiple Group.\n There will be 2 Option\n\n1.Join The Group By List\n2.Forward Your Message in Multiple Group.", button=option_keyboard)


# ==================== Start Client ==================#
client.run_until_disconnected()
