import os
import json

from pathlib import Path
from dotenv import load_dotenv
from os.path import join, dirname
from twitchio.ext import commands

dir_path = os.path.dirname(os.path.realpath(__file__))
dotenv_path = join(dir_path, '.env')
load_dotenv(dotenv_path)

# credentials
TMI_TOKEN = os.environ.get('TMI_TOKEN')
CLIENT_ID = os.environ.get('CLIENT_ID')
BOT_NICK = os.environ.get('BOT_NICK')
BOT_PREFIX = os.environ.get('BOT_PREFIX')
CHANNEL = os.environ.get('CHANNEL')

JSON_FILE = str(os.path.dirname(os.path.realpath(__file__))) + '/data.json'

bot = commands.Bot(
    irc_token=TMI_TOKEN,
    client_id=CLIENT_ID,
    nick=BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=[CHANNEL]
)

@bot.event
async def event_ready():
    """ Runs once the bot has established a connection with Twitch """
    print(f"{BOT_NICK} is online!")

@bot.event
async def event_message(ctx):
    """ 
    Runs every time a message is sent to the Twitch chat and relays it to the 
    command callbacks 
    """

    # log all messages
    log_messages(ctx)
    
    # the bot should not react to itself
    if ctx.author.name.lower() == BOT_NICK.lower():
        return
    
    # relay message to command callbacks
    await bot.handle_commands(ctx)

@bot.command(name='asmr')
async def asmr_notif(ctx):
    """
    Explains the premise of the stream
    """
    await ctx.send("""No facecam or mic. Pure, Unadulterated, Raw, Mario.""")

@bot.command(name='route')
async def route_notif(ctx):
    """
    Explains the currently ran route
    """
    await ctx.send("""Currently running the beginner route, though I'm working on more advanced strats.
                        https://ukikipedia.net/wiki/RTA_Guide/16_Star#Beginner_Guide""")

@bot.command(name='timesave')
async def timesave_notif(ctx):
    """
    Explains the current possible time saves
    """
    await ctx.send("""I'm horribly inconsistent and also currently running the beginner route, so timesaves are everywhere in the run. Specifically,
                        Cannonless, Owlless, Bowser 1 Reds, MIPS clips, and Bowser 3.""")

@bot.command(name='so')
async def shoutout(ctx):
    """
    Shoutout streamer channel
    """
    # check if user who issued the command is a mod
    if(ctx.author.is_mod):

        # parse add command
        command_string = ctx.message.content
        # remove '!add' and white space
        command_string = command_string.replace('!so', '').strip()
        if command_string is None:
            return
        streamer_url = f"https://www.twitch.tv/{command_string}" 

        await ctx.send(f'Hey, you should check out @{command_string} over at {streamer_url}')

def log_messages(ctx):
    with open('log.txt', 'a+') as f:
        f.write(f">>>{ctx.author.name}:{ctx.content}'\n'")
        
if __name__ == "__main__":
    # launch bot
    bot.run()
