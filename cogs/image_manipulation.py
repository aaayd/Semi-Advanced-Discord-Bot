import discord, requests, os, random
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw, ImageChops
from utils.constant_strings import CHANNEL_GENERAL_ID, GUILD_ID


path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'image_processing')
class ImageManipulatioon(commands.Cog):
    def __init__(self, client):
        self.client = client

    def round_image(self, image):
        bigsize = (image.size[0] * 3, image.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        ImageDraw.Draw(mask).ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(image.size, Image.ANTIALIAS)
        mask = ImageChops.darker(mask, image.split()[-1])
        image.putalpha(mask)
        return image

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(int(CHANNEL_GENERAL_ID))
        card = Image.open(os.path.join(f"{path}//welcome//backgrounds//", f"background_{random.randint(1,14)}.png"))
        av_outline_circle = Image.open(os.path.join(f"{path}//welcome//utils//", f"black_circle.png"))
        alpha_plate = Image.open(os.path.join(f"{path}//welcome//utils//", f"alpha_plate.png"))
        welcome_text_plate = Image.open(os.path.join(f"{path}//welcome//utils//", f"welcome_plate.png"))
        avatar_img = Image.open(requests.get(member.avatar_url_as(size=1024), stream=True).raw).convert("RGBA")
        avatar_img = self.round_image(avatar_img.resize((363,363)))
        draw = ImageDraw.Draw(card)
    
        card.paste(alpha_plate, (100,100), alpha_plate)
        card.paste(welcome_text_plate, (569,20), welcome_text_plate)
        card.paste(av_outline_circle, (566,114), av_outline_circle)
        card.paste(avatar_img, ((569,117)), avatar_img)

        _text_width, _h = draw.textsize(f"{member.name}#{member.discriminator}", ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 70))
        draw.text(((1500-_text_width)/2 ,501), f"{member.name}", font=ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 70), fill=(255,255,255))
        _w, _h = draw.textsize(f"{member.name}", ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 70))
        draw.text(((1500-_text_width)/2 + _w + 3,501), f"#{member.discriminator}", font=ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 70), fill=(81,81,81))

        _text_width, _h = draw.textsize(f"Member #{self.client.get_guild(int(GUILD_ID)).member_count}", ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 55))
        draw.text(((1500-_text_width)/2 ,574), f"Member #{self.client.get_guild(int(GUILD_ID)).member_count}", font=ImageFont.truetype(os.path.join(f"{path}//font//","uni-sans-light.ttf"), 55), fill=(255,255,255))

        card.save(os.path.join(f"{path}//temp//","temp_welcome.png"))
        await channel.send(file=discord.File(os.path.join(f"{path}//temp//","temp_welcome.png")))

def setup(client):
    client.add_cog(ImageManipulatioon(client))