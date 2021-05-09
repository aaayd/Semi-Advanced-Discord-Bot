# Zenyx-Bot
An easy to setup Discord bot utilising a MongoDB database made in Python 

# Features 
- MongoDB Backend 
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
- Pillow 
- pymongo

# Installation 
```py
# pip install discordpy 
# pip install Pillow
# pip install pymongo 
```

# Setup
1. Open `protected_vars.env`
2. Set `SRV_URL` to your `MongoDB` Connection URL 

- Change default `General` text channel 
1. `?change_channel` `general` `[new_channel_id]`

- Change default `Logs` text channel 
1. `?change_channel` `logs` `[new_channel_id]`




