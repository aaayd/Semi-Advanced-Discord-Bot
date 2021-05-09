
from main import result, client
from utils.constants import CLUSTER_BLACKLIST_WORDS, CLUSTER_GIFS, CLUSTER_SERVER_ROLES, CLUSTER_CONFESSION, DEF_SNIPE_GIFS

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

_init_mongo_arr(CLUSTER_BLACKLIST_WORDS, "type_blacklist", ["nigger"])
_init_mongo_arr(CLUSTER_SERVER_ROLES, "type_on_join_roles")
_init_mongo_arr(CLUSTER_GIFS, "type_snipe_gifs", DEF_SNIPE_GIFS)
_init_mongo_bool(CLUSTER_CONFESSION, "type_confession")