#!usr/bin/python
import discord
import asyncio
from datetime import datetime
import sys
from os import path
import os
import traceback

#
#   Very simple utils set for Reports Patrol Mineplex Discord
#

question_channel = '731928268269158471'
bot_token = 'NzMzMzM0MzE4NDA3MjIxMzgw.XxBpVw.ModRUDpRDmAQd-HJ7N0Fb2II6p8'
rp_discord_id = '731892044141690880'
rp_discord_announcements = '731927613538304152'
rp_lead = '161940995204841474'
rp_role = '731892867324444682'
date_save_file = 'last_reminder.txt'


qotw_reminder_msg = f'''<@&{rp_role}>\n**QOTW Reminder Message!**
\nIf you are unsure whether you have submitted your QOTW yet, please go to the **QOTW link** and see if it still allows you to send in a response 
(which would mean you haven't sent in a response yet) or says you have already submitted a response.
\nIf you would like to re-submit your QOTW for whatever reason, please contact <@{rp_lead}>.
'''


class DiscordClient(discord.Client):

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        self.loop.create_task(self.qotw_reminder_loop())
        self.last_sent = self.get_last_announce_from_file() #'2020-07-19-20:03:41'
        self.writing_file = False
    

    async def on_message(self, message):
        if message.author == self.user: return

        if message.content == '!ping':
            await message.channel.send('pong')

        if message.content == '@here' and str(message.channel.id) == question_channel:
            await message.channel.send('Forwarding your @here...')

    def get_last_announce_from_file(self):
        if path.exists(date_save_file):
            f = open(date_save_file)
            data = f.read()
            if len(data) != 19:
                return None
            print('Last QOTW Reminder was sent on ', data)
            return data
        return None

    def save_new_last_announce(self):
        if path.exists(date_save_file):
            os.remove(date_save_file)

        f = open(date_save_file, 'w')
        f.write(self.last_sent)
        f.close()

    def should_post_qotw(self):
        now = datetime.utcnow()
        now_day = now.strftime("%A")
        now_date  = now.strftime('%Y-%m-%d-%H:%M:%S')
        day_to_post = 'Saturday'

        if self.last_sent == None:
            if now_day == day_to_post:
                return (True, now_date)
            else:
                return (False, None)
        
        if now_day != day_to_post:
            return (False, None)

        old_month = self.last_sent[5:7]
        current_month = now_date[5:7]
        old_day = self.last_sent[8:10]
        current_day = now_date[8:10]

        if old_day != current_day or old_month != current_month:
            return (True, now_date)
        
        return (False, None)

    async def qotw_reminder_loop(self):
        while True:
            try:
                g = self.get_guild(int(rp_discord_id))
                if not g == None:
                    c = g.get_channel(int(rp_discord_announcements))

                    if not c == None:
                        r = self.should_post_qotw()
                        send_now = r[0]
                    
                        if send_now and not self.writing_file:
                            self.writing_file = True
                            await c.send(qotw_reminder_msg)
                            self.writing_file = False
                            self.last_sent = r[1]
                            self.save_new_last_announce()

            except Exception as e:
                traceback.print_exc()
                    
            await asyncio.sleep(5)


client = DiscordClient()
client.run(bot_token)
