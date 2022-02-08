# Moderator commands
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


class cogs(commands.Cog):
    def __init__(self, Bot):
        self.bot = Bot

    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    # Moderator commands
    # Kick
    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason=None):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        print(
            f'{datetime.now()}: {ctx.message.author} executed command - {prefixes[str(ctx.guild.id)]}{ctx.invoked_with}')

        if member is None:
            await ctx.message.channel.send(
                embed=discord.Embed(
                    description=f'**{ctx.message.author}**, please mention somebody to kick.', color=0xFFC200))

        elif member == ctx.message.author:
            await ctx.message.channel.send(
                embed=discord.Embed(
                    description=f"**{ctx.message.author}**, you cannot kick yourself.", color=0xFFC200))

        elif member == member.bot:
            await ctx.message.channel.send(
                embed=discord.Embed(
                    description=f"You can not kick **" + format(member) + "** bots.".format(member),
                    color=0xFFC200))
        else:
            if member.dm_channel is None:
                await member.create_dm()
            await member.dm_channel.send(
                embed=discord.Embed(
                    description=f'You have been kicked from **{ctx.guild}** by **{ctx.message.author}**. \n '
                                f'**Reason:** {reason} ', color=0xf30000))
            await member.kick()
            log = discord.Embed(
                description='User **' + member.display_name + f'** has been kicked by **{ctx.message.author}**'
                                                              f'. \n **Reason:** {reason}',
                color=0xf30000)
            await ctx.send(embed=log)
            print(
                'User **' + member.display_name + f'** has been kicked by **{ctx.message.author} from guild {ctx.guild}**. \n **Reason:** {reason}')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            error_kick = discord.Embed(description="You don't have permission to ban members:exclamation:",
                                       color=0xFFC200)
            await ctx.message.channel.send(embed=error_kick)

    # Ban
    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason=None):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        print(
            f'{datetime.now()}: {ctx.message.author} executed command - {prefixes[str(ctx.guild.id)]}{ctx.invoked_with}')

        Staff = discord.utils.get(ctx.guild.roles, name='Staff')

        if member == None:
            return await ctx.message.channel.send(
                embed=discord.Embed(
                    description=f'**{ctx.message.author}**, please mention somebody to ban.', color=0xFFC200))

        if member == ctx.message.author:
            return await ctx.message.channel.send(
                embed=discord.Embed(
                    description=f"**{ctx.message.author}**, you cannot ban yourself, silly.", color=0xFFC200))

        if member.bot:
            return await ctx.message.channel.send(
                embed=discord.Embed(
                    description=f"You can not ban **" + format(member) + "** because the member is a bot.".format(
                        member),
                    color=0xFFC200))

        if Staff in member.roles:
            return await ctx.message.channel.send(
                embed=discord.Embed(
                    description=f"**{ctx.message.author}**, you can't ban another staff member. :warning:",
                    color=0xFFC200))

        if member.dm_channel is None:
            await member.create_dm()
        await member.dm_channel.send(embed=discord.Embed(
            description=f"You have been banned from **{ctx.guild}** by **{ctx.message.author}** \n **Reason:** {reason} ",
            color=0xf30000))

        await member.ban(reason=reason)
        ban_log = discord.Embed(description=f'User **' + member.display_name + f'** has been banned by '
                                                                               f'**{ctx.message.author}**.'
                                                                               f' \n **Reason:** ' + reason,
                                color=0xf30000)

        a_log_channel = bot.get_channel(902599258857955348)
        await a_log_channel.send(embed=ban_log)
        await ctx.send(embed=ban_log)
        print(f'User **' + member.display_name + f'** has been banned by '
                                                 f'**{ctx.message.author}**.'
                                                 f' \n **Reason:** ' + reason)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            error_ban = discord.Embed(description="You don't have permission to ban members :warning:", color=0xFFC200)
            await ctx.message.channel.send(embed=error_ban)

    # Unban
    @commands.command(name='unban', pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member: discord.Member = None):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        print(
            f'{datetime.now()}: {ctx.message.author} executed command - {prefixes[str(ctx.guild.id)]}{ctx.invoked_with}')

        banned_user = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        for ban_entry in banned_user:
            user = ban_entry.user

            if member == None:
                return await ctx.message.channel.send(
                    embed=discord.Embed(
                        description=f'**{ctx.message.author}**, please mention somebody to ban.', color=0xFFC200))

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                log_channel = bot.get_channel(902599258857955348)
                await ctx.guild.unban(user)
                embed = discord.Embed(description=f"**{ctx.message.author}** unbanned {user.mention}!")
                save_log_unban = discord.Embed(description=f"**{ctx.message.author}** unbanned {user.mention}!")
                await ctx.send(embed=embed)
                await log_channel.send(embed=save_log_unban)
                print(f"**{ctx.message.author}** unbanned {user.mention}!")
                return

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            error_unban = discord.Embed(description="You don't have permission to ban members :warning:",
                                        color=0xFFC200)
            await ctx.message.channel.send(embed=error_unban)

    # Mute
    @commands.command(name='mute')
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member = None, *, reason=None):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        print(
            f'{datetime.now()}: {ctx.message.author} executed command - {prefixes[str(ctx.guild.id)]}{ctx.invoked_with}')

        log_channel = bot.get_channel(902599258857955348)
        add_role = discord.utils.get(ctx.guild.roles, name='Muted')

        if member == None:
            return await ctx.message.channel.send(
                embed=discord.Embed(
                    description=f'**{ctx.message.author},** please mention somebody to mute.', color=0xFFC200))

        if member == ctx.message.author:
            return await ctx.message.channel.send(
                embed=discord.Embed(
                    description=f"**{ctx.message.author},** you cannot mute yourself, silly.", color=0xFFC200))

        if member.bot:
            return await ctx.message.channel.send(
                embed=discord.Embed(
                    description=f"You can not mute **" + format(member) + "** because the member is a bot.".format(
                        member),
                    color=0xFFC200))

        if add_role in member.roles:
            return await ctx.message.channel.send(
                embed=discord.Embed(
                    description="**{}** is already muted. :warning:".format(member), color=0xFFC200))

        else:
            await member.add_roles(add_role, reason=reason)
            mute_log = discord.Embed(description=f'User {member.display_name} has been muted. \n**Reason:** '
                                                 f'{reason if reason is not None else "None"}', color=0xf30000)
            await ctx.send(embed=mute_log)
            await log_channel.send(embed=mute_log)
            print(
                f'User {member.display_name} has been muted. \n**Reason:** {reason if reason is not None else "None"}')

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            error_mute = discord.Embed(description="You don't have permission to ban members :warning:",
                                       color=0xFFC200)
            await ctx.message.channel.send(embed=error_mute)

    # Un mute
    @commands.command(name='unmute', pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        print(
            f'{datetime.now()}: {ctx.message.author} executed command - {prefixes[str(ctx.guild.id)]}{ctx.invoked_with}')

        muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
        log_channel = bot.get_channel(902599258857955348)

        guild = ctx.guild
        user = member

        if member == None:
            await ctx.send(f'**{ctx.message.author},** please mention somebody to unmute.')
            return

        if member == ctx.message.author:
            await ctx.send(f'**{ctx.message.author},** wtf... what do u mean bro.')
            return

        for role in guild.roles:
            if role.name == "Muted":
                if role in user.roles:
                    await member.remove_roles(muted_role)
                    unmute_log = discord.Embed(
                        description='User **' + member.display_name + '** have been unmuted. ',
                        color=0xf30000)
                    await ctx.send(embed=unmute_log)
                    await log_channel.send(embed=unmute_log)
                    print(f'User **' + member.display_name + '** have been unmuted.')
                    return
                else:
                    await ctx.send(f"Can't mute **{ctx.message.author}** because he/she is not muted.")

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            error_unmute = discord.Embed(description="You don't have permission to unmute members :warning:",
                                         color=0xFFC200)
            await ctx.message.channel.send(embed=error_unmute)

    # clear [Amount] messages
    @commands.command(aliases=["msgclear"])
    @commands.has_permissions(kick_members=True)
    async def clear(self, ctx, amount):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        print(
            f'{datetime.now()}: {ctx.message.author} executed command - {prefixes[str(ctx.guild.id)]}{ctx.invoked_with}')

        amount = int(amount)
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"{amount} messages deleted!", delete_after=5)
        print(f"{amount} messages deleqed!")

    # Check bots ping
    @commands.command()
    async def ping(self, ctx):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        print(
            f'{datetime.now()}: {ctx.message.author} executed command - {prefixes[str(ctx.guild.id)]}{ctx.invoked_with}')

        await ctx.send(f'**Pong!** {round(self.bot.latency * 1000)}ms ')

    """
    @commands.command(name='r')
    async def r(self, ctx, *, reason=None):
        await bot.get_channel(784414610027446292).send(embed=discord.Embed(description=f"{ctx.message.author} "
                                                                                       f"\n **Reported:** " + reason))
    """

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def changeprefix(self, ctx, prefix):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        print(
            f'{datetime.now()}: {ctx.message.author} executed command - {prefixes[str(ctx.guild.id)]}{ctx.invoked_with}')

        with open('../json/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('../json/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)




def setup(bot):
    bot.add_cog(cogs(bot))
