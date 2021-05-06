from os import link
from colorama.ansi import Style
import discord
from random import choice
from datetime import datetime, timedelta
from discord import message
import re
from discord.ext import commands
from pymongo.message import delete
from main import CLUSTER
from colorama import Fore, Style
GIF_DB = CLUSTER["discord"]["gifs"]
BLACKLIST = CLUSTER["discord"]["utils"].find_one({"id": "type_blacklist"})["blacklist"]

deleted_messages = []
class Logger(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.author_temp = ""

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=10):
        '''?purge [amount to delete]'''

        print (f"{Fore.MAGENTA}[{self.client.command_prefix}]{Style.RESET_ALL} {Fore.BLUE}[{datetime.now().strftime('%H:%M:%S')}]{Style.RESET_ALL} {Fore.CYAN}{ctx.author}{Style.RESET_ALL} used command {Fore.YELLOW}[PURGE]{Style.RESET_ALL} on {Fore.RED}{amount}{Style.RESET_ALL} messages")
        await ctx.channel.trigger_typing()
        
        async for message in ctx.channel.history(limit=amount):
            if message.author == ctx.author:
                self.author_temp = message.author
                if not message.content.startswith("?"):
                    for word in BLACKLIST:
                        message.content = message.content.lower().replace(word, "[redacted]")
                    deleted_messages.append(message)
        if deleted_messages:
            deleted_messages.reverse()

        await ctx.channel.purge(limit=amount + 1)
        

        embed=discord.Embed(title="", description=f"Purged {amount} messages from {ctx.channel.mention}", timestamp=datetime.utcnow(), color=0xff0000
            ).set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}"
        )
        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        async for entry in message.guild.audit_logs(action=discord.AuditLogAction.message_delete, limit=1):
            now = datetime.utcnow()
            if now - timedelta(seconds=2) <= entry.created_at <= now+timedelta(seconds=2):
                self.deletee = entry.user
            else:
                self.deletee = message.author
        log_channel = self.client.get_channel(808411931383431198)

        if message.author.bot:
            return
            
        if str(self.author_temp) != str(message.author):
            deleted_messages.clear()
            self.author_temp = message.author

        if not message.content.startswith("?"):
            print(f"{Fore.YELLOW}[EVENT]{Style.RESET_ALL} {Fore.RED}[MESSAGE DELETE]{Style.RESET_ALL} {Fore.BLUE}[{datetime.now().strftime('%H:%M:%S')}] {Fore.CYAN}{message.author}{Style.RESET_ALL}: {Fore.RED}{message.content}{Style.RESET_ALL}")
            for word in BLACKLIST:
                message.content = message.content.lower().replace(word, "[redacted]")
            deleted_messages.append(message)

        try:
            embed=discord.Embed(title="", description=f"Message deleted in: {message.channel.mention} by {self.deletee.mention}" if message.content[0:2] != "?m" else f"**Mirrored** message in: {message.channel.mention}", timestamp=datetime.utcnow(), color=0xff0000
                ).set_author(name=f"{message.author}", icon_url=f"{message.author.avatar_url}"
                ).add_field(name="Content", value=f"{message.content}"
                ).add_field(name="ID", value=f"```ml\nUser = {message.author.id}\nMessage = {message.id}\n```", inline=False
            )
            await log_channel.send(embed=embed)
        except:
            pass
            
    @commands.Cog.listener()
    async def on_message_edit(self, before_edit, after_edit):
        log_channel = self.client.get_channel(808411931383431198)
        if before_edit.content == after_edit.content:
            return

        print(f"{Fore.YELLOW}[EVENT] {Fore.MAGENTA}[MESSAGE EDIT]{Style.RESET_ALL} {Fore.BLUE}[{datetime.now().strftime('%H:%M:%S')}] {Fore.CYAN}{before_edit.author}{Style.RESET_ALL}: {Fore.RED}{before_edit.content}{Style.RESET_ALL} -> {Fore.MAGENTA}{after_edit.content}{Style.RESET_ALL}")
        try:
            if any(word in after_edit.content.lower() for word in BLACKLIST):
                await before_edit.delete()
        except:
            pass
        self.temp_message_edit_before = before_edit
        self.temp_message_edit_after = after_edit

        channel_id = before_edit.channel.id
        message_id = before_edit.id
        message_link = "https://discord.com/channels/787823476966162452" + f"/{channel_id}" + f"/{message_id}"
        

        try:
            embed=discord.Embed(title="", description=f"Message edited in: {before_edit.channel.mention}\n[Go To Message]({message_link})", timestamp=datetime.utcnow(), color=0x800080
                ).set_author(name=f"{before_edit.author}", icon_url=f"{before_edit.author.avatar_url}"
                ).add_field(name="Before", value=f"{before_edit.content}", inline=False
                ).add_field(name="After", value=f"{after_edit.content}"
            )
            
            await log_channel.send(embed=embed)
        except:
            pass
    
    @commands.command()
    async def snipe(self, ctx):
        '''?snipe'''
        if not deleted_messages:
            await ctx.send("Nothing to snipe!")
            return
        
        if ctx.message.channel == deleted_messages[0].channel:
            gif_db = GIF_DB.find_one({"gif": "find_elem"})
            gif_arr = gif_db["gif_arr"]
            
            strs = [x.content for x in deleted_messages]

            embed=discord.Embed(title="", description=f"Message deleted in: {ctx.message.channel.mention} by {self.deletee.mention}", timestamp=datetime.utcnow(), color=0xff0000
            ).set_author(name=f"{self.author_temp} just got sniped", icon_url=f"{self.author_temp.avatar_url}")
            for i, str in enumerate(strs):
                embed.add_field(name=f"Sniped Message {i + 1}", value=f"{str}", inline=False)
            embed.set_footer(text=f"ID - {self.author_temp.id}"
            ).set_image(url=choice(gif_arr))

            try:
                await ctx.send(embed=embed)
            except:
                try:
                    embed=discord.Embed(title="", description=f"Message deleted in: {ctx.message.channel.mention}", timestamp=datetime.utcnow(), color=0xff0000
                    ).set_author(name=f"{self.author_temp} just got sniped", icon_url=f"{self.author_temp.avatar_url}")
                    for i, str in enumerate(strs):
                        embed.add_field(name=f"Sniped Message {i + 1}", value=f"{str}", inline=False)
                    embed.set_footer(text=f"ID - {self.author_temp.id}"
                    ).set_image(url=choice(gif_arr))

                except:
                    await ctx.send("Cannot Snipe message. Perhaps it contains no text?")

    @commands.command()
    async def esnipe(self, ctx):
        '''?snipe'''
        try:
            before_edit = self.temp_message_edit_before
            after_edit = self.temp_message_edit_after
        except:
            await ctx.send("Nothing to snipe!")
            return

        if ctx.message.channel == self.temp_message_edit_before.channel:
            gif_db = GIF_DB.find_one({"gif": "find_elem"})
            gif_arr = gif_db["gif_arr"]

            before_edit_content = self.temp_message_edit_before.content
            after_edit_content = self.temp_message_edit_after.content
            try:
                for word in BLACKLIST:
                    before_edit_content = before_edit_content.lower().replace(word, "[redacted]")
                    after_edit_content = after_edit_content.lower().replace(word, "[redacted]")
            except:
                pass

            message_id = before_edit.id
            message_link = "https://discord.com/channels/787823476966162452/787823476966162455" + f"/{message_id}"

            embed=discord.Embed(title="", description=f"Message edited in: {before_edit.channel.mention}\n[Go To Message]({message_link})", timestamp=datetime.utcnow(), color=0x800080
                ).set_author(name=f"{before_edit.author} was sniped!", icon_url=f"{before_edit.author.avatar_url}"
                ).add_field(name="Before", value=f"{before_edit_content}", inline=False
                ).add_field(name="After", value=f"{after_edit_content}"
                ).set_image(url=choice(gif_arr)
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def add_gif(self, ctx, link = "NoLinkSpecified"):
        try:
            if link.endswith('.gif') == False and link != "NoLinkSpecified":
                await ctx.send("Please ensure that the link IS a gif and not an embed (e.g tenor links)")
                return

            if link == "NoLinkSpecified":
                link = ctx.message.attachments[0].url

            GIF_DB.update_one({"gif": "find_elem"}, {"$push":{"gif_arr":link}})

            embed = discord.Embed(description=f"Gif has been set!"
                ).set_image(url=link
            )

            await ctx.send(embed=embed)
        except:
            await ctx.send("Could not add gif to array")

        
        
def setup(client):
    client.add_cog(Logger(client))