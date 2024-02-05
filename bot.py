#!/usr/bin/python3.10
import asyncio
import configparser
import collections
from terminaltables import AsciiTable
from pathlib import Path
import re
import time
import random
from random import randint

# Discord Specific
import discord
from discord.ext import commands
from discord.ext.commands import Bot

# Other Scripts
from suslist import *
from dbup import *

##### ### # === = -- -
# Play the stupid clip
##### ### # === = -- -

class msgParse:
    def __init__(self, message, suslist):
        self.message = message
        self.suslist = suslist

    def getReaction(self):
        reactquote = self.message.rjust(1999)
        for stringmatch, reactname in self.suslist:
            rprog = '\s' + stringmatch
            rpattern = re.compile(rprog)
            if rpattern.search(reactquote):
                reactemote = reactname
                print(f"Reacting with emote {reactemote}\n")
                return reactemote

    def badCheckMatch(self):
        badquote = self.message.rjust(1999)
        for stringmatch in self.suslist:
            bprog = '\s' + stringmatch
            bpattern = re.compile(bprog)
            if bpattern.search(badquote, re.IGNORECASE):
                return 1

##### ### # === = -- -
# Read Configs
##### ### # === = -- -
config = configparser.ConfigParser()
config.read('settings.ini')

client = discord.Client(activity=discord.Game(name='definitely not among us'))
bot = commands.Bot(command_prefix="!")

##### ### # === = -- -
# Print Start to Console
##### ### # === = -- -
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})\n\n----------\n')

##### ### # === = -- -
# Actions based on messages
##### ### # === = -- -
@bot.event
async def on_message(ctx):

    if ctx.author.bot: return

    if ctx.content == "hh":
        print(f"lol hh")
        await ctx.reply("hh")

    if "bing chilling" in ctx.content.lower():
        print("bing chilling")
        await ctx.add_reaction("🥶")
        await ctx.add_reaction("🍦")

    if ctx.content == "!help":
        print(f"Help called.")
        await ctx.reply("Voice connectivity works, though FFMPeg bs does not. Don't worry Naiah, he can't make noise anymore.")

    if ctx.content.startswith('!leaderboard'):
        print(f"Request Bad Word Leaderboard")

        if ctx.content == '!leaderboard me':
            # Do function for user current leaderboard standing
            print(f"Criminal Scum: ", ctx.author.id)

            lbdata = []
            lbdata = leaderboardCheck(ctx.author.id,ctx.guild.id)

            await ctx.reply(f"User <@{lbdata[1]}> is currently **#{lbdata[0]}** with a total of **{lbdata[2]}** points.")

        if ctx.content == '!leaderboard all':
            # Do function for top offenders
            print(f"List top offenders")
            # Returns a nested list atm
            lbtop4 = leaderboardTopFour(ctx.guild.id)
            msgData = []
            msgData.append((["Rank","User","Count"]))
            # Build User List with the user IDs returned
            for uids in lbtop4:
                # Take user IDs from the database output from earlier
                userid = int(uids[1])
                # Translate those IDs to usernames similar to Titan#0001
                guildmemid = await ctx.guild.fetch_member(userid)
                #msgData.append(uids[0],guildmemid,uids[2])
                tmpList = [uids[0], guildmemid, uids[2]]
                msgData.append(tmpList)

            table = AsciiTable(msgData)
            msgDone = table.table
            await ctx.reply(f"**Leaderboard**\n ```\n{msgDone}```\nYou should be ashamed.")

        if ctx.content == '!leaderboard':
            await ctx.reply("Please use either `!leaderboard me` or `!leaderboard all`.")

    # RNG Insult
    insultchance = randint(1,2000)
    if insultchance == 1:
        with open('insults') as insultlist:
            insult = insultlist.read().splitlines()
            randominsult = random.choice(insult)
            await ctx.reply(f"{randominsult}")

    # Parse Message
    parsemsg = ctx.content.lower()

##### ### # === = -- -
# No-no word counter
##### ### # === = -- -

    # print(ctx.content)
    # Bad Word Check first and foremost
    badCheck = msgParse(parsemsg, countmsg)
    badThing = badCheck.badCheckMatch()

    if badThing == 1:
        print("Bad word detected for user: ", ctx.author.id)
        badwordlog = open("badword.log", "a")
        badwordlog.write(f"User: {ctx.author.id}\nGuild: {ctx.guild.id}\n------\n{ctx.content}\n##### ### # === = -- -\n")
        incrementCount(ctx.author.id,ctx.guild.id)
        time.sleep(1)
        await ctx.delete()
        print("Deleted Bad Word by User ID ", ctx.author.id)

##### ### # === = -- -
# Emote Reactions
##### ### # === = -- -

    # Reacting to messages
    reactCheck = msgParse(parsemsg, reactmsg)
    reactThing = reactCheck.getReaction()

    # Doing things based on message triggers
    if reactThing is not None:
        await ctx.add_reaction(reactThing)

##### ### # === = -- -
# The Anti-Crim Section
##### ### # === = -- -
@bot.event
async def on_message_edit(beforectx, afterctx):

    editedmsg = afterctx.content

    # Bad Word Check first and foremost
    badCheck = msgParse(editedmsg, countmsg)
    badThing = badCheck.badCheckMatch()

    if badThing == 1:
        print("Bad word detected for user: ", afterctx.author.id)
        badwordlog = open("badword.log", "a")
        badwordlog.write(f"User: {afterctx.author.id}\nGuild: {afterctx.guild.id}\n------\n***Edited Content***\n{afterctx.content}\n##### ### # === = -- -\n")
        incrementCount(afterctx.author.id,afterctx.guild.id)
        time.sleep(1)
        await afterctx.delete()
        print("Deleted Bad Word by User ID ", afterctx.author.id)

bot.run(config['discord']['token'])