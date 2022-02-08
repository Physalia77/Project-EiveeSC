import discord
import datetime
from datetime import datetime
import self as self
from discord.ext import commands, tasks
from discord.ext.commands import bot
import tracemalloc
import random
import asyncio
import json
import discord.utils
import os
import aiocron
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from inspect import currentframe, getframeinfo
import sys
from dislash import InteractionClient, ActionRow, Button, ButtonStyle
from discord.utils import find, get
import os.path
import module
import youtube_dl
from discord.ext.commands import MissingPermissions
import time
import threading
from itertools import cycle
# pip install pyfiglet
import pyfiglet
from termcolor import colored
import schedule
import sqlite3

"""
All commands for The Knight Bot
"""


def get_prefix(message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


class cogs(commands.Cog):
    def __init__(self, Bot):
        self.bot = Bot

    # Commands
    # Setup command
    @commands.command(name="setup1", aliases=["setup"])
    async def setup1(self, ctx):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        print(
            f'{datetime.now()}: {ctx.message.author} executed command - {prefixes[str(ctx.guild.id)]}{ctx.invoked_with}')
        guild = ctx.guild
        server_id = ctx.message.guild.id
        for guild in bot.guilds:
            if discord.utils.get(guild.text_channels, name="bot-chat"):
                def v0():
                    channel = discord.utils.get(ctx.guild.channels, name="bot-chat")
                    bot_chat_id = channel.id
                    print(f"ID for channel #Quote {bot_chat_id}")

                print(f'Channel #bot-chat´already exist in server, server ID: {server_id}')
                await ctx.send("There is already a channel in this server with the name 'bot-chat'")
                v0()
            else:
                create_channel = await guild.create_text_channel('bot-chat')
                print(create_channel.id)

            if discord.utils.get(guild.text_channels, name="quotes"):
                def v1():
                    channel = discord.utils.get(ctx.guild.channels, name="quotes")
                    quote_id = channel.id
                    print(f"ID for channel #Quote {quote_id}")

                await ctx.send("There is already a channel in this server with the name 'quotes'")
                print(f'Channel #quotes already exist in server, server ID: {server_id}')
                v1()
            else:
                q_channel = await guild.create_text_channel('quotes')
                print(q_channel.id)

    """    
    # The quote command
    @commands.command(aliases=["q"])
    async def quote(self, ctx, *, text):
        await bot.get_channel()

    # Member count command
    @commands.command()
    async def members(self, ctx):
        id_s = bot.get_guild(764500927808798781)
        await ctx.send(f"# of Members: {id_s.member_count}")
    """

    # test with buttons

    # Help command
    """ 
    @commands.command(description=f"Help page for all related topics you could need help with around Eivee")  # Help command, command list
    async def help(self, ctx):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        embed = discord.Embed(title="Eivee's help command",
                              description=f" page for all related topics you could need help with around {self.bot.user.name}", color=0x3457db)
        for command in bot.walk_commands():
            description = command.description
            if not description or description is None or description == "":
                description = 'No description provided'
            embed.add_field(
                name=f"`{prefixes[str(ctx.guild.id)]}{command.name}{command.signature if command.signature is not None else ''}`", value=description)
            embed.timestamp = datetime.utcnow()
            embed.set_footer(text='\u200b')
        await ctx.send(embed=embed)
    """

    #   Server Information
    @commands.command(name="serverinfo", aliases=["server", "sinfo"])
    async def serverinfo(self, ctx):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        print(
            f'{datetime.now()}: {ctx.message.author} executed command - {prefixes[str(ctx.guild.id)]}{ctx.invoked_with}')
        name = str(ctx.guild.name)
        description = str(ctx.guild.description)

        owner = str(ctx.guild.owner)
        server_id = str(ctx.guild.id)
        region = str(ctx.guild.region)
        member_count = str(ctx.guild.member_count)

        icon = str(ctx.guild.icon_url)

        embed = discord.Embed(
            title=name + " Server Information",
            description=description,
            color=0x3457db
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner:", value=owner, inline=True)
        embed.add_field(name="Server ID:", value=server_id, inline=True)
        embed.add_field(name="Region:", value=region, inline=True)
        embed.add_field(name="Member Count:", value=member_count, inline=True)

        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def welcome(self, ctx):
        await ctx.send('Available Setup Commands \nwelcome channel <#channel>\nwelcome text <message>')

    @welcome.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('testdb.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = "INSERT INTO main (guild_id, channel_id) VALUES(?,?)"
                val = (ctx.guild.id, channel.id)
                await ctx.send(f"Channel has been set to {channel.mention}")
            elif result is not None:
                sql = "UPDATE main  SET channel_id = ? WHERE guild_id = ?"
                val = (ctx.guild.id, channel.id)
                await ctx.send(f"Channel has been updated to {channel.mention}")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    @welcome.command()
    async def channel(self, ctx, *, text):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('testdb.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT msg FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = "INSERT INTO main (guild_id, msg) VALUES(?,?)"
                val = (ctx.guild.id, text)
                await ctx.send(f"Message has been set to `{text}`")
            elif result is not None:
                sql = "UPDATE main  SET msg = ? WHERE guild_id = ?"
                val = (ctx.guild.id, text)
                await ctx.send(f"Message has been updated to `{text}`")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()


def setup(bot):
    bot.add_cog(cogs(bot))
