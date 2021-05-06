import discord, requests, os
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageChops, UnidentifiedImageError
from colorama import Fore, Style
import numpy as np
from datetime import datetime

from main import CLUSTER

text_channels = [808411931383431198]
levels = {
    '5': "Level 5",
    '10': "Level 10",
    '15': "Level 15",
    '20': "Level 20"
}
path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'image_processing')

leveling = CLUSTER["discord"]["fsfsefsefesf"]
def get_level(xp):
    lvl = 0
    while True:
        if xp < ((50*(lvl**2))+(50*(lvl))):
            break
        lvl += 1
    return lvl

def get_rank(member):
    rankings = leveling.find().sort("xp", -1)
    for iter,rank in enumerate(list(rankings)):
        if rank["id"] == member.id:
            rank_in_server = iter + 1
            return rank_in_server

def round_image(image):
    bigsize = (image.size[0] * 3, image.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(image.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, image.split()[-1])
    image.putalpha(mask)
    return image

def change_white(image, colour):
    data = np.array(image)
    red, green, blue, alpha= data.T 
    white_areas = (red == 255) & (blue == 255) & (green == 255)
    data[..., :-1][white_areas.T] = colour 

    
    return Image.fromarray(data)

class RankV2(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["bg"])
    async def set_background(self, ctx, link="NoLinkSpecified"):
        try:
            if link == "NoLinkSpecified":
                link = ctx.message.attachments[0].url
            else:
                response = requests.get(link)

            leveling.update_one({"id": ctx.author.id}, {"$set":{"background":link}})

            embed = discord.Embed(description=f"Your personal background has been changed! \n- DO NOT delete the picture or the background will reset"
                ).set_image(url=link
            )

            await ctx.send(embed=embed)
        except:
            await ctx.send("Could not set image")


    @commands.command(aliases=["cr"])
    async def set_colour(self, ctx, r):
        await ctx.message.delete()
        try:
            r = r.lstrip('#')
            colour = ImageColor.getcolor(f"#{str(r).lower()}", "RGB")
            leveling.update_one({"id": ctx.author.id}, {"$set":{"colour":colour}})

            embed = discord.Embed(description=f"Your personal colour has been changed!", color=int(hex(int(r.replace("#", ""), 16)), 0))
            await ctx.send(embed=embed)
        except:
            await ctx.send("Probably invalid HEX value")


    @commands.command(aliases=["r2"])
    async def rank(self, ctx, member: discord.Member = None):
        '''?rank [user]'''
        print (f"{Fore.MAGENTA}[{self.client.command_prefix}]{Style.RESET_ALL} {Fore.BLUE}[{datetime.now().strftime('%H:%M:%S')}]{Style.RESET_ALL} {Fore.CYAN}{ctx.author}{Style.RESET_ALL} used command {Fore.YELLOW}[RANK]{Style.RESET_ALL}")
        await ctx.message.delete()
        
        if member is None:
            member = ctx.author

        await ctx.channel.trigger_typing()
        
        stats = leveling.find_one({"id" : member.id})

        if stats is None:
            await ctx.send("This user has no XP")
            return

        xp = stats["xp"]
        lvl = get_level(xp)
        xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
        rank = get_rank(member)
        try:
            colour = (stats["colour"][0],stats["colour"][1],stats["colour"][2])
        
        except:
            colour = (65, 178, 138)

        try:
            background = (stats["background"])
        except:
            background = "https://media.discordapp.net/attachments/665771066085474346/821993295310749716/statementofsolidarity.jpg?width=1617&height=910"


        try:
            card = Image.open(requests.get(background, stream=True).raw).convert("RGBA")
        
        except UnidentifiedImageError:
            await ctx.send("Your image cannot be found. Ensure it has not been deleted\nYour background has been reset")
            background = "https://media.discordapp.net/attachments/665771066085474346/821993295310749716/statementofsolidarity.jpg?width=1617&height=910"
            leveling.update_one({"id": ctx.author.id}, {"$set":{"colour":colour}})
        avatar_img = Image.open(requests.get(member.avatar_url_as(size=1024), stream=True).raw).convert("RGBA")
        empty = Image.open(os.path.join(f"{path}//rank//","empty_png.png")).convert("RGBA")

        '''RESIZE IMAGE'''
        card = card.resize((1260,420))

        '''PASTE TRANSPARENCY'''
        empty = empty.resize((1260, 420))
        card.paste(empty, ((0,0)), empty)

        # Paste alpha rectangle
        

        draw = ImageDraw.Draw(card)

        '''PASTE AVATAR'''
        avatar_img = avatar_img.resize((222,222))
        avatar_img = round_image(avatar_img)
        card.paste(avatar_img, ((84,91)), avatar_img)
        # Paste avatar image

        '''DRAW USER STATUS'''
        start = Image.open(os.path.join(f"{path}//rank//","activity_circle.png")).convert("RGBA")
        start = change_white(start, (0,0,0))
        card.paste(start, (244, 248), start)

        if str(member.status) == "online":
            fill_colour = (27, 174, 27)
        elif str(member.status) == "idle":
            fill_colour = (237, 126, 27)
            special = Image.open(os.path.join(f"{path}//rank//","activity_circle_eclipse.png")).convert("RGBA")
        elif str(member.status) == "dnd":
            fill_colour = (174, 27, 27)
            special = Image.open(os.path.join(f"{path}//rank//","activity_circle_dnd.png")).convert("RGBA")
        else:
            fill_colour = (81,81,81)

        start = Image.open(os.path.join(f"{path}//rank//","activity_circle_inner.png")).convert("RGBA")
        start = change_white(start, fill_colour)
        card.paste(start, (247, 251), start)

        if str(member.status) == "dnd":
            card.paste(special, (255, 277), special)

        elif str(member.status) == "idle":
            card.paste(special, (247, 252), special)

        '''DRAW TEXT'''
        draw.text((340,128), f"{member.name}", font=ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 40), fill=colour)
        _w, h = draw.textsize(f"{member.name}", ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 40))
        # Get width of text 
        draw.text((340 + _w + 3,128), f"#{member.discriminator}", font=ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 40), fill=(81,81,81))
        # Put #2431 using width of text
        
        draw.text((340,219), f"{xp}", font=ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 40), fill=colour)
        w, h = draw.textsize(f"{xp}", ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 40))
        draw.text((340+w+3, 219), f"/ {int(200*((1/2)*lvl))} XP", font=ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 40), fill=(81,81,81))
        # Place XP text

        
        
        #draw.text((1016,58), f"{rank}", font=ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 40), fill=colour)
        while True:
            w, h = draw.textsize(f"#{rank} / {ctx.guild.member_count}", ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 40))
            border = 1181

            if (w + 1016) > border:
                difference = (w + 1016) - border
                break

            difference = 0
            break
        
        draw.text((1016 - difference,58), f"#{rank}", font=ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 40), fill=colour)
        w, h = draw.textsize(f"#{rank}", ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 40))
        draw.text(((1016+w+3) - difference, 58), f" / {ctx.guild.member_count}", font=ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 40), fill=(81,81,81))
        # Place RANK text

        draw.text((694,219), f"Level: {lvl}", font=ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 40), fill=colour)
        # Place LVL text

        '''DRAW XP BAR'''
        start = Image.open(os.path.join(f"{path}//rank//","half_circle.png")).convert("RGBA")
        start = change_white(start, colour)

        card.paste(start, (334, 263), start)

        percentage = round(((xp / int(200*((1/2)*lvl))* 100) * 714) / 100)

        draw.rectangle(((350, 263), (percentage + 333, 309)), fill=colour)

        start = start.rotate(180)
        card.paste(start, (percentage + 334, 263), start)

        card.save(os.path.join(f"{path}//rank//","card_temp.png"))
        await ctx.send(file=discord.File(os.path.join(f"{path}//rank//","card_temp.png")))

                
    
def setup(client):
    client.add_cog(RankV2(client))
