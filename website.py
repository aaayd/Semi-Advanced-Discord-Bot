from quart import Quart, render_template, request, redirect, url_for
from quart_discord import DiscordOAuth2Session
from discord.ext import ipc, commands
from bot import bot
from datetime import datetime
from Bot.utils.constants import get_cluster, get_channel_id
import discord, os, asyncio
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'loggers': {
        'quart.app': {
            'level': 'ERROR',
        },
        'quart.serving': {
            'level': 'ERROR',
        },
    },
})

template_folder_path = os.path.abspath('Website/src')
static_folder_path = os.path.abspath('Website/static')
app = Quart(__name__, template_folder = template_folder_path, static_folder = static_folder_path)
ipc_client = ipc.Client(secret_key = bot.env_vars["IPC_SECRET"])
app.config["SECRET_KEY"] = str(bot.env_vars["SECRET_KEY"])
app.config["DISCORD_CLIENT_ID"] = int(bot.env_vars["DISCORD_CLIENT_ID"])   # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = str(bot.env_vars["DISCORD_CLIENT_SECRET"])   # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = str(bot.env_vars["DISCORD_REDIRECT_URI"])
discord_auth = DiscordOAuth2Session(app)

class DiscordClient:
	def __init__(self):
		self.bot = discord.Client(intents=discord.Intents.all())
		
	async def get_guild(self, id):
		await self.bot.wait_until_ready()
		
		return self.bot.get_guild(id)

	async def get_channel(self, id):
		await self.bot.wait_until_ready()

		return self.bot.get_channel(id)
		
class Website(commands.Cog, name = "Website COG"):
	def __init__(self, bot):
		self.bot = bot
	
	@app.before_serving
	async def before_serving():
		loop = asyncio.get_event_loop()
		app.discord_client = DiscordClient()

		await app.discord_client.bot.login(bot.env_vars["TOKEN"])
		loop.create_task(app.discord_client.bot.connect())

	@app.route("/")
	async def home():
		client_id = app.config["DISCORD_CLIENT_ID"]
		return await render_template("index.html", authorized = await discord_auth.authorized, client_id=client_id)

	@app.route("/login")
	async def login():
		return await discord_auth.create_session()

	@app.route("/callback")
	async def callback():
		try:
			await discord_auth.callback()
		except Exception:
			pass

		return redirect(url_for("dashboard"))

	@app.route("/dashboard")
	async def dashboard():
		if not await discord_auth.authorized:
			return redirect(url_for("login")) 
			

		guilds = [guild for guild in await discord_auth.fetch_guilds() if guild.permissions.administrator]

		for guild in guilds:
			guild_temp = await ipc_client.request("get_guild", guild_id = guild.id)

			if guild_temp is None:
				guild.in_server = False
			else:
				guild.in_server = True

		member = await discord_auth.fetch_user()
		return await render_template(
			"dashboard.html", guilds = guilds, member=member, join_url = f'https://discord.com/api/oauth2/authorize?client_id={app.config["DISCORD_CLIENT_ID"]}&permissions=8&scope=bot'
			)

	@app.route("/dashboard/<int:guild_id>")
	async def dashboard_server(guild_id):
		
		if not await discord_auth.authorized:
			return redirect(url_for("login")) 

		guild = await ipc_client.request("get_guild", guild_id = guild_id)
		commands  = await ipc_client.request("get_all_commands")
		cogs = await ipc_client.request("get_all_cogs")
		channels = await ipc_client.request("get_all_channels", guild_id = guild_id)

		_db_important_channels = get_cluster(guild_id, "CLUSTER_CHANNELS").find_one({"id" : "type_important_channels"})["dict"]
		_db_commands = get_cluster(guild_id, "CLUSTER_CHANNELS").find_one({"id" : "type_command_activity"})["dict"]
		_db_warns = get_cluster(guild_id, "CLUSTER_WARN").find().sort("time", -1)

		if guild is None:
			return redirect(f'https://discord.com/oauth2/authorize?&client_id={app.config["DISCORD_CLIENT_ID"]}&scope=bot&permissions=8&guild_id={guild_id}&response_type=code&redirect_uri={app.config["DISCORD_REDIRECT_URI"]}')
			
		return await render_template(
			"guild_id.html", guild=guild, 
			_db_important_channels=_db_important_channels, 
			commands=commands, _db_commands=_db_commands,
			cogs=cogs, _db_warns=_db_warns, channels=channels
		)


	@app.route('/update_command_state')
	def update_command_state():
		data = request.args.get('change_dict')[1:-1].replace('"', "").split(",")
		guild_id = request.args.get('guild_id')
		CLUSTER_UTIL = bot.mongo_client[guild_id]["utils"]

		data_dict = {}
		for var in data:
			key = var.split(":")[0][8:]
			val = int(var.split(":")[1])

			data_dict[f"dict.{key}"] = val

		if not data_dict:
			return "ERROR", 404

		CLUSTER_UTIL.update_one({
			"id" : "type_command_activity"
				},{
					"$set" : data_dict
				}
			)

		return "OK", 200

	@app.route('/send_message')
	async def send_message():
		message = request.args.get('message')
		channel_id = request.args.get('channel_id').replace("channel_id_", "")
		channel = await app.discord_client.get_channel(int(channel_id))

		author = await discord_auth.fetch_user()

		embed = discord.Embed(
			description=f"{message}", 
			timestamp=datetime.utcnow(), 
			color=0xffc600
			).set_author(name=f"{author.name} made an announcement!", icon_url=f"{author.avatar_url}"
		)
		await channel.send(embed=embed)
		return "OK", 200
		

	if __name__ == "__main__":
		app.run(debug=True)

        
def setup(bot):
	bot.add_cog(Website(bot))


