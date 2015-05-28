
"""
SF Map data is stored a 
Database named "maps"
and a collection named "sanfrancisco"
"""


def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    # Connect to the maps data base
    db = client.maps
    return db

def main():
    db = get_db()
    query = {"addr.street": "Polk Street"}
    nodes = db.sanfrancisco.find(query)
    import pprint
    for i in range(nodes.count()):
       pprint.pprint(nodes[i])
    

main()
