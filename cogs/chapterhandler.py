import requests
import scripts.epic_utils as epic_utils
from discord import Client
from discord.ext import commands, tasks
import os
from scripts.initlog import getLogger
from scripts.getGuildIds import getGuildIds
from cogs.admincommands import admin_command
from discord_slash import cog_ext, SlashContext
import json
import asyncio
import datetime
import pytz

baseurl = "https://onepiecechapters.com"
requesturl = "https://onepiecechapters.com/mangas/5/one-piece"
params = {
    "headers": [
      {
        "name": ":authority",
        "value": "onepiecechapters.com"
      },
      {
        "name": ":method",
        "value": "GET"
      },
      {
        "name": ":path",
        "value": "/mangas/5/one-piece?2022-10-213964"
      },
      {
        "name": ":scheme",
        "value": "https"
      },
      {
        "name": "accept",
        "value": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
      },
      {
        "name": "accept-encoding",
        "value": "gzip, deflate, br"
      },
      {
        "name": "accept-language",
        "value": "en-US,en;q=0.9"
      },
      {
        "name": "cache-control",
        "value": "max-age=0"
      },
      {
        "name": "cookie",
        "value": "__gads=ID=47e019e0fe7889bd-227ed020bbd700b8:T=1666369374:RT=1666369374:S=ALNI_MY1Cq4BDdrvG_O_jlm18P-cs6hOsQ; __gpi=UID=0000088f66034029:T=1666369374:RT=1666369374:S=ALNI_MZh-qAwkk6mRYa8bQwf2ntJdOoICQ; _gid=GA1.2.1954738004.1666369374; _au_1d=AU1D-0100-001666369375-GLKD1W0E-H0NT; _pbjs_userid_consent_data=3524755945110770; _fbp=fb.1.1666369375461.986117323; _cc_id=12de861cde7e7550681cbb004bc504d; panoramaId_expiry=1666974178675; panoramaId=2cdfa70d3756dff7ef79693c5f9d4945a702bdc1e39d1594cd7dc20fa287a63f; _ga_FS7ZSFKXT2=GS1.1.1666369375.1.1.1666369383.0.0.0; _ga_65659PLZ57=GS1.1.1666369374.1.1.1666369383.0.0.0; _au_last_seen_pixels=eyJhcG4iOjE2NjYzNjkzNzUsInR0ZCI6MTY2NjM2OTM3NSwicHViIjoxNjY2MzY5Mzc1LCJhZHgiOjE2NjYzNjkzNzUsImdvbyI6MTY2NjM2OTM3NSwib3BlbngiOjE2NjYzNjkzNzUsInRhYm9vbGEiOjE2NjYzNjkzNzUsImJlZXMiOjE2NjYzNjkzNzUsInBwbnQiOjE2NjYzNjkzNzUsImFkbyI6MTY2NjM2OTM3NSwiaW1wciI6MTY2NjM2OTM4NCwicnViIjoxNjY2MzY5Mzg0LCJtZWRpYW1hdGgiOjE2NjYzNjkzODQsInVucnVseSI6MTY2NjM2OTM4NCwic29uIjoxNjY2MzY5Mzg0LCJzbWFydCI6MTY2NjM2OTM4NH0=; _ga=GA1.2.1754283446.1666369374; FCNEC=%5B%5B%22AKsRol-cAPuTIRhJu32XXZ95BXcCE0oIFb_j2t-7VJxeVl_rxIUiUsNtCWnXb_3HibfuTXYSaYG0LAWPmLjmu84bTV4etlZGiK5J5C5h78o1sdeEuj24ZxrGv7XBEiP4bfICH_bocOBz_taf5KxocclGXMuXYNDuTQ%3D%3D%22%5D%2Cnull%2C%5B%5D%5D"
      },
      {
        "name": "referer",
        "value": "https://onepiecechapters.com/mangas/5/one-piece"
      },
      {
        "name": "sec-ch-ua",
        "value": "\"Not-A.Brand\";v=\"99\", \"Opera GX\";v=\"91\", \"Chromium\";v=\"105\""
      },
      {
        "name": "sec-ch-ua-mobile",
        "value": "?0"
      },
      {
        "name": "sec-ch-ua-platform",
        "value": "\"Windows\""
      },
      {
        "name": "sec-fetch-dest",
        "value": "document"
      },
      {
        "name": "sec-fetch-mode",
        "value": "navigate"
      },
      {
        "name": "sec-fetch-site",
        "value": "same-origin"
      },
      {
        "name": "sec-fetch-user",
        "value": "?1"
      },
      {
        "name": "upgrade-insecure-requests",
        "value": "1"
      },
      {
        "name": "user-agent",
        "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.72"
      }
    ]
}

guild_ids = getGuildIds()

def setup(bot):
    bot.add_cog(ChapterHandler(bot))
    getLogger().log("Extensions.ChapterHandler: setup ext")
    
    
    
class ChapterHandler(commands.Cog):
    def __init__(self, bot: Client):
        self.bot = bot
        self.logger=getLogger()
        self.logger.log("Cogs.ChapterHandler: Initialized cog")
        self.currentChapter: int =self.getLatestChapter()[1]
        self.logger.log("Cogs.ChapterHandler: Current chapter is "+str(self.currentChapter))
        self.chapterLoop.start()
      
    #* Operational Methods  
    def getLatestChapter(self):
      """

      Returns:
          tuple(str, int): link and number of latest chapter
      """
      response = requests.get(url=requesturl,params=params, stream=True)

      for line in response.iter_lines(decode_unicode=True):
          if not line.startswith("<a href=\"/chapters"):
              continue
          quotes = []
          numQuotes = 0
          
          #The link to the chapter is within quotes, so this loop extracts the first expression within quotes
          for ind, char in enumerate(line):
              if numQuotes == 2:
                  break
              if char == "\"":
                  quotes.append(ind)
                  numQuotes +=1
          link: str = baseurl + line[quotes[0]+1:quotes[1]]
          break
      chapNum: int = int(link[-4:])
      return (link,chapNum)
    
    
    #*Task Loop Methods
    @tasks.loop(seconds=15)
    async def chapterLoop(self):
      sentLink = False
      link, num = self.getLatestChapter()
      
      if int(num) > self.currentChapter:
        self.currentChapter = int(num)
        sentLink = True
        with open("settings.json") as f:
          settings = json.load(f)
          for guild,channel in settings["channels"].items():
            await self.bot.get_channel(int(channel)).send(f"Yo new chapter out!\nChapter {num} can be found at {link}")
            
      with open("checklog.txt", "a") as f:
        f.write(f"Checked for new chapter at {datetime.datetime.now()} | current chapter: {self.currentChapter} | Found chapter: {num} | Sent link: {sentLink}" + '\n')
        
    #*User Methods   
    @cog_ext.cog_slash(
      name = "LatestChapter",
      description="Return latest chapter",
      guild_ids=guild_ids
    )
    async def sendChapter(self, ctx: SlashContext):
      
      link, number = self.getLatestChapter()
      
      await ctx.send(f"Chapter {number} can be found at {link} t", hidden=True)
      
    #*Admin Methods
    @commands.command()
    @admin_command
    async def setchapter(self, ctx, chap: int):
      self.currentChapter = int(chap)
      await ctx.send(f"Current chapter set to {chap}")
      
    @commands.command()
    @admin_command
    async def sendlogs(self, ctx, numberOfLogs: int):
      numberOfLogs = int(numberOfLogs)
      
      with open("checklog.txt", "r") as f:
        lines = f.readlines()
        if numberOfLogs > len(lines):
          numberOfLogs = len(lines)
        await ctx.send(f"```{'\n'.join(lines[-numberOfLogs:])}```")
      
      