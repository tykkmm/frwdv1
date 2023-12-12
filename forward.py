import asyncio
import logging
import os
import re

from pyrogram import Client
from telethon import Button, TelegramClient, errors, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest as join

from config import *

logging.basicConfig(level=logging.WARNING)
LOGS = logging.getLogger()
client = TelegramClient("LegendBoy", API_ID, API_HASH).start(bot_token=TOKEN)


# ============== Function ====================
def check_sudo(user_id):
    if user_id in SUDO_USERS:
        return True
    return False


# =================== Button =================
owner_keyboard = [[Button.url("Owner", url="https://t.me/LegendBoy_OP")]]

option_keyboard = [
    [Button.inline("Join", data="join"), Button.inline("Forward", data="forward")]
]


# ===================== Command =================
@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    if not check_sudo(event.sender_id):
        return await event.reply(
            "Hello Sir,\n\nWelcome To Join The List of Group and Forward Your Message in Multiple Group. Contact The Owner to Buy this bot Click Below and Start Talking With My Boss\n\n        Thanks 🙏.",
            buttons=owner_keyboard,
        )
    await event.reply(
        "Hello Sir,\n\nWelcome To Join The List of Group and Forward Your Message in Multiple Group.\n There will be 2 Option\n\n1.Join The Group By List\n2.Forward Your Message in Multiple Group.",
        buttons=option_keyboard,
    )


links = []


@client.on(events.callbackquery.CallbackQuery(data=re.compile(b"join")))
async def users(event):
    global links
    async with client.conversation(event.chat_id) as x:
        await x.send_message("GIVE ME TELETHON/PYROGRAM STRING SESSION")
        strses = await x.get_response()
        await x.send_message("GIVE ME THE FILE IN .TXT EXTENSION FILE")
        grpid = await x.get_response()
        downloaded = await grpid.download_media()
        try:
            with open(downloaded, "r") as f:
                content = f.read()
                new_content = content.split("\n")
                for i in new_content:
                    i = i.replace("https://t.me/", "@").replace(" ", "").strip()
                    links.append(i)
            os.remove(downloaded)
        except Exception as e:
            await event.reply(
                f"**Something Error in Downloading File : ** `{e}`",
                buttons=option_keyboard,
            )
            os.remove(downloaded)
        try:
            if strses.text.endswith("="):
                legend = TelegramClient(StringSession(strses.text), API_ID, API_HASH)
                await legend.connect()
                for i in links:
                    try:
                        await legend(join(i))
                        await legend.send_message(i, "Thanks 🙏")
                    except errors.FloodWaitError as e:
                        await asyncio.sleep(int(e.seconds) + 100)
                        continue
                    except Exception as e:
                        links.remove(i)
                        await event.reply(
                            f"This {i} group is not get joined due something error : `{e}`"
                        )
                        continue
                    await asyncio.sleep(100)
                await legend.disconnect()
            else:
                async with Client(
                    "prolegend",
                    api_id=API_ID,
                    api_hash=API_HASH,
                    session_string=strses.text,
                ) as plegend:
                    for i in links:
                        try:
                            await plegend.join_chat(i)
                            await plegend.send_message(i, "Thanks 🙏")
                        except pyro_errors.FloodWait as e:
                            await asyncio.sleep(int(e.value) + 100)
                            continue
                        except Exception as e:
                            links.remove(i)
                            await event.reply(
                                f"This {i} group is not get joined due something error : `{e}`"
                            )
                            continue
                        await asyncio.sleep(100)
        except Exception as e:
            await event.reply(f"Something Error : `{e}`")
        to_write = ""
        for i in links:
            to_write += f"{i}\n"
        with open("new_file.txt", "w", encoding="utf-8") as f:
            f.write(to_write)
        with open(f"new_file.txt", "rb") as f:
            await asyncio.sleep(5)
            doc = await event.client.send_file(
                event.chat_id, file=f, caption="Here is your new txt file."
            )


owo = []


@client.on(events.callbackquery.CallbackQuery(data=re.compile(b"forward")))
async def forward(event):
    global owo
    async with client.conversation(event.chat_id) as x:
        await x.send_message("GIVE ME TELETHON/PYROGRAM STRING SESSION")
        strses = await x.get_response()
        await x.send_message("GIVE ME THE FILE IN .TXT EXTENSION FILE")
        grpid = await x.get_response()
        downloaa = await grpid.download_media()
        await x.send_message("GIVE ME THE LINK OF MESSAGE")
        msg_link = await x.get_response()
        try:
            with open(downloaa, "r") as f:
                content = f.read()
                new_content = content.split("\n")
                for i in new_content:
                    i = i.replace("https://t.me/", "@").replace(" ", "").strip()
                    owo.append(i)
            os.remove(downloaa)
        except Exception as e:
            await event.reply(
                f"**Something Error in Downloading File : ** `{e}`",
                buttons=option_keyboard,
            )
            os.remove(downloaa)
        try:
            if strses.text.endswith("="):
                legend = TelegramClient(StringSession(strses.text), API_ID, API_HASH)
                await legend.connect()
                msg_id = legend.get_messages(msg_link)
                for i in owo:
                    try:
                        await legend.forward_messages(i, msg_id)
                    except errors.FloodWaitError as e:
                        await asyncio.sleep(int(e.seconds) + 100)
                        continue
                    except Exception as e:
                        owo.remove(i)
                        await event.reply(
                            f"Error in sending message in {i} due to : `{e}`"
                        )
                    continue
                    await asyncio.sleep(100)
                await legend.disconnect()
        except Exception as e:
            await event.reply(f"Something Error : `{e}`")


# ==================== Start Client ==================#
client.run_until_disconnected()
