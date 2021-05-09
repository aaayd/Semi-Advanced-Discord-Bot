
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

