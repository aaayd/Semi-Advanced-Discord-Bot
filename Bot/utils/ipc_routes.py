import discord
from discord.ext import commands, ipc

class IpcRoutes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @ipc.server.route()
    async def get_all_guilds(self, data):
        return self.bot.guilds

    @ipc.server.route()
    async def get_all_commands(self, data):

        cmds = {}
        for command in self.bot.commands:
            try:
                description = str(command.help).split(".")[0]
                
                if description is not None or description != "None":
                    help = str(command.help).split(".")[1]
                    cmds[command.name] = [description, help]
            except:
                pass

            
            
        return cmds

    @ipc.server.route()
    async def get_all_cogs(self, data):

        cogs = {"Games" : []}
        for cog in self.bot.cogs:
            cog_name = str(cog)

            if "game" in str(cog).lower():
                cog_name = "Games"
            else:
                cogs[cog_name] = []
                
            for command in self.bot.get_cog(cog).get_commands():
                cogs[cog_name].append([command.name, command.description])

        return dict(sorted(cogs.items(), key=lambda x: x[0].lower()))

    @ipc.server.route()
    async def get_guild(self, data):
        guild = self.bot.get_guild(data.guild_id)
        
        if guild is None: 
            
            return None
        
        guild_data = {
            "name": guild.name,
            "id": guild.id,
            "icon_url": str(guild.icon_url),
            "member_count": int(guild.member_count),
            "role_count": int(len(guild.roles)), 
            "region": str(guild.region), 
            "owner": str(guild.owner),
            "channel_count": int(len(guild.channels)),
            "category_count": int(len(guild.categories))
        }

        try:
            return guild_data
        
        except:
            return None

def setup(bot):
    bot.add_cog(IpcRoutes(bot))
