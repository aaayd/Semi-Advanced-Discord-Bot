import discord , random
from discord.ext import commands, tasks
from discord import Embed
from datetime import datetime
import random
from main import CLUSTER

GAY_DB = CLUSTER["discord_fun"]["gay"]
DICK_DB = CLUSTER["discord_fun"]["dick"]
PUSSY_DB = CLUSTER["discord_fun"]["pussy"]
SHIP_DB = CLUSTER["discord_fun"]["ship"]
BULLY_SAM_BOOL = CLUSTER["discord"]["utils"].find_one({"id": "type_bully_sam"})["bully_sam"]

async def get(session: object, url: object) -> object:
    async with session.get(url) as response:
        return await response.text()

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if BULLY_SAM_BOOL:
            if before.id == 608090925524189319:
                if (before.nick != after.nick) and "jeep" not in after.nick.lower():
                    await after.edit(nick=f"{after.nick} [JEEP]") 
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if BULLY_SAM_BOOL:
            if message.author.id == 608090925524189319:
                if "stop" in message.content.lower():
                    await message.channel.send("No, jeep, this wont stop.")
                    
                if random.randint(0,100) > 87:
                    phrases = [
                        "Who asked?",
                        "Does it look like I care, jeep.",
                        "OK? Shut up bitch",
                        "Shut up, Jeep, you have no rights",
                        "OK? And? Shut up.",
                        "Nobody cares.",
                        "Look, a jeep who thinks he can talk!",
                        "Oh well, you wasted your time, jeep",
                        "Honk honk"
                    ]
                    try:
                        await message.delete()
                    except:
                        pass
                    await message.channel.send(random.choice(phrases))
                
                if random.randint(0,100) > 93:
                    nicks = [
                        "IM A STINKY JEEP",
                        "JEEPY JEEPY JEEPY",
                        "jeep",
                        "HONK HONK WEENIE JEEP",
                        "I EAT SLEEP DREAM JEEPS",
                        "FUCK ME IM A JEEP",
                        "IM A JEEP I HAVE NO RIGHTS",
                        "Jeepy Jeepy"   
                    ]
                    
                    a = list(random.choice(nicks).lower())
                    a[1::2] = [x.upper() for x in a[1::2]]
                    s = ''.join(a)
                    await message.author.edit(nick=s)
                
                if random.randint(0,100) > 87:
                    try:
                        a = list(message.content.lower())
                        a[1::2] = [x.upper() for x in a[1::2]]
                        await message.delete()
                        await message.channel.send(f"{message.author.mention}: {''.join(a)}")
                    except:
                        try:
                            await message.delete()
                        except:
                            pass


                emoji = [emoji for emoji in message.guild.emojis if emoji.name == "jeep"][0]
                emoji = self.client.get_emoji(id=emoji.id)
                try:
                    await message.add_reaction(emoji)
                except:
                    pass


    @commands.command()
    async def kiss(self, ctx, member: discord.Member = None):
        if member is None:
            return

        variable_list = [
            'https://media1.tenor.com/images/32d4f0642ebb373e3eb072b2b91e6064/tenor.gif?itemid=15150255',
            'https://media1.tenor.com/images/a390476cc2773898ae75090429fb1d3b/tenor.gif?itemid=12837192',
            'https://media1.tenor.com/images/558f63303a303abfdddaa71dc7b3d6ae/tenor.gif?itemid=12879850',
            'https://media1.tenor.com/images/7fd98defeb5fd901afe6ace0dffce96e/tenor.gif?itemid=9670722',
            'https://media1.tenor.com/images/558f63303a303abfdddaa71dc7b3d6ae/tenor.gif?itemid=12879850',
            'https://media1.tenor.com/images/693602b39a071644cebebdce7c459142/tenor.gif?itemid=6206552',
            'https://media1.tenor.com/images/105a7ad7edbe74e5ca834348025cc650/tenor.gif?itemid=9158317',
            'https://media1.tenor.com/images/503bb007a3c84b569153dcfaaf9df46a/tenor.gif?itemid=17382412',
            'https://media1.tenor.com/images/78095c007974aceb72b91aeb7ee54a71/tenor.gif?itemid=5095865',
            'https://media1.tenor.com/images/ea9a07318bd8400fbfbd658e9f5ecd5d/tenor.gif?itemid=12612515',
            'https://media1.tenor.com/images/3d56f6ef81e5c01241ff17c364b72529/tenor.gif?itemid=13843260',
            'https://media1.tenor.com/images/bc5e143ab33084961904240f431ca0b1/tenor.gif?itemid=9838409',
            'https://media1.tenor.com/images/7fd98defeb5fd901afe6ace0dffce96e/tenor.gif?itemid=9670722',
            'https://media1.tenor.com/images/f102a57842e7325873dd980327d39b39/tenor.gif?itemid=12392648',
            'https://media1.tenor.com/images/02d9cae34993e48ab5bb27763d5ca2fa/tenor.gif?itemid=4874618',
            'https://media1.tenor.com/images/e76e640bbbd4161345f551bb42e6eb13/tenor.gif?itemid=4829336',
            'https://media1.tenor.com/images/f5167c56b1cca2814f9eca99c4f4fab8/tenor.gif?itemid=6155657',
            'https://media1.tenor.com/images/621ceac89636fc46ecaf81824f9fee0e/tenor.gif?itemid=4958649',
            'https://media1.tenor.com/images/a1f7d43752168b3c1dbdfb925bda8a33/tenor.gif?itemid=10356314',
            'https://media1.tenor.com/images/1306732d3351afe642c9a7f6d46f548e/tenor.gif?itemid=6155670',
            'https://media1.tenor.com/images/6f455ef36a0eb011a60fad110a44ce68/tenor.gif?itemid=13658106',
            'https://media1.tenor.com/images/b8d0152fbe9ecc061f9ad7ff74533396/tenor.gif?itemid=5372258',
            'https://media1.tenor.com/images/d0cd64030f383d56e7edc54a484d4b8d/tenor.gif?itemid=17382422',
            'https://media1.tenor.com/images/a390476cc2773898ae75090429fb1d3b/tenor.gif?itemid=12837192',
            'https://media1.tenor.com/images/ba1841e4aeb5328e41530d3289616f46/tenor.gif?itemid=14240425',
            'https://media1.tenor.com/images/4b5d5afd747fe053ed79317628aac106/tenor.gif?itemid=5649376',
            'https://media1.tenor.com/images/e00f3104927ae27d7d6a32393d163176/tenor.gif?itemid=12192866',
            'https://media1.tenor.com/images/4c66d14c58838d05376b5d2712655d91/tenor.gif?itemid=15009390',
            'https://media1.tenor.com/images/ef4a0bcb6e42189dc12ee55e0d479c54/tenor.gif?itemid=12143127',
            'https://media1.tenor.com/images/230e9fd40cd15e3f27fc891bac04248e/tenor.gif?itemid=14751754',
    
        ]
        embed = discord.Embed(title = "", description=f"{ctx.message.author.mention} Kissed {member.mention}, How Sweet :heart:", color=0xc81f9f,
            ).set_image(url=f"{random.choice(variable_list)}"
        )
        await ctx.send(embed=embed)


    @commands.command(aliases=["diceroll"])
    async def rolldice(self, ctx):
        """Roll some die"""

        embed= discord.Embed(description=(f"You rolled a {random.randint(1, 6)}!"), timestamp=datetime.now()
            ).set_author(name=f"Dice Roll", icon_url=f"https://www.freeiconspng.com/thumbs/dice-png/dice-png-transparent-images--png-all-4.png"
        )
        await ctx.send(embed=embed)


    @commands.command(aliases=["flipcoin", "fiftyfifty", "5050"])
    async def coinflip(self, ctx):
        """Flip a coin"""
        choices = ["heads", "tails"]
        
        embed= discord.Embed(description=(f"{random.choice(choices).capitalize()}!"), timestamp=datetime.now()
            ).set_author(name=f"Coin Flip", icon_url=f"https://www.pngarts.com/files/3/Silver-Coin-Transparent-Background-PNG.png"
        )
        await ctx.send(embed=embed)



    @commands.command()
    async def gayav(self, ctx, member : discord.Member = None):
        if member is None:
            member = ctx.author
        
        url = f'https://some-random-api.ml/canvas/gay?avatar={member.avatar_url}'
        if url.endswith(".webp?size=1024"):
            url = url[:-len(".webp?size=1024")]
        
        elif url.endswith(".gif?size=1024"):
            url = url[:-len(".gif?size=1024")]

        await ctx.send(embed=Embed(
            title=f"Gay Avatar for {member.display_name}", timestamp=datetime.now(), url=url
        ).set_image(url=url))

    @commands.command(aliases=["simp"])
    async def ship(self, ctx, member : discord.Member=None, member2:discord.Member=None):
        try:
            if member is None or member2 is None:
                return

            members = [member.id, member2.id]
            members.sort()

            _find_user = SHIP_DB.find_one({"member_one" : members[0], "member_two": members[1]})
            
            if _find_user is None:
                shipnumber = random.randint(0,100)
                new_ship = ({"member_one" : members[0], "member_two": members[1], "rating": shipnumber})
                SHIP_DB.insert(new_ship)

                _find_user = SHIP_DB.find_one({"member_one" : members[0], "member_two": members[1]})
            
            shipnumber = _find_user["rating"]
            if 0 <= shipnumber <= 10:
                status = "Really low! {}".format(random.choice(["Friendzone ;(", 
                                                                'Just "friends"', 
                                                                '"Friends"', 
                                                                "Little to no love ;(", 
                                                                "There's barely any love ;("]))
            elif 10 < shipnumber <= 20:
                status = "Low! {}".format(random.choice(["Still in the friendzone", 
                                                        "Still in that friendzone ;(", 
                                                        "There's not a lot of love there... ;("]))
            elif 20 < shipnumber <= 30:
                status = "Poor! {}".format(random.choice(["But there's a small sense of romance from one person!", 
                                                        "But there's a small bit of love somewhere", 
                                                        "I sense a small bit of love!", 
                                                        "But someone has a bit of love for someone..."]))
            elif 30 < shipnumber <= 40:
                status = "Fair! {}".format(random.choice(["There's a bit of love there!", 
                                                        "There is a bit of love there...", 
                                                        "A small bit of love is in the air..."]))
            elif 40 < shipnumber <= 60:
                status = "Moderate! {}".format(random.choice(["But it's very one-sided OwO", 
                                                            "It appears one sided!", 
                                                            "There's some potential!", 
                                                            "I sense a bit of potential!", 
                                                            "There's a bit of romance going on here!", 
                                                            "I feel like there's some romance progressing!", 
                                                            "The love is getting there..."]))
            elif 60 < shipnumber <= 70:
                status = "Good! {}".format(random.choice(["I feel the romance progressing!", 
                                                        "There's some love in the air!", 
                                                        "I'm starting to feel some love!"]))
            elif 70 < shipnumber <= 80:
                status = "Great! {}".format(random.choice(["There is definitely love somewhere!", 
                                                        "I can see the love is there! Somewhere...", 
                                                        "I definitely can see that love is in the air"]))
            elif 80 < shipnumber <= 90:
                status = "Over average! {}".format(random.choice(["Love is in the air!", 
                                                                "I can definitely feel the love", 
                                                                "I feel the love! There's a sign of a match!", 
                                                                "There's a sign of a match!", 
                                                                "I sense a match!", 
                                                                "A few things can be imporved to make this a match made in heaven!"]))
            elif 90 < shipnumber <= 100:
                status = "True love! {}".format(random.choice(["It's a match!", 
                                                            "There's a match made in heaven!", 
                                                            "It's definitely a match!", 
                                                            "Love is truely in the air!", 
                                                            "Love is most definitely in the air!"]))

            if shipnumber <= 33:
                shipColor = 0xE80303
            elif 33 < shipnumber < 66:
                shipColor = 0xff6600
            else:
                shipColor = 0x3be801

            emb = (discord.Embed(color=shipColor, \
                                title="Simp rate for:", \
                                description="**{0}** and **{1}** {2}".format(member, member2, random.choice([
                                                                                                            ":sparkling_heart:", 
                                                                                                            ":heart_decoration:", 
                                                                                                            ":heart_exclamation:", 
                                                                                                            ":heartbeat:", 
                                                                                                            ":heartpulse:", 
                                                                                                            ":hearts:", 
                                                                                                            ":blue_heart:", 
                                                                                                            ":green_heart:", 
                                                                                                            ":purple_heart:", 
                                                                                                            ":revolving_hearts:", 
                                                                                                            ":yellow_heart:", 
                                                                                                            ":two_hearts:"]))))
            emb.add_field(name="Results:", value=f"{shipnumber}%", inline=True)
            emb.add_field(name="Status:", value=(status), inline=False)
            emb.set_author(name="Shipping", icon_url="http://moziru.com/images/kopel-clipart-heart-6.png")
            await ctx.send(embed=emb)
        except Exception as e:
            print(e)
        
    @commands.command(aliases=['8ball'])
    async def eightball(self, ctx, *, _ballInput):
        """extra generic just the way you like it"""
        choiceType = random.choice(["(Affirmative)", "(Non-committal)", "(Negative)"])
        if choiceType == "(Affirmative)":
            prediction = random.choice(["It is certain ", 
                                        "It is decidedly so ", 
                                        "Without a doubt ", 
                                        "Yes, definitely ", 
                                        "You may rely on it ", 
                                        "As I see it, yes ",
                                        "Most likely ", 
                                        "Outlook good ", 
                                        "Yes ", 
                                        "Signs point to yes "]) + ":8ball:"

            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0x3be801, description=prediction))
        elif choiceType == "(Non-committal)":
            prediction = random.choice(["Reply hazy try again ", 
                                        "Ask again later ", 
                                        "Better not tell you now ", 
                                        "Cannot predict now ", 
                                        "Concentrate and ask again "]) + ":8ball:"
            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0xff6600, description=prediction))
        elif choiceType == "(Negative)":
            prediction = random.choice(["Don't count on it ", 
                                        "My reply is no ", 
                                        "My sources say no ", 
                                        "Outlook not so good ", 
                                        "Very doubtful "]) + ":8ball:"
            emb = (discord.Embed(title="Question: {}".format(_ballInput), colour=0xE80303, description=prediction))
        emb.set_author(name='Magic 8 ball', icon_url='https://www.horoscope.com/images-US/games/game-magic-8-ball-no-text.png')
        await ctx.send(embed=emb)

    @commands.command()
    async def guess(self, ctx, guess):
        answer = random.randint(1,100)
        await ctx.send(answer)

        if guess > answer:
            await ctx.send("Guess is higher than the answer")
        elif guess < answer:
            await ctx.send("Guess is lower than the answer")
        else:
            await ctx.send("Correct!!")
    @commands.command(aliases=['gay-scanner', 'gayscanner', 'gay'])
    async def gay_scanner(self, ctx, member : discord.Member=None):
        if member == None:
            member = ctx.author
        

        _find_user = GAY_DB.find_one({"id" : member.id})
        
        if _find_user is None:
            gayness = random.randint(0,100)
            new_gay_client = ({"id": member.id, "gay_rating": gayness})
            GAY_DB.insert(new_gay_client)
            _find_user = GAY_DB.find_one({"id" : member.id})
        
        gayness = _find_user["gay_rating"]
        gayColor = 0xFFFFFF
        if gayness <= 10:
            gayStatus = random.choice(["Suspiciously Straight", 
                                    "Super Straight"])
        elif 10 < gayness < 33:
            gayStatus = random.choice(["No homo", 
                                    "Wearing socks", 
                                    '"Only sometimes"', 
                                    "Straight-ish", 
                                    "No homo bro", 
                                    "Girl-kisser", 
                                    "Hella straight"])
            gayColor = 0xFFC0CB
        elif 33 < gayness < 66:
            gayStatus = random.choice(["Possible homo", 
                                    "My gay-sensor is picking something up", 
                                    "I can't tell if the socks are on or off", 
                                    "Gay-ish", 
                                    "Looking a bit homo", 
                                    "lol half  g a y", 
                                    "safely inbetween for now"])
            gayColor = 0xFF69B4
        else:
            gayStatus = random.choice([ "HOMO ALERT", 
                                    "MY GAY-SENSOR IS OFF THE CHARTS", 
                                    "STINKY GAY", 
                                    "GAY AS FUCK", 
                                    "THE SOCKS ARE OFF", 
                                    "HELLA GAY"])
            gayColor = 0xFF00FF
        emb = discord.Embed(description=f"Gayness for **{member }**", color=gayColor)
        emb.add_field(name="Gayness:", value=f"{gayness}% gay")
        emb.add_field(name="Comment:", value=f"{gayStatus} :kiss_mm:")
        emb.set_author(name="Gay-Scanner™", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/ICA_flag.svg/2000px-ICA_flag.svg.png")
        await ctx.send(embed=emb)

    @commands.command(aliases=['pussy'])
    async def pussy_size(self, ctx, member : discord.Member=None):
        if member == None:
            member = ctx.author
        

        _find_user = PUSSY_DB.find_one({"id" : member.id})
        
        if _find_user is None:
            size = random.randint(0,100)
            new_pussy = ({"id": member.id, "pussy_size": size})
            PUSSY_DB.insert(new_pussy)
            _find_user = PUSSY_DB.find_one({"id" : member.id})
        
        size = _find_user["pussy_size"]

        colour = 0xFFFFFF
        if size <= 20:
            status = random.choice(["Tiny Pussy", 
                                    "Virgin"
                                    ])
        elif 20 < size < 50:
            status = random.choice(["Body count of 1", 
                                    "Taken an average dick", 
                                    "Nuttable"
                                    ])
            colour = 0xFFC0CB

        elif 50 < size < 66:
            status = random.choice(["Kinda loose", 
                                    "You know your way around a dick", 
                                    "Body count of 3-5"
                                    ])
            colour = 0xFF69B4
        else:
            status = random.choice(["Bucket", 
                                    "Been through every guy you've met", 
                                    "Your pussy stink", 
                                    "Dirty Slag"])
            colour = 0xFF00FF
        emb = discord.Embed(description=f"Pussy Size for **{member }**", color=colour)
        emb.add_field(name="Pussy Size:", value=f"{status}")
        emb.set_author(name="Pussy-Scanner™", icon_url="https://assets.stickpng.com/images/580b585b2edbce24c47b2792.png")
        await ctx.send(embed=emb)

    @commands.command()
    async def dick(self, ctx, member : discord.Member=None):
        if member == None:
            member = ctx.author
        

        _find_user = DICK_DB.find_one({"id" : member.id})
        
        if _find_user is None:
            dick_size = f"8{'='*random.randint(1,12)}3"
            new_dick_size = ({"id": member.id, "dick_size": dick_size})
            DICK_DB.insert(new_dick_size)
            _find_user = DICK_DB.find_one({"id" : member.id})
        
        dick_size = _find_user["dick_size"]
        gayColor = 0xFFFFFF
       
        emb = discord.Embed(description=f"Dick size for **{member }**", color=gayColor)
        emb.add_field(name="Dick Size:", value=f"{dick_size}\n{len(dick_size)-1} Inches")
        emb.set_author(name="Dick-Detector™", icon_url="https://static.thenounproject.com/png/113312-200.png")
        await ctx.send(embed=emb)

def setup(client):
    client.add_cog(Fun(client))
