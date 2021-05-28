#!/usr/bin/env python
import os.path, subprocess
from re import compile
from discord.ext import commands, ipc
from discord import Intents, Game
from colorama import Fore, Style
from discord.flags import Intents
from colorama import Fore, Style
from pymongo import MongoClient

class Bot(commands.Bot):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.ipc = ipc.Server(self,secret_key = result["IPC_SECRET"])

        self.COGS = {
            "root" : [
                "website"
            ],

            "cogs" : [
                "afk","audio","experience_system",
                "fun","image_manipulation","image","misc", 
                "logger", "moderation"
            ],
            
            "utils" : [
                "error_handler", "utility_commands", "help",
                "ipc_routes"
            ],


            "games" : [
                "trivia_quiz._cog", "connect_4", "battle_ships"
            ]
        }

    async def on_ready(self):
        print(f"{Fore.GREEN}[!]{Style.RESET_ALL} Bot is ready!")
        await bot.change_presence(activity=Game(name=f"?help"))
        
    async def on_ipc_ready(self):
        try:
            process = subprocess.Popen(f'python website.py')
        except:
            process = subprocess.Popen(["python3","website.py"])

        print(f"{Fore.GREEN}[!]{Style.RESET_ALL} IPC Server is ready!")

    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)


with open('protected_vars.env') as ins:
    result = {}
    for line in ins:
        match = compile(r'''^([^\s=]+)=(?:[\s"']*)(.+?)(?:[\s"']*)$''').match(line)
        if match is not None:
            result[match.group(1)] = match.group(2)

bot_var_arr = [result["SRV_URL"], result["TOKEN"]]
website_var_arr = [result["SECRET_KEY"], result["IPC_SECRET"], result["DISCORD_CLIENT_ID"], result["DISCORD_CLIENT_SECRET"], result["DISCORD_REDIRECT_URI"]]

ROOT = str(__file__)[:-len("bot.py")]
CLUSTER = MongoClient(result["SRV_URL"])

bot = Bot(command_prefix = '?', intents = Intents.all(), case_insensitive=True)
bot.remove_command('help')

for key, cogs in bot.COGS.items():
    for cog in cogs:

        string = f'Bot.{key}.{cog}'

        if key == "root":
            string = f'{cog}'

        bot.load_extension(string)

if __name__ == "__main__":
    if any("INSERT" in word for word in website_var_arr):
        print(f"{Fore.RED}[x]{Style.RESET_ALL} Website vars have not been set-up. Skipping...")
    else:
        bot.ipc.start()
        
    if any("INSERT" in word for word in bot_var_arr):
        print(f"{Fore.RED}[x]{Style.RESET_ALL} Bot vars have not been set-up. Skipping...")
    else:
        bot.run(result["TOKEN"])