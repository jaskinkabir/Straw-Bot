import scripts.epic_utils as epic_utils
from scripts.initlog import getLogger
import logging

logging.basicConfig(level=logging.ERROR)

logger=getLogger()
startupTimer=epic_utils.runTimer()

startupTimer.start()
logger.log("------------------------Beginning Startup Sequence------------------------") 

import discord
import discord.ext
from discord.ext import commands
from discord_slash import SlashCommand
import json

with open ("./settings.json") as settingsfile: #Setup bot object according to settings.json
    settings = json.load(settingsfile)



if settings['testing']:
    token = settings['tokentest']
    bot = commands.Bot(command_prefix = settings['prefixtest'], help_command=None, intents=discord.Intents.default())
else:
    token = settings['token']
    bot = commands.Bot(command_prefix = settings['prefix'], help_command=None, intents=discord.Intents.default())

setattr(bot, 'embedColor', discord.Color(int(settings['embedcolor'], base=16)))

logger.log("Initialized settings")

slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True) #Initialize slashcommand object

@bot.event
async def on_ready():
    bot.load_extension("cogs.coghandler") #Initialize cogs
    bot.get_cog("CogHandler").initializeCogs()
    await bot.get_channel(860332677852037153).send('startup complete') 
    startupTimer.end()
    logger.log(f"Startup took {startupTimer.timeToFinish()} seconds to complete")
    logger.log("------------------------Startup Sequence Completed------------------------")
    
    
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


bot.run(token)