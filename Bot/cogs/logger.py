from Bot.utils.error_handler import ExpectedLiteralInt, MissingArgument
from Bot.utils.constants import command_activity_check, get_channel_id, get_cluster, get_command_description
import discord
from random import choice
from datetime import datetime, timedelta
from discord.ext import commands

deleted_messages = []
class Logger(commands.Cog, name="Log Commands"):
    """
    Commands related to logging.
    """

    def __init__(self, client):
        self.client = client
        self.author_temp = ""

    @commands.command()
    @command_activity_check()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount):
        """
        Purge messages in a channel.
        ?purge [amount]
        """
     
        await ctx.channel.trigger_typing()
        if amount is None:
            raise MissingArgument("Amount of messages", get_command_description(ctx.command.name))

        try:
            amount = int(amount)
        except:
            raise ExpectedLiteralInt

        
        async for message in ctx.channel.history(limit=amount):
            if message.author == ctx.author:
                self.author_temp = message.author

                _db = get_cluster(ctx.message.guild.id, "CLUSTER_BLACKLIST_WORDS").find_one({"id": "type_blacklist"})["array"]
                if not message.content.startswith("?"):
                    for word in _db:
                        message.content = message.content.lower().replace(word, "[redacted]")
                    deleted_messages.append(message)
        if deleted_messages:
            deleted_messages.reverse()

        await ctx.channel.purge(limit=amount + 1)
        

        embed=discord.Embed(
            description=f"Purged {amount} messages from {ctx.channel.mention}", 
            timestamp=datetime.utcnow(), 
            color=0xff0000
            ).set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}"
        )
        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.content == "":
            return

        async for entry in message.guild.audit_logs(action=discord.AuditLogAction.message_delete, limit=1):
            now = datetime.utcnow()

            if now - timedelta(seconds=2) <= entry.created_at <= now+timedelta(seconds=2):
                self.deletee = entry.user
            else:
                self.deletee = message.author

        log_channel = self.client.get_channel(get_channel_id(message.guild.id, "channel_logs"))

        if message.author.bot:
            return
            
        if str(self.author_temp) != str(message.author):
            deleted_messages.clear()
            self.author_temp = message.author

        if not message.content.startswith("?"):
            _db = get_cluster(message.guild.id, "CLUSTER_BLACKLIST_WORDS").find_one({"id": "type_blacklist"})["array"]
            for word in _db:
                message.content = message.content.lower().replace(word, "[redacted]")
            deleted_messages.append(message)

        embed=discord.Embed(
            description=f"Message deleted in: {message.channel.mention} by {self.deletee.mention}" if message.content[0:2] != "?m" else f"**Mirrored** message in: {message.channel.mention}", 
            timestamp=datetime.utcnow(), 
            color=0xff0000
            ).set_author(name=f"{message.author}", icon_url=f"{message.author.avatar_url}"
            ).add_field(name="Content", value=f"{message.content}"
            ).add_field(name="ID", value=f"```ml\nUser = {message.author.id}\nMessage = {message.id}\n```", inline=False
        )
        await log_channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if any(word in message.content.lower() for word in get_cluster(message.guild.id, "CLUSTER_BLACKLIST_WORDS").find_one({"id": "type_blacklist"})["array"]):
            await message.delete()

    @commands.Cog.listener()
    async def on_message_edit(self, before_edit, after_edit):
        log_channel = self.client.get_channel(get_channel_id(before_edit.guild.id, "channel_logs"))
        if before_edit.content == after_edit.content:
            return

        if any(word in after_edit.content.lower() for word in get_cluster(before_edit.guild.id, "CLUSTER_BLACKLIST_WORDS").find_one({"id": "type_blacklist"})["array"]):
            await before_edit.delete()

        self.temp_message_edit_before = before_edit
        self.temp_message_edit_after = after_edit

        channel_id = before_edit.channel.id
        message_id = before_edit.id
        message_link = "https://discord.com/channels/787823476966162452" + f"/{channel_id}" + f"/{message_id}"
        
        embed=discord.Embed(title="", description=f"Message edited in: {before_edit.channel.mention}\n[Go To Message]({message_link})", timestamp=datetime.utcnow(), color=0x800080
            ).set_author(name=f"{before_edit.author}", icon_url=f"{before_edit.author.avatar_url}"
            ).add_field(name="Before", value=f"{before_edit.content}", inline=False
            ).add_field(name="After", value=f"{after_edit.content}"
        )
        
        await log_channel.send(embed=embed)
    
    @commands.command()
    @command_activity_check()
    async def snipe(self, ctx):
        """
        Sends most recent deleted messages by a member.
        ?snipe
        """

        if not deleted_messages:
            await ctx.send("Nothing to snipe!")
            return
        
        if ctx.message.channel == deleted_messages[0].channel:
            gif_arr = get_cluster(ctx.message.guild.id, "CLUSTER_GIFS").find_one({"id": "type_snipe_gifs"})["array"]
            strs = [x.content for x in deleted_messages]

            embed=discord.Embed(
                description=f"Message deleted in: {ctx.message.channel.mention} by {self.deletee.mention}", 
                timestamp=datetime.utcnow(), 
                color=0xff0000
                ).set_author(name=f"{self.author_temp} just got sniped", icon_url=f"{self.author_temp.avatar_url}"
            )

            for i, str in enumerate(strs):
                embed.add_field(name=f"Sniped Message {i + 1}", value=f"{str}", inline=False)
            embed.set_footer(text=f"ID - {self.author_temp.id}"
            ).set_image(url=choice(gif_arr))

            try:
                await ctx.send(embed=embed)
            except:
                try:
                    embed=discord.Embed(
                        description=f"Message deleted in: {ctx.message.channel.mention}", 
                        timestamp=datetime.utcnow(), 
                        color=0xff0000
                        ).set_author(name=f"{self.author_temp} just got sniped", icon_url=f"{self.author_temp.avatar_url}")

                    for i, str in enumerate(strs):
                        embed.add_field(name=f"Sniped Message {i + 1}", value=f"{str}", inline=False)
                    embed.set_footer(text=f"ID - {self.author_temp.id}"
                    ).set_image(url=choice(gif_arr))

                except:
                    await ctx.send("Cannot Snipe message. Perhaps it contains no text?")

    @commands.command()
    @command_activity_check()
    async def esnipe(self, ctx):
        """
        Sends most recent edited messages by a member.
        ?esnipe
        """

        try:
            before_edit = self.temp_message_edit_before
            after_edit = self.temp_message_edit_after
        except:
            await ctx.send("Nothing to snipe!")
            return

        if ctx.message.channel == self.temp_message_edit_before.channel:
            gif_arr = get_cluster(ctx.message.guild.id, "CLUSTER_GIFS").find_one({"id": "type_snipe_gifs"})["array"]

            before_edit_content = self.temp_message_edit_before.content
            after_edit_content = self.temp_message_edit_after.content
            try:
                for word in get_cluster(ctx.message.guild.id, "CLUSTER_BLACKLIST_WORDS").find_one({"id": "type_blacklist"})["array"]:
                    before_edit_content = before_edit_content.lower().replace(word, "[redacted]")
                    after_edit_content = after_edit_content.lower().replace(word, "[redacted]")
            except:
                pass

            message_id = before_edit.id
            channel_id = get_channel_id(ctx.message.guild.id, "channel_general")
            message_link = f"https://discord.com/channels/{ctx.message.guild.id}/{channel_id}" + f"/{message_id}"

            embed=discord.Embed(
                description=f"Message edited in: {before_edit.channel.mention}\n[Go To Message]({message_link})", 
                timestamp=datetime.utcnow(), 
                color=0x800080
                ).set_author(name=f"{before_edit.author} was sniped!", icon_url=f"{before_edit.author.avatar_url}"
                ).add_field(name="Before", value=f"{before_edit_content}", inline=False
                ).add_field(name="After", value=f"{after_edit_content}"
                ).set_image(url=choice(gif_arr)
            )
            await ctx.send(embed=embed)
        
        
def setup(client):
    client.add_cog(Logger(client))