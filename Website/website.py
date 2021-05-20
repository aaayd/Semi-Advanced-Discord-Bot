from quart import Quart, render_template, request, session, redirect, url_for
from quart_discord import DiscordOAuth2Session
from discord.ext import ipc

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

	guild_count = await ipc_client.request("get_guild_count")
	user_guilds = await discord.fetch_guilds()
	
	guilds = [guild for guild in user_guilds if guild.permissions.administrator]

	for guild in guilds:
		guild_temp = await ipc_client.request("get_guild", guild_id = guild.id)

		if guild_temp is None:
			guild.in_server = False
		else:
			guild.in_server = True

	member = await discord.fetch_user()
	return await render_template(
		"dashboard.html", guild_count = guild_count, guilds = guilds, member=member, join_url = f'https://discord.com/api/oauth2/authorize?client_id=813239350702637058&permissions=8&scope=bot'
		)

@app.route("/dashboard/<int:guild_id>")
async def dashboard_server(guild_id):
	if not await discord.authorized:
		return redirect(url_for("login")) 

	guild = await ipc_client.request("get_guild", guild_id = guild_id)

	
	if guild is None:
		return redirect(f'https://discord.com/oauth2/authorize?&client_id={app.config["DISCORD_CLIENT_ID"]}&scope=bot&permissions=8&guild_id={guild_id}&response_type=code&redirect_uri={app.config["DISCORD_REDIRECT_URI"]}')
	
	guilds = await discord.fetch_guilds()
	guild = [guild for guild in guilds if int(guild.id) == int(guild_id)][0]
	print(guild)
	return await render_template(
		"guild_id.html", guild=guild
	)


if __name__ == "__main__":
	app.run(debug=True)