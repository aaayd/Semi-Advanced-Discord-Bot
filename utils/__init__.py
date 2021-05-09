
from utils.constants import CLUSTER_BLACKLIST_WORDS, CLUSTER_SERVER_ROLES

def _create_blank_mongo_arr(cluster, _id):
        _exists = cluster.find_one({
            "id": _id
        })

        if _exists is None:
            cluster.insert_one({
                "id": _id, 
                "array": []
            })

_create_blank_mongo_arr(CLUSTER_BLACKLIST_WORDS, "type_blacklist")
_create_blank_mongo_arr(CLUSTER_SERVER_ROLES, "type_on_join_roles")