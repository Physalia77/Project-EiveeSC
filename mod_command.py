# Moderator commands
import datetime
import json
from datetime import datetime

import discord
import discord.utils
import asyncio

# pip install pyfiglet
import pyfiglet
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from discord.ext.commands import Bot
from configparser import ConfigParser

# Config File
file = 'config.ini'
config = ConfigParser()
config.read(file)
phy = "316673884172582922"
scream = "355056076862914561"


class Moderation(commands.Cog):
    """
    Moderations commands for moderators and admins
    """

    def __init__(self, Bot):
        self.bot = Bot

    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    # Moderator commands
    # Kick
    @commands.command(name='kick', description='[member] (optional reason)')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason=None):
        """Kicks a member from the server, they can return to the server with a new invite."""
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

    """
    ChatGPT code for temp/perm ban and mute + error handler
    """

    def parse_time(self, time):
        if "s" in time or "second" in time:
            return datetime.timedelta(seconds=int(time.strip("s").strip("second")))
        elif "m" in time or "minute" in time:
            return datetime.timedelta(minutes=int(time.strip("m").strip("minute")))
        elif "h" in time or "hour" in time:
            return datetime.timedelta(hours=int(time.strip("h").strip("hour")))
        elif "d" in time or "day" in time:
            return datetime.timedelta(days=int(time.strip("d").strip("day")))
        elif "w" in time or "week" in time:
            return datetime.timedelta(weeks=int(time.strip("w").strip("week")))
        elif "y" in time or "year" in time:
            return datetime.timedelta(days=int(time.strip("y").strip("year")) * 365)
        else:
            return None

    @commands.command()
    async def mute(self, ctx, member: discord.Member, *, duration=None):
        if duration:
            duration = self.parse_time(duration)
            if duration:
                role = discord.utils.get(ctx.guild.roles, name="Mute")
                await member.add_roles(role)
                await ctx.send(embed=discord.Embed(description=f'{member.mention} has been muted for {duration}.'))
                await asyncio.sleep(duration)
                await member.remove_roles(role)
                await ctx.send(embed=discord.Embed(description=f'{member.mention} has been unmuted.'))
            else:
                await ctx.send(embed=discord.Embed(
                    description="Invalid time format. Please use s, m, h, d, or y for seconds, minutes, hours, days, or years respectively."))
        else:
            role = discord.utils.get(ctx.guild.roles, name="Mute")
            await member.add_roles(role)
            await ctx.send(embed=discord.Embed(description=f'{member.mention} has been permanently muted.'))

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, duration=None):
        if duration:
            duration = self.parse_time(duration)
            if duration:
                await member.ban()
                await ctx.send(embed=discord.Embed(description=f'{member.mention} has been banned for {duration}.'))
                await asyncio.sleep(duration)
                await member.unban()
                await ctx.send(embed=discord.Embed(description=f'{member.mention} has been unbanned.'))
            else:
                await ctx.send(embed=discord.Embed(
                    description="Invalid time format. Please use s, m, h, d, or y for seconds, minutes, hours, days, or years respectively."))
        else:
            await member.ban()
            await ctx.send(embed=discord.Embed(description=f'{member.mention} has been permanently banned.'))

    """
    ChatGPT Code ends for temp/perm ban and mute command with error handler
    """

    # Unban

    @commands.command(name='unban', pass_context=True, description='[member]')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member: discord.Member = None):
        """Unban a member form the server"""
        banned_user = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        for ban_entry in banned_user:
            user = ban_entry.user

            if member == None:
                return await ctx.message.channel.send(
                    embed=discord.Embed(
                        description=f'**{ctx.message.author}**, please mention somebody to ban.', color=0xFFC200))

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                log_channel = Bot.get_channel(902599258857955348)
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
    @commands.command(name='mute', description='[member] (optional reason)')
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member = None, *, reason=None):
        """Mute a member in the server"""
        log_channel = Bot.get_channel(902599258857955348)
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
    @commands.command(name='unmute', pass_context=True, description='[member]')
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member):
        """Unmute a member in the server """
        muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
        log_channel = Bot.get_channel(902599258857955348)

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
    @commands.command(aliases=["msgclear"], description='[amount]')
    @commands.has_permissions(kick_members=True)
    async def clear(self, ctx, amount):
        amount = int(amount)
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"{amount} messages deleted!", delete_after=5)

    # Check bots ping
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def ping(self, ctx):
        """Pings the bot to check the bot's latency"""
        await ctx.send(f'**Pong!** {round(self.bot.latency * 1000)}ms ')

    """
    @commands.command(name='r')
    async def r(self, ctx, *, reason=None):
        await bot.get_channel(784414610027446292).send(embed=discord.Embed(description=f"{ctx.message.author} "
                                                                                       f"\n **Reported:** " + reason))
    """

    @commands.command(description='[new prefix]')
    @commands.has_permissions(administrator=True)
    async def changeprefix(self, ctx, prefix):
        """Change the prefix for commands to anything you would like"""
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def invite(self, ctx):
        """Sends a nice invite link"""
        await ctx.message.delete()
        # Creating an invite link
        link = await ctx.channel.create_invite(xkcd=True, max_age=0, max_uses=0)
        # max_age = 0 The invite link will never exipre.
        # max_uses = 0 Infinite users can join throught the link.
        # -----------------------------------------------------#

        # -------Embed Time-----#
        em = discord.Embed(title=f"Join The {ctx.guild.name} Discord Server Now!", url=link,
                           description=f"**{ctx.guild.member_count} Members** [**JOIN**]({link})\n\n**Invite link for {ctx.channel.mention} is created.**\nNumber of uses: **Infinite**\nLink Expiry Time: **Never**",
                           color=0x303037)

        # Embed Footer
        em.set_footer(text=f"Made by </{ctx.message.author}")

        # Embed Thumbnail Image
        em.set_thumbnail(url=ctx.guild.icon_url)

        # Embed Author
        em.set_author(name="INSTANT SERVER INVITE")
        # -----------------------------------------#
        await ctx.send(f"> {link}", embed=em)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rules(self, ctx):
        await ctx.message.delete()

        def rules_message():
            print(f"Sending Rules.Embed to #Rules \n Channel ID: {cid}")
            global rules_embed
            rules_embed = discord.Embed(
                title='RULES & INFORMATION',
                description="Welcome to Eivee's Community Discord server, here you can get support, help and chat with new people or even come up with new ideas to Eivee! \n",
                color=discord.Color.purple())
            rules_embed.add_field(name='\u200b',
                                  value="These rules includes to all channels and Voice-Channels!!! \nFollow the rules as good you can or there can be consequences or just a warning depending on the situation",
                                  inline=False)
            rules_embed.add_field(name="\u200b", value="\u200b")
            rules_embed.add_field(name="`[1]` No spamming",
                                  value='```This includes mentioning a user repeatedly \nSending same message multiple times '
                                        '\nUnnecessary spam of meaning less letters, symbols and numbers, for example "nbtue9567434je#¤%&/("```',
                                  inline=False)
            rules_embed.add_field(name="`[2]` No NSFW content",
                                  value='```For example half/fully nude pictures \nAdult content```', inline=False)
            rules_embed.add_field(name="`[3]` Use common sense",
                                  value='```Do not annoy or tick off the mods \nFollow the Discord TOS (Terms Of Service)```',
                                  inline=False)
            rules_embed.add_field(name="`[4]` Discord TOS",
                                  value='```Follow the Discord TOS (Terms Of Service), if you do not know what the TOS says then you can read about it in the link that you find in the end of this embed!```',
                                  inline=False)
            rules_embed.add_field(name="`[5]` Use channels for their purpose",
                                  value='```Try to use the channels for their purpose and nothing else, if you are not sure'
                                        ' what channel to go to then we recommend you to read the channel description. '
                                        'You can find them either here further down or in the top of each channel```')
            rules_embed.add_field(name="`[6]` Keep chats in same language", inline=False,
                                  value='```We want all chats to be either in English or Swedish, to make it easier for the staff to moderate and keep the chats in a good level.```')
            rules_embed.add_field(name="\u200b", value="\u200b")
            rules_embed.add_field(name="Discord TOS (Terms Of Service)", inline=False,
                                  value="[TOS](https://discord.com/terms)")
            rules_embed.set_footer(text='In progress...')
            rules_embed.set_thumbnail(url=ctx.guild.icon_url)

        if ctx.message.author.id == phy or ctx.message.author.id == scream:
            server_id = ctx.message.guild.id
            if channeli := discord.utils.get(ctx.guild.text_channels, name="rules"):
                cid = channeli.id
                print(cid)
                """channel = Bot.get_channel(cid)"""
                print(f'Channel #Rules´already exist in server, server ID: {server_id}')
                rules_message()
                await self.bot.get_channel(cid).send(embed=rules_embed)
            else:
                channeli = await ctx.guild.create_text_channel('rules')
                cid = channeli.id
                rules_message()
                await self.bot.get_channel(cid).send(embed=rules_embed)
        else:
            return


def setup(bot):
    bot.add_cog(Moderation(bot))
