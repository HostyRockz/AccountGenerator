#    Copyright (C) Midhun KM 2020-2021
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import requests
from telethon.tl.types import InputWebDocument
from telethon import TelegramClient, events
from starkfunc import check_if_subbed
from telethon import custom, events, Button
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from Configs import Config
from loggers import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
import random
import re
from math import ceil
import telethon
import users_sql as warner
from telethon import Button, custom, events, functions

bot = TelegramClient("bot", api_id=Config.API_ID, api_hash=Config.API_HASH)
warnerstarkbot = bot.start(bot_token=Config.BOT_TOKEN)



@warnerstarkbot.on(events.NewMessage(pattern="^/start$"))
async def hmm(event):
    if Config.JTU_ENABLE:
    	starky = await check_if_subbed(Config.CHANNEL_USERNAME, event, warnerstarkbot)
    	if starky is False:
        	await event.reply("**I am Sorry To Say That, To Access Me You Have To Be The Member Of Our Channel To Use This Bot..!**", buttons=[[custom.Button.url("Join Channel", Config.CHANNEL_URL)]])
        	return
    st = await event.client(GetFullUserRequest(event.sender_id))
    user_text = f"""**Hello {st.user.first_name},
Welcome To {Config.ACCOUNT_GEN_NAME} Account Generator Bot

To Know About commands type:
/cmds

Bot Made With ❤️ By @DevseXpo**
""" 
    await event.reply(user_text) 
    
@warnerstarkbot.on(events.NewMessage(pattern="^/(help|cmds|commands|cmd|command)$"))
async def cmds(event):
    if Config.JTU_ENABLE:
    	starky = await check_if_subbed(Config.CHANNEL_USERNAME, event, warnerstarkbot)
    	if starky is False:
        	await event.reply("**I am Sorry To Say That, To Access Me You Have To Be The Member Of Our Channel To Use This Bot..!**", buttons=[[custom.Button.url("Join Channel", Config.CHANNEL_URL)]])
        	return
    st = await event.client(GetFullUserRequest(event.sender_id))
    help_text = f"""**Hello {st.user.first_name},
My Commands Are As Follows:

/start - To Restart Bot..!
/cmds - To Get Help Menu
/generate - To Generate Zee5 Accounts
/about - To Get Your Current Info

Share And Support Us...❤️**
"""
    await event.reply(help_text)     
    
@warnerstarkbot.on(events.NewMessage(pattern="^/(generate|gen|account)$"))
async def hmm(event):
    if Config.JTU_ENABLE:
    	starky = await check_if_subbed(Config.CHANNEL_USERNAME, event, warnerstarkbot)
    	if starky is False:
        	await event.reply("**I am Sorry To Say That, To Access Me You Have To Be The Member Of Our Channel To Use This Bot..!**", buttons=[[custom.Button.url("Join Channel", Config.CHANNEL_URL)]])
        	return
    hmmw = await event.reply("**Generating Account...Stay Tuned.**")
    if warner.is_user_in_db(int(event.sender_id)):
        hmm = warner.get_user_info(int(event.sender_id))
        if warner.is_user_in_db(int(event.sender_id)) >= Config.GEN_LIMIT_PERDAY:
            await hmmw.edit(f"**Your Daily Limit is exhausted, Kindly Contact the admins to increase ur limit\n\nBy The Way Daily Limit is {Config.GEN_LIMIT_PERDAY} accounts per day**", buttons=[[custom.Button.url("Join Channel", Config.CHANNEL_URL)]])
            return
        warner.update_user_usage(int(event.sender_id), int(1))
    else:

        warner.add_new_user(int(event.sender_id), int(1))
        print("New User : " + str(event.sender_id))
    with open('hits.txt') as f:
        stark_dict = f.read().splitlines()
    sed = random.choice(stark_dict)
    user_s = await warnerstarkbot.get_me()
    username = user_s.username
    email, password = sed.split(":")
    await hmmw.edit(
        f"<b><u>{Config.ACCOUNT_GEN_NAME} Account Generated.</u></b> \n<b>Email :</b> <code>{email}</code> \n<b>Password :</b><code>{password}</code> \n<b>You Can Check Your Limit or Info By /about<b> \n<b>Generated By @{username}</b>",
        parse_mode="HTML")
    
@warnerstarkbot.on(events.NewMessage(pattern="^/reset$"))
async def reset(event):
    if event.sender_id != Config.OWNER_ID:
        print("A Non Owner Used This Cmd")
        return
    ok = warner.get_all_users_id()
    for s in ok:
        try:
            warner.rm_user(int(s))
            await warnerstarkbot.send_message(int(s), "**Limit Has Been Reset , Generate Your Accounts Now !**")
        except:
            pass
    await event.reply("Reset Sucessfull Done!")    
    
@warnerstarkbot.on(events.NewMessage(pattern="^/broadcast"))
async def reset(event):
error_count = 0
msgtobroadcast = event.pattern_match.group(1)
if event.sender_id != Config.OWNER_ID:
    await event.reply("**Fuck OFF Bitch !**")
    return
hmm = get_all_users()
for starkcast in hmm:
    try:
        await UltraBot.send_message(int(starkcast.chat_id), msgtobroadcast)
    except BaseException:
        error_count += 1
sent_count = error_count - len(hmm)
await UltraBot.send_message(
event.chat_id,
      f"Broadcast Done in {sent_count} Group/Users and I got {error_count} Error and Total Number Was {len(userstobc)}",
)
        
async def clear_data():
    ok = warner.get_all_users_id()
    for s in ok:
        try:
            warner.rm_user(int(s))
            await warnerstarkbot.send_message(int(s), "**Limit Has Been Reset , Generate Your Accounts Now !**")
        except:
            pass
        
@warnerstarkbot.on(events.NewMessage(pattern="^/about$"))
async def a(event):
    if not warner.is_user_in_db(int(event.sender_id)):
        await event.reply(f"User-ID : {event.sender_id} \nLimit Used : 0 \nLimit Left : {Config.GEN_LIMIT_PERDAY}")
        return
    info_s = warner.get_user_info(int(event.sender_id))
    await event.reply(f"**📡Your Account Information\n\nUser-ID : {event.sender_id} \nLimit Used : {warner.is_user_in_db(int(event.sender_id))} \nLimit Left : {Config.GEN_LIMIT_PERDAY-warner.is_user_in_db(int(event.sender_id))}**")


scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(clear_data, trigger="cron", hour=6)
scheduler.start()

print("Bot Started Successfully")


def startbot():
    warnerstarkbot.run_until_disconnected()

if __name__ == "__main__":
    startbot()
