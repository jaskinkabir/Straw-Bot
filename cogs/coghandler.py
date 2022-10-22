import scripts.epic_utils as epic_utils
from discord.ext import commands
import os
from scripts.initlog import getLogger
from cogs.admincommands import admin_command



def setup(bot):
    bot.add_cog(CogHandler(bot))
    getLogger().log("Extensions.coghandler: setup ext")
    
class CogHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger=getLogger()
        self.logger.log("Cogs.CogHandler: Initialized cog")
    
    def initializeCogs(self):
        self.logger.log("------------------------cogInitializer():Initializing Extensions and Cogs------------------------")
        cogTimer=epic_utils.runTimer()
        cogTimer.start() 
        for filename in os.listdir('./cogs'): #Initialize extensions/cogs
            if filename=="coghandler.py" or not filename.endswith('.py'):
                continue
            self.bot.load_extension(f'cogs.{filename[:-3]}')
        cogTimer.end() 
        self.logger.log(f"cogInitializer(): Took {cogTimer.timeToFinish()} seconds to complete")
        self.logger.log("------------------------cogInitializer():Initialized Extensions and Cogs------------------------")
    
    @commands.command()
    @admin_command
    async def load(self, ctx, extension):
        self.bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"Loaded extension {extension}")

    @commands.command()
    @admin_command
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f"Unloaded extension {extension}")

    @commands.command()
    @admin_command
    async def reload(self, ctx, extension):
        self.bot.reload_extension(f"cogs.{extension}")
        await ctx.send(f"Reloaded extension {extension}")
    

