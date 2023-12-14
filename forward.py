import asyncio
import contextlib
import logging
import os
import re
import sys

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

final_links = []
@client.on(events.callbackquery.CallbackQuery(data=re.compile(b"join")))
async def users(event):
    global links, success, fail
    async with client.conversation(event.chat_id) as x:
        await x.send_message("GIVE ME TELETHON/PYROGRAM STRING SESSION")
        strses = await x.get_response()
        await x.send_message("GIVE ME THE FILE IN .TXT EXTENSION FILE")
        grpid = await x.get_response()
        downloaded = await grpid.download_media()
        await x.send_message("GIVE ME THE LINK OF MESSAGE")
        message_link = await x.get_response()
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
            await event.client.send_message(
                event.chat_id, f"Total Groups in the List: {len(links)}\nProcessing"
            )
            await x.send_message("GIVE ME THE INITIAL NUMBER FROM WHICH YOU WANT TO START JOINING")
            initial_num = await x.get_response()
            await x.send_message("GIVE ME THE FINAL NUMBER FROM WHICH YOU WANT TO STOP JOINING")
            final_num = await x.get_response
            if strses.text.endswith("="):
                legend = TelegramClient(StringSession(strses.text), API_ID, API_HASH)
                await legend.connect()
                success = 0
                fail = 0
                parts = message_link.text.split("/")
                channel_username = parts[3]
                message_id = int(parts[4])
                msg_id = await legend.get_messages(channel_username, ids=message_id)
                for i in range(int(inital_num), int(final_num)):
                    group_username = links[i]
                    final_links.append(group_username)
                    try:
                        await legend(join(group_username))
                        await legend.forward_messages(group_username, msg_id)
                        success += 1
                    except errors.FloodWaitError as e:
                        await event.client.send_message(
                            event.chat_id,
                            f"You have a floodwait of {e.seconds} Seconds\nPlease wait end of floodwait i will inform you",
                        )
                        if e.seconds > 2000:
                            pass
                        else:
                            await asyncio.sleep(int(e.seconds) + 100)
                    except Exception as f:
                        await event.reply(
                            f"This {group_username} group is not get joined due something error : `{f}`"
                        )
                        fail += 1
                    if int(success) % 3 == 0:
                        time = 300
                        await event.client.send_message(
                            event.chat_id,
                            f"Till Now Groups Joined :  `{success}`\nTill Now Its Fail : `{fail}`",
                        )
                    else:
                        time = 30
                    await asyncio.sleep(time)
                await legend.disconnect()
                await event.client.send_message(
                    event.chat_id,
                    f"Successfully Completed Your Task\nTotal Groups Joined : {success}\nTotal Fail : {fail}",
                )
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
                            await event.client.send_message(
                                event.chat_id,
                                f"You have a floodwait of {e.value} Seconds\nPlease wait end of floodwait i will inform you",
                            )
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
        for i in final_links:
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
        message_link = await x.get_response()
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
            await event.client.send_message(
                event.chat_id, f"Total Groups in the list : {len(owo)}"
            )
            if strses.text.endswith("="):
                legend = TelegramClient(StringSession(strses.text), API_ID, API_HASH)
                await legend.connect()

                try:
                    parts = message_link.text.split("/")
                    channel_username = parts[3]
                    message_id = int(parts[4])
                    msg_id = await legend.get_messages(channel_username, ids=message_id)
                    for i in owo:
                        try:
                            await legend.forward_messages(i, msg_id)
                            await event.client.send_message(
                                event.chat_id, f"Sended Message in {i} Group"
                            )
                        except errors.FloodWaitError as e:
                            await event.client.send_message(
                                event.chat_id,
                                f"You have a floodwait of {e.seconds} Seconds\nPlease wait end of floodwait i will inform you",
                            )
                            await asyncio.sleep(int(e.seconds) + 100)
                            continue
                        except Exception as e:
                            owo.remove(i)
                            await event.reply(
                                f"Error in sending message in {i} due to : `{e}`"
                            )
                            continue
                        await asyncio.sleep(100)
                except Exception as e:
                    await event.client.send_message(
                        event.chat_id,
                        f"Error in getting message : {e}",
                        buttons=option_keyboard,
                    )
                try:
                    await legend.run_until_disconnected()
                except Exception as e:
                    LOGS.error(e)
        except Exception as e:
            await event.reply(f"Something Error : `{e}`", buttons=option_keyboard)


# ================== Start Function ===================


async def startup_process():
    for i in SUDO_USERS:
        await client.send_file(
            i,
            file="https://telegra.ph/file/2707a66c92ba3c2e40cee.jpg",
            caption=f"#START\n\nVersion:- α • 1.0\n\nYour Ads Promotion Bot Has Been Started Successfully",
            buttons=option_keyboard,
        )


client.loop.run_until_complete(startup_process())


# ==================== Start Client ==================#
if len(sys.argv) in {1, 3, 4}:
    with contextlib.suppress(ConnectionError):
        client.run_until_disconnected()
else:
    client.disconnect()
