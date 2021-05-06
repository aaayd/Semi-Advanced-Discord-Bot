from io import BytesIO
import discord, os, praw
from discord.ext import commands, tasks
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw, ImageChops, ImageFilter
from colorama import Fore, Style
import praw, random, requests
from main import CLUSTER

rate_limit = CLUSTER["discord"]["xp_rate_limit"]
CONFESSION_BOOL = CLUSTER["discord"]["utils"].find_one({"id": "type_confession"})["confession"]

r = praw.Reddit(client_id="7oE7yB5GJJua2Q", client_secret="ooidPB-ETJxbRflpja6a65KX03g", user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36', username="PhantomVipermon", check_for_async=False)
last_check = datetime.utcnow
path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'image_processing')

def round_image(image):
    bigsize = (image.size[0] * 3, image.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(image.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, image.split()[-1])
    image.putalpha(mask)
    return image


class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_role("Developer")
    @commands.command()
    async def _roleCheck(self, ctx):
        print (f"{Fore.MAGENTA}[{self.client.command_prefix}]{Style.RESET_ALL} {Fore.BLUE}[{datetime.now().strftime('%H:%M:%S')}]{Style.RESET_ALL} {Fore.CYAN}{ctx.author}{Style.RESET_ALL} used command {Fore.YELLOW}[_roleCheck]{Style.RESET_ALL}")
        await ctx.message.delete()
        
        nibble_role = discord.utils.get(ctx.guild.roles, id = 809888833713471488)
        colour_role = discord.utils.get(ctx.guild.roles, id = 813191738898251796)
        chat_lvl_rank_role = discord.utils.get(ctx.guild.roles, id = 813187617981333536)

        roleless = []
        for member in ctx.guild.members:
            if colour_role not in member.roles and chat_lvl_rank_role not in member.roles:
                roleless.append(member)
        
        count = 0
        for unroled_member in roleless:
            try:
                await unroled_member.add_roles(colour_role, chat_lvl_rank_role, nibble_role)
                count += 1
                print (f"{Fore.BLUE}[{count}/{len(roleless)}]{Style.RESET_ALL} Added {Fore.MAGENTA}2{Style.RESET_ALL} roles to {Fore.CYAN}{unroled_member}{Style.RESET_ALL}")
            except Exception as e:
                pass
        
        print (f"{Fore.GREEN}[!]{Style.RESET_ALL} Finished adding roles to {Fore.MAGENTA}{count}{Style.RESET_ALL} members")
    
    @commands.command(aliases=["st", "shower", "showerthought"])
    async def _get_shower_thought(self, ctx):
        sub = r.subreddit('showerthoughts')
        sub = sub.random()
        text = sub.selftext

        if text  == "":
            text = sub.title
            if text == "":
                await ctx.send("Could not find text")
                return
        

        embed=discord.Embed(title="", description=f"{text}\n\n{sub.url}", inline=False
        ).set_author(name=f"Showerthought by {sub.author}")

        await ctx.send(embed=embed)

    @commands.command()
    async def invites(self, ctx, member : discord.Member = None):
        if member is None:
            member = ctx.author

        totalInvites = 0
        for i in await ctx.guild.invites():
            if i.inviter == ctx.author:
                totalInvites += i.uses
        await ctx.send(f"{member} has invited {totalInvites} member{'' if totalInvites == 1 else 's'} to the server!")


    @commands.command(aliases=['m'])
    async def mirror(self, ctx):
        if ctx.author.id == 506240196036263937:
            return
            
        message = ctx.message.content
        print (f"{Fore.MAGENTA}[{self.client.command_prefix}]{Style.RESET_ALL} {Fore.BLUE}[{datetime.now().strftime('%H:%M:%S')}]{Style.RESET_ALL} {Fore.CYAN}{ctx.author}{Style.RESET_ALL} used command {Fore.YELLOW}[MIRROR]{Style.RESET_ALL} {Fore.BLUE}[{message[3:]}]{Style.RESET_ALL}")
        try:
            if isinstance(ctx.channel, discord.channel.DMChannel):
                log_channel = self.client.get_channel(808411931383431198)
                channel = self.client.get_channel(787823476966162455)
                embed=discord.Embed(title="", description=f"**Mirrored** message in DM's with {message.author.mention}", timestamp=datetime.utcnow(), color=0xff0000
                    ).set_author(name=f"{message.author}", icon_url=f"{message.author.avatar_url}"
                    ).add_field(name="Content", value=f"{message.content[3:]}"
                    ).add_field(name="ID", value=f"```ml\nUser = {message.author.id}\nMessage = {message.id}\n```", inline=False
                )
                await log_channel.send(embed=embed)
                await channel.send(message.content[3:])
                return
                
            message = message[3:]
            
            if message[0] == str(self.client.command_prefix):
                await ctx.reply("Yoo wtf man why try send a command like that? Not cool.")
                return

            await ctx.message.delete()
            await ctx.send(message)



        except:
            pass


    @commands.command()
    async def serverinfo(self, ctx):
        '''?serverinfo'''
        embed = discord.Embed(
            title=str(ctx.guild.name) + " Server Information",
            description=str(ctx.guild.description),
            color=discord.Color.blue()
            
            ).set_thumbnail(url=str(ctx.guild.icon_url)
            ).add_field(name="Owner", value=str(ctx.guild.owner), inline=True
            ).add_field(name="Server ID", value=str(ctx.guild.id), inline=True
            ).add_field(name="Region", value=str(ctx.guild.region), inline=True
            ).add_field(name="Member Count", value=str(ctx.guild.member_count), inline=True
        )

        await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(787823476966162455)
        card = Image.open(os.path.join(f"{path}//welcome//backgrounds//", f"background_{random.randint(1,14)}.png"))
        av_outline_circle = Image.open(os.path.join(f"{path}//welcome//utils//", f"black_circle.png"))
        alpha_plate = Image.open(os.path.join(f"{path}//welcome//utils//", f"alpha_plate.png"))
        welcome_text_plate = Image.open(os.path.join(f"{path}//welcome//utils//", f"welcome_plate.png"))
        avatar_img = Image.open(requests.get(member.avatar_url_as(size=1024), stream=True).raw).convert("RGBA")
        avatar_img = round_image(avatar_img.resize((363,363)))
        draw = ImageDraw.Draw(card)
    
        card.paste(alpha_plate, (100,100), alpha_plate)
        card.paste(welcome_text_plate, (524,20), welcome_text_plate)
        card.paste(av_outline_circle, (566,114), av_outline_circle)
        card.paste(avatar_img, ((569,117)), avatar_img)

        _text_width, _h = draw.textsize(f"{member.name}#{member.discriminator}", ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 70))
        draw.text(((1500-_text_width)/2 ,501), f"{member.name}", font=ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 70), fill=(255,255,255))
        _w, _h = draw.textsize(f"{member.name}", ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 70))
        draw.text(((1500-_text_width)/2 + _w + 3,501), f"#{member.discriminator}", font=ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 70), fill=(81,81,81))

        _text_width, _h = draw.textsize(f"Member #{self.client.get_guild(787823476966162452).member_count}", ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 55))
        draw.text(((1500-_text_width)/2 ,574), f"Member #{self.client.get_guild(787823476966162452).member_count}", font=ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 55), fill=(255,255,255))

        card.save(os.path.join(f"{path}//temp//","temp_welcome.png"))
        await channel.send(file=discord.File(os.path.join(f"{path}//temp//","temp_welcome.png")))

    '''Confess command'''
    @commands.command()
    async def confess(self, ctx, *str):
        '''[dm only] ?confess [message]'''
        if isinstance(ctx.channel, discord.channel.DMChannel) and CONFESSION_BOOL:
            try:
                print (f"{Fore.MAGENTA}[{self.client.command_prefix}]{Style.RESET_ALL} {Fore.BLUE}[{datetime.now().strftime('%H:%M:%S')}]{Style.RESET_ALL} {Fore.CYAN}{ctx.author}{Style.RESET_ALL} used command {Fore.YELLOW}[CONFESSION]{Style.RESET_ALL} {Fore.BLUE}[{( ' '.join(str))}]{Style.RESET_ALL}")
                channel = self.client.get_channel(810134738110513152)
                embed=discord.Embed(title=f"New Anonymous Confession!", description=( ' '.join(str)))
                await channel.send(embed=embed)
            except:
                pass
        elif CONFESSION_BOOL == False:
            channel = self.client.get_channel(810134738110513152)
            await ctx.send("Confess is disabled due to misuse of the command.")
            
    @commands.command()
    async def ping(self, ctx):
        print (f"{Fore.MAGENTA}[{self.client.command_prefix}]{Style.RESET_ALL} {Fore.BLUE}[{datetime.now().strftime('%H:%M:%S')}]{Style.RESET_ALL} {Fore.CYAN}{ctx.author}{Style.RESET_ALL} used command {Fore.YELLOW}[PING]{Style.RESET_ALL}")
        '''Returns bot ping'''
        embed=discord.Embed(title=f"", description=f'Pong :ping_pong:    {round(self.client.latency * 1000)}ms!')
        await ctx.reply(embed=embed)
        
    @commands.command(aliases=["av"])
    async def avatar(self, ctx, member : discord.Member=None):
        print (f"{Fore.MAGENTA}[{self.client.command_prefix}]{Style.RESET_ALL} {Fore.BLUE}[{datetime.now().strftime('%H:%M:%S')}]{Style.RESET_ALL} {Fore.CYAN}{ctx.author}{Style.RESET_ALL} used command {Fore.YELLOW}[AV]{Style.RESET_ALL}")
        if member == None:
            member = ctx.message.author    
    
        url_png = str(member.avatar_url)[:-14] + "png?size=2048"
        url_jpg = str(member.avatar_url)[:-14] + "jpg?size=2048"
        url_webp = str(member.avatar_url)[:-14] + "webp?size=2048"

        embed=discord.Embed(title="", description=f"[PNG]({url_png}) | [JPEG]({url_jpg}) | [WEBP]({url_webp})", inline=False, color=0x912aad
            ).set_author(name=f"Avatar for: {member}", icon_url=f"{member.avatar_url}"
        )

        if ".gif?" in str(member.avatar_url):
            embed.set_image(url=f"{member.avatar_url}")
            
        else:
            embed.set_image(url=f"{url_png}")
        
        await ctx.send(embed=embed)

    @commands.command(aliases=['color', 'colour'])
    async def _colour(self, ctx):
        channel = self.client.get_channel(809117825620639764)
        await ctx.message.delete() 
        if channel == ctx.channel:
                
            colour_arr = ["BLACK",
                "WHITE",
                "RED",
                "ORANGE",
                "YELLOW",
                "CHARTRUESE",
                "GREEN",
                "CYAN",
                "BLUE",
                "PURPLE",
                "MAGENTA"
            ]

            message = ctx.message.content
            try:
                if message.split(" ")[1].upper() == "BLACK" or message.split(" ")[1].upper() == "WHITE":
                    return

                if message.split(" ")[1].upper() in colour_arr:
                    role = discord.utils.get(ctx.guild.roles, name=message.split(" ")[1].upper())

                    for colour in colour_arr:
                        if discord.utils.get(ctx.guild.roles, name=colour) in ctx.author.roles:
                            await ctx.author.remove_roles(discord.utils.get(ctx.guild.roles, name=colour))

                    await ctx.author.add_roles(role)

                else:
                    return
            except:
                pass
    
    @commands.has_role("Developer")
    @commands.command()
    async def _set_colour_text(self, ctx):
        embed=discord.Embed(title="", description=f"There are new colors in the server! Here you can select your new colours!\nUsage: **?color [color_name]**", timestamp=datetime.utcnow(), color=0x800080
            ).add_field(name="Color Names", value=f"Red, Orange, Yellow, Chartruese\nGreen, Cyan, Blue, Purple, Magenta", inline=True
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["whois"])
    async def userinfo(self,ctx, member: discord.Member = None):
        if not member:  # if member is no mentioned
            member = ctx.message.author  # set member as the author
        roles = [role for role in member.roles[:1]]
        embed = discord.Embed(colour=discord.Colour.purple(), title=f"User Info - {member}"
            ).set_thumbnail(url=member.avatar_url
            ).set_footer(text=f"Requested by {ctx.author}"

            ).add_field(name="ID:", value=member.id
            ).add_field(name="Display Name:", value=member.display_name

            ).add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")
            ).add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC")

            ).add_field(name="Highest Role:", value=member.top_role.mention
        )
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(add_reactions=True,embed_links=True)
    async def help(self,ctx, word = "None"):
        word = word.lower()

        if word == "moderation":
            embed=discord.Embed(title="", description=f"Here is list of [MODERATION] commands", timestamp=datetime.utcnow(), color=0xff0000
                ).add_field(name="Mute", value=f"?mute [@member] [time] [reason]"
                ).add_field(name="Unmute", value=f"?unmute [@member]"
                ).add_field(name="Purge", value=f"?purge [amount to delete]"
                ).add_field(name="Clear user messages", value=f"?clear [@member] [amount to delete]"
                ).add_field(name="Warn", value=f"?warn [@member] [reason]"
                ).add_field(name="View warns", value=f"?modlogs [@member]"
                ).add_field(name="Clear warns", value=f"?clearwarns [@member]"
                ).add_field(name="Kick", value=f"?kick [@member] [reason]"
                ).add_field(name="Ban", value=f"?ban [@member] [reason]"
            ).add_field(name="Server Information", value=f"?serverinfo"
            )
        
        elif word == "fun":
            embed=discord.Embed(title="", description=f"Here is list of [FUN] commands", timestamp=datetime.utcnow(), color=0xff0000
                ).add_field(name="Roll a Dice", value=f"?rolldice"
                ).add_field(name="Flip a Coin", value=f"?coinflip"
                ).add_field(name="Snipe last message", value=f"?snipe"
                ).add_field(name="Gay-o-meter", value=f"?gay [@member]"
                ).add_field(name="Dick-Detector", value=f"?dick [@member]"
                ).add_field(name="Pussy-Puffer", value=f"?pussy [@member]"
                ).add_field(name="Simp", value=f"?simp [@user1] [@user2]"
                ).add_field(name="Confess secret [dm only]", value=f"?confess [message]"
                ).add_field(name="Show avatar", value=f"?av [@member]"
                ).add_field(name="Show ping", value=f"?ping"
                ).add_field(name="Kiss Somebody", value=f"?kiss [@member]"
                ).add_field(name="Mirror message", value=f"?m [message]"
            )

        elif word == "level" or word == "levels":
            embed=discord.Embed(title="", description=f"Here is list of [LEVEL] commands", timestamp=datetime.utcnow(), color=0xff0000
                ).add_field(name="View rank", value=f"?rank [@member]"
                ).add_field(name="View leaderboard", value=f"?leaderboard"
                ).add_field(name="Set AFK status", value=f"?afk [afk status message]"
            )

        elif word == "afk":
            embed=discord.Embed(title="", description=f"Here is list of [AFK] commands", timestamp=datetime.utcnow(), color=0xff0000 
                ).add_field(name="Set AFK status", value=f"?afk [afk status message]"
            )

        elif word == "music":
            embed=discord.Embed(title="", description=f"Here is list of [AUDIO] commands", timestamp=datetime.utcnow(), color=0xff0000 
                ).add_field(name="Connect to channel", value=f"?connect"
                ).add_field(name="Play a video", value=f"?play [link]"
                ).add_field(name="Pause a video", value=f"?pause"
                ).add_field(name="Resume video", value=f"?resume"
                ).add_field(name="Skip video", value=f"?resume"
                ).add_field(name="View Queue", value=f"?queue"
                ).add_field(name="Set Volume", value=f"?volume [0.2 - 1.0]"
                ).add_field(name="Stop", value=f"?stop"
            )

        elif word == "custom" or word == "rank":
            embed=discord.Embed(title="", description=f"Here is list of [CUSTOM] commands", timestamp=datetime.utcnow(), color=0xff0000
                ).add_field(name="Change Rank Background", value=f"?bg [image_link]", inline=False
                ).add_field(name="Change Rank Colour", value=f"?cr [hex]", inline=False
                ).set_footer(text="You can also send a file instead of a link with ?bg ! "
            )
            
        elif word == "animal" or word == "animals":
            embed=discord.Embed(title="", description=f"Here is list of [ANIMAL] commands", timestamp=datetime.utcnow(), color=0xff0000
                ).add_field(name="Send Dog Image", value=f"?animal dog", inline=False
                ).add_field(name="Send Cat Image", value=f"?animal cat", inline=False
                ).add_field(name="Send Fox Image", value=f"?animal fox", inline=False
                ).add_field(name="Send Koala Image", value=f"?animal koala", inline=False
                ).add_field(name="Send Panda Image", value=f"?animal panda", inline=False
                ).add_field(name="Send Racoon Image", value=f"?animal racoon", inline=False
                ).add_field(name="Send Kangaroo Image", value=f"?animal kangaroo", inline=False
            )
                

        elif word == "nsfw" or word == "animals":
            embed=discord.Embed(title="", description=f"Here is list of [ANIMAL] commands", timestamp=datetime.utcnow(), color=0xff0000
                ).add_field(name="Send Tits", value=f"?tits", inline=False
                ).add_field(name="Send Ass", value=f"?ass", inline=False
                ).add_field(name="Send Feet", value=f"?feet", inline=False
                ).add_field(name="Send Porn Gif", value=f"?porngif", inline=False
                ).add_field(name="Send Rule 34", value=f"?r34 [* rule 34 query]", inline=False
                ).add_field(name="Send Random Reddit Post", value=f"?reddit [subreddit]", inline=False
            )

        else:
            embed=discord.Embed(title="", description=f"Please select a category [?help category]", timestamp=datetime.utcnow(), color=0xff0000
                ).set_author(name=f"{ctx.message.author} requested  bot help", icon_url=f"{ctx.author.avatar_url}"
                ).add_field(name="Custom Rank BG / Colour", value=f"?help custom", inline=False
                ).add_field(name="Music", value=f"?help music", inline=False
                ).add_field(name="Moderation", value=f"?help moderation", inline=False
                ).add_field(name="Level", value=f"?help level", inline=False
                ).add_field(name="AFK", value=f"?help afk", inline=False
                ).add_field(name="Fun", value=f"?help fun", inline=False
                ).add_field(name="Animals", value=f"?help animal", inline=False
            )
        await ctx.send(embed=embed)






def setup(client):
    client.add_cog(Misc(client))

#    @commands.Cog.listener()
#    async def on_member_ban(self, guild, user):    
