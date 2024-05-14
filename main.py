import discord
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

confessions = {}
confessionUSR = {}
confessionConfirmed = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    bot.loop.create_task(check_confession_changes())

@bot.command()
async def mainMSG(ctx):
    message = await ctx.send(" ```Anonymous posts ```")
    await message.add_reaction("😊")

@bot.event
async def on_reaction_add(reaction, user):
    if str(reaction.emoji) == "😊" and not user.bot:
        if user.id in confessionUSR:
            del confessionUSR[user.id]  
        dm_message = await user.send("Send your anonymous post here.")
        confessions[user.id] = dm_message.id
        await reaction.message.remove_reaction(reaction.emoji, user)

@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel) and not message.author.bot:
        user_id = message.author.id
        confession = message.content
        
        if user_id not in confessionUSR:  
            await message.author.send("Are you sure you want to submit this post? Reply with 'yes' or 'no'.")
            confessions[user_id] = confession
            confessionUSR[user_id] = confession
            print(confession, "1", confessionUSR, "2")
        else:
            if message.content.lower() == 'yes':
                await message.author.send("Thank you for your post.")
                confessionConfirmed[user_id] = confessions.pop(user_id)  
            elif message.content.lower() == 'no':
                await message.author.send("Okay, feel free to submit your post again.")
                confessions.pop(user_id, None)  
                confessionUSR.pop(user_id, None)
        return  
    
    await bot.process_commands(message)
    
async def check_confession_changes():
    global confessionConfirmed
    while True:
        await asyncio.sleep(1)
        for user_id, wsws in confessionConfirmed.items():
            if wsws:
                channel = discord.utils.get(bot.get_all_channels(), name='general')
                if channel:
                    await channel.send(wsws)
                    confessionConfirmed[user_id] = None  
                else:
                    print('General channel not found.')



