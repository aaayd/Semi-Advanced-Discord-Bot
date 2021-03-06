<p align="center"><img src="https://cdn.discordapp.com/attachments/833503537479942155/841505138497814559/zenyx_bot_2_small.png" /></p>

# Zen-Bot
An easy to setup, feature-rich, Discord Bot utilising a MongoDB database, powered by Python 3<br>

# Usage
To use the bot, invite it to your server by clicking [here](https://discord.com/api/oauth2/authorize?client_id=813239350702637058&permissions=8&scope=bot) <br>
Alternatively, you can host the bot yourself by cloning the files and going through the setup  
- Note, when hosting yourself, be sure to invite the bot <b>AFTER</b> it is online. This way the bot can initialise important files in the database.

# Features 
- A Website Dashboard
- Games
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
- discord.py
- discord-ext-ipc
- pymongo
- dnspython
- aiohttp
- Quart
- Quart-Discord
- Pillow
- youtube_dl
- numpy
- animals.py
- praw
- fuzzywuzzy
- emojis

# Installation 
1. Open CMD in the same location as the bot root folder
2. Execute the following in the terminal:
```py
# pip install -r requirements.txt
```
<br>

Alternatively, install the libraries manually:
```py
# pip install discord.py
# pip install discord-ext-ipc
# pip install pymongo
# pip install dnspython
# pip install aiohttp
# pip install Quart
# pip install Quart-Discord
# pip install Pillow
# pip install youtube_dl
# pip install numpy
# pip install animals.py
# pip install praw
# pip install fuzzywuzzy
# pip install emojis
```


# Bot Setup
1. Open `protected_vars.env`
2. Set `SRV_URL` to your `MongoDB` Connection URL 
3. Set `TOKEN` to your bot token 
4. Save!

- Optional
5. Change your default `general` and `logs` channel

- Change Default Channels Example: <br>
![image_example](https://cdn.discordapp.com/attachments/833503537479942155/842426219093688320/unknown.png)

# Website Setup
1. Open `protected_vars.env`
2. Set `WEBSITE_ENABLED` to `TRUE`
3. Set `SECRET_KEY` to any secret key you desire; e.g: `1234`
4. Set `IPC_SECRET` to any secret key you desire; e.g: `5678`
5. Set `DISCORD_CLIENT_ID` to your Discord Bot `Client ID`
6. Set `DISCORD_CLIENT_SECRET` to your Discord Bot `Client Secret`
7. Set `DISCORD_REDIRECT_URI` to your website's `URI` (default is `http://127.0.0.1:5000/callback`)
8. Save!

- Note
You can access this website by going to your URI address; e.g: `http://127.0.0.1:5000`

