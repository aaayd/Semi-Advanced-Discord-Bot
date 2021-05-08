#!/usr/bin/env python

import os, os.path, sys
from discord.ext import commands
from discord import Intents, Game
from pathlib import Path
from discord.flags import Intents
from pymongo import MongoClient
from re import compile

with open('protected_vars.env') as ins:
    result = {}
    for line in ins:
        match = compile(r'''^([^\s=]+)=(?:[\s"']*)(.+?)(?:[\s"']*)$''').match(line)
        if match is not None:
            result[match.group(1)] = match.group(2)
            
TOKEN = result["TOKEN"]

CLUSTER = MongoClient(result["SRV_URL"])
client = commands.Bot(command_prefix = '?', intents = Intents.all(), case_insensitive=True)
client.remove_command('help')

CHANNEL_GENERAL = client.get_channel(result["channel_general"])
CHANNEL_LOGS = client.get_channel(result["channel_logs"])

@client.event
async def on_ready():
    await client.change_presence(activity=Game(name="?help"))

@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, cog):
    client.load_extension(f'cogs.{cog}')
        
@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, cog):
    client.unload_extension(f'cogs.{cog}')
        
@commands.has_permissions(administrator=True)
async def update(ctx, cogss=[x for x in (os.listdir((Path(__file__) / "../cogs/").resolve()))]):
    await ctx.message.delete()
    for cog in enumerate(cogss): 
        if cog.endswith('.py') and not cog.startswith("__"):
            client.unload_extension(f'cogs.{cog[:-3]}')
            client.load_extension(f'cogs.{cog[:-3]}')


@commands.has_permissions(administrator=True)
async def restart(ctx):
    await ctx.message.delete()
    os.execv(sys.executable, ['python'] + sys.argv)

for filename in os.listdir((Path(__file__) / "../cogs/").resolve()):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)
