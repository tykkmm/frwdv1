import asyncio
import contextlib
import os
import random
import re
import secrets
import string
import sys
import time
import logging

from pyrogram import Client
from pyrogram import errors as pyro_errors
from telethon import Button, TelegramClient, errors, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest as join

from config import *
logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] [%(name)s] : %(message)s",
    level=logging.ERROR,
    datefmt="%H:%M:%S",
)

LOGS = logging.getLogger("ForwardBot")

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


cancelj = {}

total = 0


@client.on(events.NewMessage(pattern="/stats"))
async def ttodjssk(event):
    global total
    return await event.reply(f"Total Running : {total}")


@client.on(events.NewMessage(pattern="/cj"))
async def cancelggjccjj(event):
    global cancelj
    if not check_sudo(event.sender_id):
        return await event.reply(
            "Hello Sir,\n\nWelcome To Join The List of Group and Forward Your Message in Multiple Group. Contact The Owner to Buy this bot Click Below and Start Talking With My Boss\n\n        Thanks 🙏.",
            buttons=owner_keyboard,
        )
    if cancelj[event.chat_id] == False:
        return await event.reply("There is no any task is running to stop joining")
    cancelj[event.chat_id] = False
    return await event.reply("Cancelled Joining Group")


@client.on(events.callbackquery.CallbackQuery(data=re.compile(b"join")))
async def users(event):
    global cancelj, total
    chat_id = event.chat_id
    links = []
    final_links = []
    if total > LIMIT:
        return await event.reply(
            f"Something Error : `The above exception was the direct cause of the following exception : Error R12 Full`"
        )
    async with client.conversation(chat_id) as x:
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
                chat_id, f"Total Groups in the List: {len(links)}\nProcessing"
            )
            await x.send_message(
                "GIVE ME THE INITIAL NUMBER FROM WHICH YOU WANT TO START JOINING"
            )
            initial_num = await x.get_response()
            await x.send_message(
                "GIVE ME THE FINAL NUMBER FROM WHICH YOU WANT TO STOP JOINING"
            )
            final_num = await x.get_response()
            cancelj[chat_id] = True
            total += 1
            if strses.text.endswith("="):
                legend = TelegramClient(StringSession(strses.text), API_ID, API_HASH)
                await legend.connect()
                success = 0
                fail = 0
                parts = message_link.text.split("/")
                channel_username = parts[3]
                message_id = int(parts[4])
                msg_id = await legend.get_messages(channel_username, ids=message_id)
                for i in range(int(initial_num.text), int(final_num.text)):
                    if cancelj[chat_id] == False:
                        total -= 1
                        await event.client.send_message(
                            event.chat_id,
                            f"Successfully Cancelled and Till Completed Your Task\nTotal Groups Joined : {success}\nTotal Fail : {fail}",
                        )
                        to_write = ""
                        for i in final_links:
                            to_write += f"{i}\n"
                        with open("new_file.txt", "w", encoding="utf-8") as f:
                            f.write(to_write)
                        with open(f"new_file.txt", "rb") as f:
                            await asyncio.sleep(5)
                            return await event.client.send_file(
                                event.chat_id,
                                file=f,
                                caption="Here is your new txt file.",
                            )
                    group_username = links[i]
                    try:
                        await legend(join(group_username))
                        await legend.forward_messages(group_username, msg_id)
                        final_links.append(group_username)
                        success += 1
                    except errors.FloodWaitError as e:
                        await event.client.send_message(
                            event.chat_id,
                            f"You have a floodwait of {int(e.seconds/60)} Minute & {int(e.seconds % 60)} Seconds .Please Wait Be Patience \nTill Now Group Joined : {success}\nTill Now Fail : {fail}",
                        )
                        await asyncio.sleep(int(e.seconds) + 100)
                    except Exception as f:
                        await event.reply(
                            f"This {group_username} group is not get joined due something error : `{f}`"
                        )
                        fail += 1
                    if int(success) % 3 == 0:
                        stime = random.randint(300, 400)
                        await event.client.send_message(
                            event.chat_id,
                            f"Till Now Groups Joined :  `{success}`\nTill Now Its Fail : `{fail}`",
                        )
                    else:
                        stime = random.randint(30, 60)
                    await asyncio.sleep(stime)
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
                            time.sleep(int(e.value) + 100)
                            continue
                        except Exception as e:
                            links.remove(i)
                            await event.reply(
                                f"This {i} group is not get joined due something error : `{e}`"
                            )
                            continue
                        time.sleep(100)
        except Exception as e:
            await event.reply(f"Something Error : `{e}`")
        total -= 1
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


cancelf = {}


@client.on(events.NewMessage(pattern="/cf"))
async def cancevddlf(event):
    global cancelf
    if not check_sudo(event.sender_id):
        return await event.reply(
            "Hello Sir,\n\nWelcome To Join The List of Group and Forward Your Message in Multiple Group. Contact The Owner to Buy this bot Click Below and Start Talking With My Boss\n\n        Thanks 🙏.",
            buttons=owner_keyboard,
        )
    if cancelf.get(event.chat_id) == False:
        return await event.reply("There is no any task is running to stop Forwarding")
    cancelf[event.chat_id] = False
    return await event.reply("Cancelled Forwarding Group")


@client.on(events.callbackquery.CallbackQuery(data=re.compile(b"forward")))
async def forward(event):
    global cancelf, total
    chat_id = event.chat_id
    owo = []
    if total > LIMIT:
        return await event.reply(
            f"Something Error : `The above exception was the direct cause of the following exception : Error R12 Full`"
        )
    async with client.conversation(chat_id) as x:
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
        os.remove(downloaa)
        return await event.reply(
            f"**Something Error in Downloading File : ** `{e}`",
            buttons=option_keyboard,
        )
    try:
        await event.client.send_message(
            chat_id, f"Total Groups in the list : {len(owo)}"
        )
        cancelf[chat_id] = True
        total += 1
        if strses.text.endswith("="):
            legend = TelegramClient(StringSession(strses.text), API_ID, API_HASH)
            await legend.connect()
            try:
                success = 0
                fail = 0
                parts = message_link.text.split("/")
                channel_username = parts[3]
                message_id = int(parts[4])
                while True:
                    for i in owo:
                        while cancelf.get(chat_id) == False:
                            total -= 1
                            return await event.client.send_message(
                                event.chat_id,
                                f"Successfully Cancelled and Till Completed Your Task\nTotal Groups in Sended : {success}\nTotal Fail : {fail}",
                            )
                        try:
                            await legend.forward_messages(
                                i, message_id, channel_username
                            )
                            success += 1
                        except errors.FloodWaitError as e:
                            await event.client.send_message(
                                event.chat_id,
                                f"You have a floodwait of {int(e.seconds/60)} Minute & {int(e.seconds % 60)}.Please Wait Be Patience \nTill Now Group in sended : {success}\nTill Now Fail : {fail}",
                            )
                            await asyncio.sleep(int(e.seconds) + 100)
                        except Exception:
                            fail += 1
                        if int(success) % len(owo) == 0:
                            stime = random.randint(900, 1200)
                            await event.client.send_message(
                                event.chat_id,
                                f"Till Now Groups in Sended :  `{success}`\nTill Now Its Fail : `{fail}`",
                            )
                        else:
                            stime = random.randint(1, 5)
                        await asyncio.sleep(stime)
            except Exception as e:
                await event.client.send_message(
                    event.chat_id,
                    f"Error in getting message :` {e}`",
                    buttons=option_keyboard,
                )
            try:
                await legend.disconnect()
            except Exception as e:
                await event.client.send_message(
                    event.chat_id,
                    f"Error While Disconnect Session : `{e}`",
                    buttons=option_keyboard,
                )
        else:
            random_string = "".join(
                secrets.choice(string.ascii_letters + string.digits) for _ in range(10)
            )
            async with Client(
                name=f"{random_string}",
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=strses.text,
            ) as kings:
                success = 0
                fail = 0
                parts = message_link.text.split("/")
                channel_username = parts[3]
                message_id = int(parts[4])
                while True:
                    for i in owo:
                        if cancelf[chat_id] == False:
                            total -= 1
                            return await event.client.send_message(
                                event.chat_id,
                                f"Successfully Cancelled and Till Completed Your Task\nTotal Groups in Sended : {success}\nTotal Fail : {fail}",
                            )
                        try:
                            await kings.forward_messages(
                                i, channel_username, message_id
                            )
                            success += 1
                        except pyro_errors.FloodWait as e:
                            await event.client.send_message(
                                event.chat_id,
                                f"You have a floodwait of {int(e.value/60)} Minute & {int(e.value % 60)}.Please Wait Be Patience \nTill Now Group in sended : {success}\nTill Now Fail : {fail}",
                            )
                            await asyncio.sleep(int(e.value) + 100)
                        except pyro_errors.Forbidden as e:
                            await event.reply(f"Forbidden Error in `{i}`: `{e}`")
                        except pyro_errors.BadRequest as e:
                            await event.reply(f"BadRequest Error in `{i}` : `{e}`")
                        except Exception as e:
                            await event.reply(
                                f"Error in sending message in {i} due to : `{e}`"
                            )
                            fail += 1
                        if int(success + fail) % len(owo) == 0:
                            stime = random.randint(1200, 1500)
                            await event.client.send_message(
                                event.chat_id,
                                f"Till Now Groups in Sended :  `{success}`\nTill Now Its Fail : `{fail}`\nSleeped For : `{stime}`",
                            )
                        else:
                            stime = random.randint(2, 4)
                        await asyncio.sleep(stime)
            total -= 1
            return await event.client.send_message(
                event.chat_id,
                f"Successfully Completed Your Task\nTotal Groups Sended : {success}\nTotal Fail : {fail}",
            )
    except Exception:
        pass


# ================== Start Function ===================


async def startup_process():
    for i in SUDO_USERS:
        try:
            await client.send_file(
                i,
                file="https://telegra.ph/file/2707a66c92ba3c2e40cee.jpg",
                caption=f"#START\n\nVersion:- α • 1.0\n\nYour Ads Promotion Bot Has Been Started Successfully",
                buttons=option_keyboard,
            )
        except:
            pass


client.loop.run_until_complete(startup_process())


# ==================== Start Client ==================#
if len(sys.argv) in {1, 3, 4}:
    with contextlib.suppress(ConnectionError):
        client.run_until_disconnected()
else:
    client.disconnect()
