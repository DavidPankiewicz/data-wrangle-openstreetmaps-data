import json

def insert_data(data, db):
    db.sanfrancisco.insert(data)
    return

def main(json_file):
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.maps
    
    # Delete any existing data in the collection. 
    db.sanfrancisco.remove()
    with open(json_file) as f:
        for line in f:
            data = json.loads(line)
            insert_data(data, db)
        # Confirm that it worked
        print "Here's a newly added document"
        print db.sanfrancisco.find_one()
    return

file_name = "large-sf-square.osm.json"

main(file_name)

