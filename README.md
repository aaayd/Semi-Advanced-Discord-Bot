<p align="center"><img src="https://cdn.discordapp.com/attachments/833503537479942155/841505138497814559/zenyx_bot_2_small.png" /></p>

# Zen-Bot
An easy to setup Discord bot utilising a MongoDB database made in Python <br>

# Usage
To use the bot, invite it to your server by clicking [here](https://discord.com/api/oauth2/authorize?client_id=813239350702637058&permissions=8&scope=bot) <br>
Alternatively, you can host the bot yourself by cloning the files and going through the setup  
- Note, when hosting yourself, be sure to invite the bot <b>AFTER</b> it is online. This way the bot can initialise important files in the database.

# Features 
- MongoDB Backend 
- Supports Multiple Servers (and so does the Database!)
- Ranking System
- Custom Image Manipulated Cards 
- Easily Customisable Rank Cards 
- Custom Error Handling 
- Plays music w/ search engine 

Rank Card Example
![rank_card](https://cdn.discordapp.com/attachments/665771066085474346/840510892516704296/card_temp-1.png)

Welcome Card Example
![welcome_card](https://cdn.discordapp.com/attachments/665771066085474346/840511453454532648/temp_welcome.png)
# Requirements 
1. Python 3

# Libraries 
- discordpy 
- discord-ext-ipc 
- Pillow 
- pymongo
- dnspython
- aiodns
- fuzzywuzzy
- quart
- quart_discord

# Installation 
1. Open CMD in the same location as the bot root folder
2. Execute the following in the terminal:
```py
# pip install requirements.txt
```
<br>

Alternatively, install the libraries manually:
```py
# pip install discordpy 
# pip install discord-ext-ipc 
# pip install Pillow
# pip install pymongo
# pip install fuzzywuzzy 
# pip install emojis
# pip install quart
# pip install quart_discord
```


# Setup
1. Open `protected_vars.env`
2. Set `SRV_URL` to your `MongoDB` Connection URL 
3. Set `TOKEN` to your bot token 
4. Save `protected_vars.env`
5. Run `bot.py`
6. Change your default `general` and `logs` channel 

- Change Default Channels Example: <br>
![image_example](https://cdn.discordapp.com/attachments/833503537479942155/842426219093688320/unknown.png)
