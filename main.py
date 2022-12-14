import json
import os.path
from configparser import ConfigParser
from inspect import currentframe, getframeinfo

import discord
import discord.utils
# pip install pyfiglet
import pyfiglet
import self as self
from discord.ext import commands
from discord.ext.commands import bot
from termcolor import colored

"""Project: Eivee-SC/(Source Code)"""


# Open Prefix.JSON
def get_prefix(bot, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


# Client/bot

bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, Intents=discord.Intents.all)

# Variables
traceback = True
dir_path = os.path.dirname(os.path.realpath(__file__))
initial_extensions = []
"""extensions = ['casino', 'commands', 'vc_commands', 'discord_events', 'mod_command']
"""
bot.remove_command('help')

# Config File

# Get script path
os.chdir(dir_path)

# Help Sub Command
with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

"""# Commands
@bot.command(
    description=f"Help page for all related topics you could need help with around Eivee")  # Help command, command list
async def help_all(ctx):
    embed = discord.Embed(title="Eivee's help command",
                          description=f" page for all related topics you could need help with around {bot.user.name}",
                          color=0x3457db)
    for command in bot.walk_commands():
        description = command.description
        if not description or description is None or description == "":
            description = "No description provided"
        embed.add_field(
            name=f"`{prefixes[str(ctx.guild.id)]}{command.name}{command.signature if command.signature is not None else ''}`",
            value=description)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text='\u200b')
    await ctx.send(embed=embed)


@bot.command(
    description=f"Help page for all related topics you could need help with around Eivee")  # Help command, command list
async def help(ctx):
    embed = discord.Embed(title="Eivee's help command",
                          description=f" page for all related topics you could need help with around {bot.user.name}",
                          color=0x3457db)
    for command in bot.walk_commands():
        description = command.description
        if not description or description is None or description == "":
            description = 'No description provided'
        embed.add_field(
            name=f"`{prefixes[str(ctx.guild.id)]}{command.name}{command.signature if command.signature is not None else ''}`",
            value=description)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text='\u200b')
    await ctx.send(embed=embed)
"""

"""COGS/EXTENSIONS"""


@bot.command(name="check_cogs", aliases=["check cog", "cc"],
             descreption="Look if cog/extension is loaded or not.")
async def check_cogs(ctx, cog_name):
    try:
        bot.load_extension(f"cogs.{cog_name}")
    except commands.ExtensionAlreadyLoaded:
        await ctx.send("Cog is loaded")
    except commands.ExtensionNotFound:
        await ctx.send("Cog not found")
    else:
        await ctx.send("Cog is unloaded")
        bot.unload_extension(f"cogs.{cog_name}")


# Load cog/extension
@bot.command(name="load", description="Enable a specific extension")
async def load(ctx, extension=None):
    if extension is None:
        await ctx.send(
            embed=discord.Embed(title=f"Error: Arg extension missing [{getframeinfo(currentframe()).lineno}]",
                                description="You have to name an extension that you want to enable", color=0xF30000,
                                delete_after=7))
    else:
        try:
            bot.load_extension(extension)
            print(f'loaded. {format(extension)}')
            await ctx.send(embed=discord.Embed(title=f"Enabled `{format(extension)}`",
                                               description=f"Extension `{format(extension)} was successfully enabled",
                                               color=0xF30000, delete_after=7))
        except Exception as error:
            print(colored(f'{format(extension)} cannot be loaded. [{format(error)}]', 'red'))
            await ctx.send(embed=discord.Embed(title=f"Error: `{getframeinfo(currentframe()).lineno}`",
                                               description=f'{format(extension)} cannot be loaded. [{format(error)}]',
                                               color=0xF30000, delete_after=7))


# unLoad cog/extension
@bot.command(name="unload", description="Disable a specific extension")
async def unload(ctx, extension=None):
    if extension is None:
        await ctx.send(
            embed=discord.Embed(title=f"Error: Arg extension missing [{getframeinfo(currentframe()).lineno}]",
                                description="You have to name an extension that you want to disable", color=0xF30000,
                                delete_after=7))
    else:
        try:
            bot.unload_extension(extension)
            print(f'Unloaded. {format(extension)}')
            await ctx.send(embed=discord.Embed(title=f"Disabled `{format(extension)}`",
                                               description=f"Extension `{format(extension)} was successfully disabled",
                                               color=0xF30000, delete_after=7))
        except Exception as error:
            print(colored(f'{format(extension)} cannot be unloaded. [{format(error)}]', 'red'))
            await ctx.send(embed=discord.Embed(title=f"Error: `{getframeinfo(currentframe()).lineno}`",
                                               description=f'{format(extension)} cannot be loaded. [{format(error)}]',
                                               color=0xF30000, delete_after=7))


# Bot status
"""
total_members_count = len(bot.users)

status = [f"Member count: {total_members_count}", "Defualt help command: ?help",
          f"{self.bot.user.name} is in {len(bot.guilds)} servers!"]


async def change_status():
    await bot.wait.until_ready
    msgs = cycle(status)

    while not bot.is_bot:
        current_status = next(msgs)
        await bot.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep()
"""

for filename in os.listdir('./'):
    if filename.endswith('.py') and filename != "main.py":
        initial_extensions.append(filename[:-3])

o = 0
if __name__ == '__main__':
    print(f'\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    print()

    ascii_banner = pyfiglet.figlet_format("EIVEE")
    print(colored(ascii_banner, "magenta"), end="")
    print()
    print(f'\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    print()
    print("Existing COGS:")
    nr = 0
    for extension in initial_extensions:
        # noinspection PyInterpreter
        try:
            bot.load_extension(extension)
            nr += 1
            print(f"    COG #{nr} {format(extension)}")
        except Exception as error:
            print()
            print(colored(f'{format(extension)} cannot be loaded. [{format(error)}]', 'red'))

    commands_list = [c.name for c in bot.commands]
    print(f'\nCommand List:', ', '.join(commands_list))

    """bot.loop.create0_task((change_status()))"""
    bot.run('OTAyNjA2MzM2NzgzNjgzNTg1.GAVD16.m1m-dx406UP5qu31rIEo6X1S3idNdEW6WUk-LY')
