import discord
import scripts.epic_utils as epic_utils
import discord.ext
from discord.ext import commands
import os
import time
import datetime
from discord_slash import SlashCommand, SlashContext
from discord_slash.context import ComponentContext
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow, wait_for_component
from discord_slash.utils.manage_commands import *
from discord.ext import tasks
import random
from functools import wraps
import shutil
from scripts.initlog import getLogger
import json

def setup(bot):
    bot.add_cog(AdminCommands(bot))
    getLogger().log("Extensions.admincommands: setup ext")

def admin_command(func): #Makes a command into an admin only command
    @wraps(func)
    async def inner(*args):
        ctx=args[1]
        author=ctx.message.author
        argstr=args[3:]
        logger=getLogger()
        
        if author.id in [195984503880024065, 371016632522375172]:
            await func(*args)
            logger.log(f'{func.__name__}{argstr}: admin accessed command')
        else:
            await ctx.send(f"I'm sorry {author.display_name}, I'm afraid I can't do that.")
            logger.log(f'{func.__name__}{argstr}: {author.display_name} tried to access admin command')
            return
    return inner

class AdminCommands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.logger=getLogger()
        
        self.logger.log("Cogs.AdminCommands: Initialized cog")

    @commands.command(pass_context=True)
    @admin_command
    async def exec(self, ctx, code):
        
        def getCog(cog):
            return self.bot.get_cog(cog)
                
        def send(out):
            asyncio.create_task(ctx.send(out))
        
        exec(code)
        
        
    @commands.command(pass_context=True)
    @admin_command
    async def eval(self, ctx, code):
        
        def getCog(cog):
            return self.bot.get_cog(cog)
        
        def slurdle():
            return self.bot.get_cog("Slurdle")
        
        
        
        try:
            await ctx.send(eval(code))
        except:
            eval(code)
            
    @commands.command(pass_context=True)
    @admin_command
    async def synccommands(self, ctx):
        await self.bot.slash.sync_all_commands(True,True)
        await ctx.send("commands synced")


