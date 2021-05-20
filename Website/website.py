from quart import Quart, render_template, request, session, redirect, url_for
from quart_discord import DiscordOAuth2Session
from discord.ext import ipc
from pymongo import MongoClient
import discord

app = Quart(__name__)
ipc_client = ipc.Client(secret_key = "Swas")

from re import compile
with open('Website\protected_website_vars.env') as ins:
    result = {}
    for line in ins:
        match = compile(r'''^([^\s=]+)=(?:[\s"']*)(.+?)(?:[\s"']*)$''').match(line)
        if match is not None:
            result[match.group(1)] = match.group(2)


app.config["SECRET_KEY"] = str(result["SECRET_KEY"])
app.config["DISCORD_CLIENT_ID"] = int(result["DISCORD_CLIENT_ID"])   # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = str(result["DISCORD_CLIENT_SECRET"])   # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = str(result["DISCORD_REDIRECT_URI"])

CLUSTER = MongoClient(result["SRV_URL"])
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


def get_cluster(guild, cluster, clusters = CLUSTERS):
    val = clusters.get(cluster)
    return CLUSTER[str(guild)][val]

def get_channel_id(guild_id, channel_name):
    return get_cluster(guild_id, "CLUSTER_CHANNELS").find_one({"id" : "type_important_channels"})["dict"][channel_name]
discord = DiscordOAuth2Session(app)

@app.route("/")
async def home():
	return await render_template("index.html", authorized = await discord.authorized)

@app.route("/login")
async def login():
	return await discord.create_session()

@app.route("/callback")
async def callback():
	try:
		await discord.callback()
	except Exception:
		pass

	return redirect(url_for("dashboard"))

@app.route("/dashboard")
async def dashboard():
	if not await discord.authorized:
		return redirect(url_for("login")) 

	guilds = [guild for guild in await discord.fetch_guilds() if guild.permissions.administrator]

	for guild in guilds:
		guild_temp = await ipc_client.request("get_guild", guild_id = guild.id)

		if guild_temp is None:
			guild.in_server = False
		else:
			guild.in_server = True

	member = await discord.fetch_user()
	return await render_template(
		"dashboard.html", guilds = guilds, member=member, join_url = f'https://discord.com/api/oauth2/authorize?client_id=813239350702637058&permissions=8&scope=bot'
		)

@app.route("/dashboard/<int:guild_id>")
async def dashboard_server(guild_id):
	if not await discord.authorized:
		return redirect(url_for("login")) 

	guild = await ipc_client.request("get_guild", guild_id = guild_id)

	_db_important_channels = get_cluster(guild_id, "CLUSTER_CHANNELS").find_one({"id" : "type_important_channels"})["dict"]

	if guild is None:
		return redirect(f'https://discord.com/oauth2/authorize?&client_id={app.config["DISCORD_CLIENT_ID"]}&scope=bot&permissions=8&guild_id={guild_id}&response_type=code&redirect_uri={app.config["DISCORD_REDIRECT_URI"]}')
		
	return await render_template(
		"guild_id.html", guild=guild, _db_important_channels=_db_important_channels
	)




if __name__ == "__main__":
	app.run(debug=True)