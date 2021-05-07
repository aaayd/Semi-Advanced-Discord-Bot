from main import CLUSTER

# Databases
CLUSTER_EXPERIENCE= CLUSTER["discord"]["levelling"]
CLUSTER_RATELIMIT = CLUSTER["discord"]["xp_rate_limit"]
CLUSTER_AFK = CLUSTER["discord"]["afk"]
CLUSTER_GAY = CLUSTER["discord_fun"]["gay"]
CLUSTER_DICK = CLUSTER["discord_fun"]["dick"]
CLUSTER_PUSSY = CLUSTER["discord_fun"]["pussy"]
CLUSTER_SHIP = CLUSTER["discord_fun"]["ship"]

# Variables
CONFESSION_BOOL = CLUSTER["discord"]["utils"].find_one({"id": "type_confession"})["confession"]
