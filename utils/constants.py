
from datetime import datetime
from main import ROOT, CLUSTER, client
import os, re, requests

# Variables 

ALL_GUILD_DATABASES = dict(
    (db, [collection for collection in CLUSTER[db].collection_names()]) for db in CLUSTER.database_names()
)

IMAGE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'image_processing')
COMMAND_IS_VALID_REGEX = "[a-zA-Z_]+"

CLUSTERS = {
    "CLUSTER_EXPERIENCE" : "leveling",
    "CLUSTER_RATELIMIT" : "xp_rate_limit",
    "CLUSTER_AFK" : "afk",
    "CLUSTER_GAY" : "gay",
    "CLUSTER_DICK" : "dick",
    "CLUSTER_PUSSY" : "pussy",
    "CLUSTER_SHIP" : "ship",
    "CLUSTER_MUTE" : "mute",
    "CLUSTER_SERVER_ROLES" : "utils",
    "CLUSTER_BLACKLIST_WORDS" : "utils",
    "CLUSTER_GIFS" : "utils",
    "CLUSTER_CONFESSION" : "utils",
    "CLUSTER_CHANNELS" : "utils",
}


# Arrays / Dicts

COLOUR_ROLES_DICT = {
    "BLACK" : 0x000000,
    "WHITE" : 0xFFFFFF,
    "RED" : 0xFA1414,
    "ORANGE" : 0xFF6600,
    "YELLOW" : 0xFFFF00,
    "GREEN" : 0x00CC00,
    "CYAN" : 0x00CCFF,
    "BLUE" : 0x0052CC,
    "PURPLE" : 0x8000FF,
    "PINK" : 0xF306C0
}

DEF_SNIPE_GIFS = [
    "https://cdn.discordapp.com/attachments/787823476966162455/819247827376013372/sniper.gif", 
    "https://cdn.discordapp.com/attachments/827207915483955271/827207962484277278/image1-14.gif",
    "https://cdn.discordapp.com/attachments/827207915483955271/827207963147239435/image0-50.gif",
    "https://cdn.discordapp.com/attachments/827207915483955271/827207963633909839/image1-38.gif",
    "https://cdn.discordapp.com/attachments/822133166206484501/827227673629032508/tenor.gif",
    "https://cdn.discordapp.com/attachments/827230906859257866/827231024102113360/image0.gif"
]

PUNCH_GIF_ARRAY = [
    "https://cdn.discordapp.com/attachments/841439376733896705/841483099452080158/f3ec8c256cb22279c14bfdc48c92e5ab.gif",
    "https://cdn.discordapp.com/attachments/841439376733896705/841483198889590804/d7c30e46a937aaade4d7bc20eb09339b.gif",
    "https://cdn.discordapp.com/attachments/841439376733896705/841483318494887936/giphy.gif",
    "https://cdn.discordapp.com/attachments/841439376733896705/841483412967129138/f2kkp3L.gif",
    "https://cdn.discordapp.com/attachments/841439376733896705/841483650985492500/9eUJ.gif",
    "https://cdn.discordapp.com/attachments/841439376733896705/841483719809564702/Omake_Gif_Anime_-_Fairy_Tail_Final_Season_-_Episode_282_-_Lucy_Punch.gif",
    "https://cdn.discordapp.com/attachments/841439376733896705/841483795467206676/8d50607e59db86b5afcc21304194ba57.gif",
    "https://cdn.discordapp.com/attachments/841439376733896705/841483861203615764/giphy.gif"
]

KISS_GIF_ARRAY = [
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

SHIP_RESPONSE_DICT = {
    "SHIP_REALLY_LOW" : [
        "Friendzone ;(", 
        "Just friends", 
        "Friends", 
        "Little to no love", 
        "There's barely any love"
    ],

    "SHIP_LOW" : [
        "Still in the friendzone", 
        "Still in that friendzone", 
        "There's not a lot of love there."
    ],

    "SHIP_POOR" : [
        "But there's a small sense of romance from one person!", 
        "But there's a small bit of love somewhere", 
        "I sense a small bit of love!", 
        "But someone has a bit of love for someone"
    ],

    "SHIP_FAIR" : [
        "There's a bit of love there!", 
        "There is a bit of love there",
        "A small bit of love is in the air"
    ],

    "SHIP_MODERATE" : [
        "But it's very one-sided", 
        "It appears one sided!", 
        "There's some potential!", 
        "I sense a bit of potential!", 
        "There's a bit of romance going on here!", 
        "I feel like there's some romance progressing!", 
        "The love is getting there"
    ],

    "SHIP_GOOD" : [
        "I feel the romance progressing!", 
        "There's some love in the air!", 
        "I'm starting to feel some love!"
    ],

    "SHIP_GREAT" : [
        "There is definitely love somewhere!", 
        "I can see the love is there! Somewhere...", 
        "I definitely can see that love is in the air"
    ],

    "SHIP_OVERAVERAGE" : [
        "Love is in the air!", 
        "I can definitely feel the love", 
        "I feel the love! There's a sign of a match!", 
        "There's a sign of a match!", 
        "I sense a match!", 
        "A few things can be imporved to make this a match made in heaven!"
    ],

    "SHIP_TRUELOVE" : [
        "It's a match!", 
        "There's a match made in heaven!", 
        "It's definitely a match!", 
        "Love is truely in the air!", 
        "Love is most definitely in the air!"
    ]
}

HEART_RESPONSE_LIST = [
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
    ":two_hearts:"
]

EIGHT_BALL_RESPONSE_DICT = {
    "EIGHT_BALL_AFFIRMATIVE" : [
        "It is certain ", 
        "It is decidedly so ", 
        "Without a doubt ", 
        "Yes, definitely ", 
        "You may rely on it ", 
        "As I see it, yes ",
        "Most likely ", 
        "Outlook good ", 
        "Yes ", 
        "Signs point to yes "
    ],

    "EIGHT_BALL_UNSURE" : [
        "Reply hazy try again ", 
        "Ask again later ", 
        "Better not tell you now ", 
        "Cannot predict now ", 
        "Concentrate and ask again "
    ],

    "EIGHT_BALL_NEGATIVE" : [
        "Don't count on it ", 
        "My reply is no ", 
        "My sources say no ", 
        "Outlook not so good ", 
        "Very doubtful "
    ]
}

GAY_RESPONSE_DICT = {
    "GAY_1" : [
        "Suspiciously Straight", 
        "Super Straight"
    ],

    "GAY_2" : [
        "No homo", 
        "Wearing socks", 
        '"Only sometimes"', 
        "Straight-ish", 
        "No homo bro", 
        "Girl-kisser", 
        "Hella straight"
    ],

    "GAY_3" : [
        "Possible homo", 
        "My gay-sensor is picking something up", 
        "I can't tell if the socks are on or off", 
        "Gay-ish", 
        "Looking a bit homo", 
        "lol half  g a y", 
        "safely inbetween for now"
    ],

    "GAY_4" : [
        "HOMO ALERT", 
        "MY GAY-SENSOR IS OFF THE CHARTS", 
        "STINKY GAY", 
        "GAY AS FUCK", 
        "THE SOCKS ARE OFF", 
        "HELLA GAY"
    ]
}

PUSSY_RESPONSE_DICT = {
    "PUSSY_SIZE_SMALL" : [
        "Tiny Pussy", 
        "Virgin"
    ],

    "PUSSY_SIZE_MEDIUM" : [
        "Body count of 1", 
        "Taken an average dick", 
        "Nuttable"
    ],

    "PUSSY_SIZE_LARGE" : [
        "Kinda loose", 
        "You know your way around a dick", 
        "Body count of 3-5"
    ],

    "PUSSY_SIZE_BUCKET" : [
        "Bucket", 
        "Been through every guy you've met", 
        "Your pussy stink", 
        "Dirty Slag"
    ]
}

# Functions

def get_cluster(guild, cluster, clusters = CLUSTERS):
    val = clusters.get(cluster)
    return CLUSTER[str(guild)][val]

def update_channel_id(var, _chan_id):
    _old_value = str(var[0]).split('=')[0]

    if str(var[0]) == 123456789 or len(str(var[0])) <= 9:
        var.append(_chan_id)
        var.pop(0) 
        with open(ROOT +'\protected_vars.env') as file:
            new_text = file.read().replace(str(_old_value), str(_chan_id))
            
        with open(ROOT +'\protected_vars.env', "w") as file:
            file.write(new_text)
 
def get_level(xp):
    lvl = 0
    while True:
        if xp < ((50*(lvl**2))+(50*(lvl))):
            break
        lvl += 1
    return lvl

def get_rank(member, _db):
    rankings = _db.find().sort("xp", -1)
    for iter,rank in enumerate(list(rankings)):
        if rank["id"] == member.id:
            return iter + 1

def converter(time):
    time_converter={
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400,
        'w': 604800}

    time = re.sub('[^a-zA-Z]+', '', time)
    return time_converter.get(time,"Invalid Timeframe.")

def query_valid_url(url):
    request = requests.get(url)
    if request.status_code == 400:
        return False
    return True

def get_command_description(command):
    return client.get_command(command).help

def get_channel_id(guild_id, channel_name):
    return get_cluster(guild_id, "CLUSTER_CHANNELS").find_one({"id" : "type_important_channels"})["dict"][channel_name]
# Functions
def get_time_elapsed(afk_date):
    elapsed_time = datetime.utcnow() - afk_date
    seconds = elapsed_time.total_seconds()
    days = seconds // 86400
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    string = ""
    if days != 0.0:
        string += f"{round(days)} day" if days == 1.0 else f"{round(days)} days"

    elif hours != 0.0:
        string += f"{round(hours)} hour" if hours == 1.0 else f"{round(hours)} hours"

    elif minutes != 0.0:
        string += f"{round(minutes)} minute" if minutes == 1.0 else f"{round(minutes)} minutes"
    
    else:
        string += f"{round(seconds)} second" if hours == 1.0 else f"{round(seconds)} seconds"
    return string

def _init_mongo_arr(cluster, _id, default_vars = []):
    _exists = cluster.find_one({
        "id": _id
    })

    if _exists is None:
        cluster.insert_one({
            "id": _id, 
            "array": []
        })
        
        for var in default_vars:
            cluster.update({
                "id" : _id}, 
                    {"$push" : {
                        "array" : var
                    }
                })

def _init_mongo_dict(cluster, _id, default_dict = {}):
    _exists = cluster.find_one({
        "id": _id
    })

    if _exists is None:
        cluster.insert_one({
            "id": _id, 
            "dict": {}
        })
    
        for key, value in default_dict.items():
            cluster.update({
                "id" : _id}, 
                    {"$set" : {
                        f"dict.{key}" : int(value) 
                    }
                })

def _init_mongo_bool(cluster, _id, bool = True):
        _exists = cluster.find_one({
            "id": _id
        })

        if _exists is None:
            cluster.insert_one({
                "id": _id, 
                "bool": bool
            })

