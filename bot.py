#!usr/bin/python
import discord

#
#   Very simple utils set for Reports Patrol Mineplex Discord
#

question_channel = '731928268269158471'
bot_token = 'NzMzMzM0MzE4NDA3MjIxMzgw.XxBpVw.ModRUDpRDmAQd-HJ7N0Fb2II6p8'



class DiscordClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
    
    async def on_message(self, message):
        if message.author == self.user: return

        if message.content == '!ping':
            await message.channel.send('pong')

        if message.content == '@here' and str(message.channel.id) == question_channel:
            await message.channel.send('Forwarding your @here...')

client = DiscordClient()
client.run(bot_token)