import discord, requests, os, random
import numpy as np
from PIL import ImageColor
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw, ImageChops
from requests.models import InvalidURL
from utils.constants import CLUSTER_EXPERIENCE, CHANNEL_GENERAL_ID, IMAGE_PATH, get_command_description, query_valid_url
from utils.error_handler import embed_error, MissingArgument


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

def create_rank_card(member : discord.Member, xp, lvl, rank, background, colour, member_count):
    card = Image.open(requests.get(background, stream=True).raw).convert("RGBA")
    avatar_img = Image.open(requests.get(member.avatar_url_as(size=1024), stream=True).raw).convert("RGBA")
    empty = Image.open(os.path.join(f"{IMAGE_PATH}//rank//","empty_png.png")).convert("RGBA")

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
    start = Image.open(os.path.join(f"{IMAGE_PATH}//rank//","activity_circle.png")).convert("RGBA")
    start = change_white(start, (0,0,0))
    card.paste(start, (244, 248), start)

    if str(member.status) == "online":
        fill_colour = (27, 174, 27)

    elif str(member.status) == "idle":
        fill_colour = (237, 126, 27)
        unique_coord = (247, 252)
        special = Image.open(os.path.join(f"{IMAGE_PATH}//rank//","activity_circle_eclipse.png")).convert("RGBA")

    elif str(member.status) == "dnd":
        fill_colour = (174, 27, 27)
        unique_coord = (255, 277)
        special = Image.open(os.path.join(f"{IMAGE_PATH}//rank//","activity_circle_dnd.png")).convert("RGBA")

    else:
        fill_colour = (81,81,81)

    start = Image.open(os.path.join(f"{IMAGE_PATH}//rank//","activity_circle_inner.png")).convert("RGBA")
    start = change_white(start, fill_colour)
    card.paste(start, (247, 251), start)

    if str(member.status) == "dnd" or str(member.status) == "idle":
        card.paste(special, unique_coord, special)

    '''DRAW TEXT'''
    draw.text((340,128), f"{member.name}", font=ImageFont.truetype(os.path.join(f"{IMAGE_PATH}//font//","uni-sans-light.ttf"), 40), fill=colour)
    _w, h = draw.textsize(f"{member.name}", ImageFont.truetype(os.path.join(f"{IMAGE_PATH}//font//","uni-sans-light.ttf"), 40))
    # Get width of text 
    draw.text((340 + _w + 3,128), f"#{member.discriminator}", font=ImageFont.truetype(os.path.join(f"{IMAGE_PATH}//font//","uni-sans-light.ttf"), 40), fill=(81,81,81))
    # Put #2431 using width of text
    
    draw.text((340,219), f"{xp}", font=ImageFont.truetype(os.path.join(f"{IMAGE_PATH}//font//","uni-sans-light.ttf"), 40), fill=colour)
    w, h = draw.textsize(f"{xp}", ImageFont.truetype(os.path.join(f"{IMAGE_PATH}//font//","uni-sans-light.ttf"), 40))
    draw.text((340+w+3, 219), f"/ {int(200*((1/2)*lvl))} XP", font=ImageFont.truetype(os.path.join(f"{IMAGE_PATH}//font//","uni-sans-light.ttf"), 40), fill=(81,81,81))
    # Place XP text

            
    #draw.text((1016,58), f"{rank}", font=ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 40), fill=colour)
    while True:
        w, h = draw.textsize(f"#{rank} / {member_count}", ImageFont.truetype(os.path.join(f"{IMAGE_PATH}//font//","uni-sans-light.ttf"), 40))
        border = 1181

        if (w + 1016) > border:
            difference = (w + 1016) - border
            break

        difference = 0
        break
    
    draw.text((1016 - difference,58), f"#{rank}", font=ImageFont.truetype(os.path.join(f"{IMAGE_PATH}//font//","uni-sans-light.ttf"), 40), fill=colour)
    w, h = draw.textsize(f"#{rank}", ImageFont.truetype(os.path.join(f"{IMAGE_PATH}//font//","uni-sans-light.ttf"), 40))
    draw.text(((1016+w+3) - difference, 58), f" / {member_count}", font=ImageFont.truetype(os.path.join(f"{IMAGE_PATH}//font//","uni-sans-light.ttf"), 40), fill=(81,81,81))
    # Place RANK text

    draw.text((694,219), f"Level: {lvl}", font=ImageFont.truetype(os.path.join(f"{IMAGE_PATH}//font//","uni-sans-light.ttf"), 40), fill=colour)
    # Place LVL text

    '''DRAW XP BAR'''
    start = Image.open(os.path.join(f"{IMAGE_PATH}//rank//","half_circle.png")).convert("RGBA")
    start = change_white(start, colour)

    card.paste(start, (334, 263), start)

    percentage = round(((xp / int(200*((1/2)*lvl))* 100) * 714) / 100)

    draw.rectangle(((350, 263), (percentage + 333, 309)), fill=colour)

    start = start.rotate(180)
    card.paste(start, (percentage + 334, 263), start)

    card.save(os.path.join(f"{IMAGE_PATH}//temp//","card_temp.png"))

class ImageManipulation(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(aliases=["bg"])
    async def set_background(self, ctx, link="NoLinkSpecified"):
        '''?set_background [image_link]'''

        if link == "NoLinkSpecified":
            if (len(ctx.message.attachments)) == 0:
                raise MissingArgument("Background Image Link", get_command_description("set_background"))

            link = ctx.message.attachments[0].url

        else:
            if not query_valid_url(link):
                raise InvalidURL


        CLUSTER_EXPERIENCE.update_one({
            "id": ctx.author.id}, 
            {"$set":{
                "background":link
                }
            })

        embed = discord.Embed(
            description=f"Your personal background has been changed! \n- DO NOT delete the picture or the background will reset"
            ).set_image(url=link
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=["cr"])
    async def set_colour(self, ctx, r = None):
        '''?set_colour [hex]''' 

        await ctx.message.delete()

        if r is None:
            raise MissingArgument("HEX", get_command_description("set_colour"))

        r = r.lstrip('#')
        colour = ImageColor.getcolor(f"#{str(r).lower()}", "RGB")
        CLUSTER_EXPERIENCE.update_one({"id": ctx.author.id}, {"$set":{"colour":colour}})

        embed = discord.Embed(
            description=f"Your personal colour has been changed!", 
            color=int(hex(int(r.replace("#", ""), 16)), 0)
        )

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(int(CHANNEL_GENERAL_ID[0]))
        card = Image.open(os.path.join(f"{IMAGE_PATH}//welcome//backgrounds//", f"background_{random.randint(1,14)}.png"))
        av_outline_circle = Image.open(os.path.join(f"{IMAGE_PATH}//welcome//utils//", f"black_circle.png"))
        alpha_plate = Image.open(os.path.join(f"{IMAGE_PATH}//welcome//utils//", f"alpha_plate.png"))
        welcome_text_plate = Image.open(os.path.join(f"{IMAGE_PATH}//welcome//utils//", f"welcome_plate.png"))
        avatar_img = Image.open(requests.get(member.avatar_url_as(size=1024), stream=True).raw).convert("RGBA")
        avatar_img = round_image(avatar_img.resize((363,363)))
        draw = ImageDraw.Draw(card)
    
        card.paste(alpha_plate, (100,100), alpha_plate)
        card.paste(welcome_text_plate, (569,20), welcome_text_plate)
        card.paste(av_outline_circle, (566,114), av_outline_circle)
        card.paste(avatar_img, ((569,117)), avatar_img)

        _text_width, _h = draw.textsize(f"{member.name}#{member.discriminator}", ImageFont.truetype(os.path.join(f"{IMAGE_PATH}//font//","uni-sans-light.ttf"), 70))
        draw.text(((1500-_text_width)/2 ,501), f"{member.name}", font=ImageFont.truetype(os.path.join(f"{IMAGE_PATH}//font//","uni-sans-light.ttf"), 70), fill=(255,255,255))
        _w, _h = draw.textsize(f"{member.name}", ImageFont.truetype(os.path.join(f"{IMAGE_PATH}//font//","uni-sans-light.ttf"), 70))
        draw.text(((1500-_text_width)/2 + _w + 3,501), f"#{member.discriminator}", font=ImageFont.truetype(os.path.join(f"{IMAGE_PATH}//font//","uni-sans-light.ttf"), 70), fill=(81,81,81))

        _text_width, _h = draw.textsize(f"Member #{member.guild.member_count}", ImageFont.truetype(os.path.join(f"{IMAGE_PATH}//font//","uni-sans-light.ttf"), 55))
        draw.text(((1500-_text_width)/2 ,574), f"Member #{member.guild.member_count}", font=ImageFont.truetype(os.path.join(f"{IMAGE_PATH}//font//","uni-sans-light.ttf"), 55), fill=(255,255,255))

        card.save(os.path.join(f"{IMAGE_PATH}//temp//","temp_welcome.png"))
        await channel.send(file=discord.File(os.path.join(f"{IMAGE_PATH}//temp//","temp_welcome.png")))

    '''
    Begin Custom Error Handling
    '''
    
    @set_colour.error
    async def set_colour_handler(self, ctx, error):
        if "ValueError" in str(error):
            embed = embed_error("Invalid `HEX` value")

def setup(client):
    client.add_cog(ImageManipulation(client))