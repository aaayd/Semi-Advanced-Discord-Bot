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

        self.env_vars = {}
        with open('protected_vars.env') as ins:
            for line in ins:
                match = compile(r'''^([^\s=]+)=(?:[\s"']*)(.+?)(?:[\s"']*)$''').match(line)
                if match is not None:
                    self.env_vars[match.group(1)] = match.group(2)
        
        self.root_path = str(__file__)[:-len("bot.py")]
        self.mongo_client = MongoClient(self.env_vars["SRV_URL"])
        self.ipc = ipc.Server(self,secret_key = self.env_vars["IPC_SECRET"])
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
        
    async def on_ipc_ready(self):
        try:
            process = subprocess.Popen(f'python website.py')
        except:
            process = subprocess.Popen(["python3","website.py"])

        print(f"{Fore.GREEN}[!]{Style.RESET_ALL} IPC Server is ready!")

    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)

bot = Bot(command_prefix = '?', intents = Intents.all(), case_insensitive=True, help_command=None, activity=Game(name=f"?help"))

for key, cogs in bot.COGS.items():
    for cog in cogs:

        string = f'Bot.{key}.{cog}'

        if key == "root":
            string = f'{cog}'

        bot.load_extension(string)

if __name__ == "__main__":
    if any("INSERT" in word for word in [bot.env_vars["SRV_URL"], bot.env_vars["TOKEN"]]):
        print(f"{Fore.RED}[x]{Style.RESET_ALL} Website vars have not been set-up. Skipping...")
    else:
        bot.ipc.start()
        
    if any("INSERT" in word for word in [bot.env_vars["SECRET_KEY"], bot.env_vars["IPC_SECRET"], bot.env_vars["DISCORD_CLIENT_ID"], bot.env_vars["DISCORD_CLIENT_SECRET"], bot.env_vars["DISCORD_REDIRECT_URI"]]):
        print(f"{Fore.RED}[x]{Style.RESET_ALL} Bot vars have not been set-up. Skipping...")
    else:
        bot.run(bot.env_vars["TOKEN"])