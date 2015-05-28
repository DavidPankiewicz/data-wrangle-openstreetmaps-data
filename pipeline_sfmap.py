"""

Run aggregate queires against a Mongo Database

Database: maps
Collection: sanfrancisco
"""

import pprint

def make_pipeline():
    
    # insert pipelin in between []
    pipeline = [    
    
    ]
    return pipeline

def aggregate(db, pipeline):
    result = db.sanfrancisco.aggregate(pipeline)
    return result        

def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.maps
    return db

def main():
    db = get_db()
       
    pipeline= make_pipeline()
    result = aggregate(db, pipeline)

    for each_result in result:
        pprint.pprint(each_result)

    return

main()