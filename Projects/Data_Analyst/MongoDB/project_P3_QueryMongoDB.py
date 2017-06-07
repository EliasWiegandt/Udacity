from pymongo import MongoClient
import pprint
import os

database_name = "OpenStreetMap"
collection_name = "copenhagen"
OSMfile = "copenhagen_denmark_custom.osm"
JSONfile = "copenhagen_denmark_custom.osm.json"


def find_filesize(name, path=""):
    '''
    Behavior:   Finds size  of file in Mega Byte (MB)
    Input:      name (string, includes fileextension),
                path (optional, if file is in another directory)
    Output:     size of file in MB
    '''
    if path == "":
        path = os.path.dirname(os.path.realpath(__file__))
    file_path = path + '\\' + name
    byte = os.path.getsize(file_path)
    megabyte = byte / 1024 / 1024
    return round(megabyte, 1)


def get_db_col():
    '''
    Behavior:   Returns an open connection to a database and a collection.
    Input:      None
    Output:     db (refers to database), col (refers to collection)
    '''
    client = MongoClient('localhost:27017')
    db = client[database_name]
    col = db[collection_name]
    return db, col


def find_data(col, query):
    '''
    Behavior:   sends "find" query to database
    Input:      col (refers to collection),
                query (dictionary which specifies query)
    Output:     dictionaries with data result from running query
    '''
    return col.find(query)


def aggr_data(col, query):
    '''
    Behavior:   sends "aggregate" query to database
    Input:      col (refers to collection),
                query (dictionary which specifies query)
    Output:     dictionaries with data result from running query
    '''
    return col.aggregate(query)


def print_results(results):
    '''
    Behavior:   print results from MongoDB query
    Input:      results (dictionaries with data result from running query),
    Output:     None
    '''
    print(" ")
    for doc in results:
        pprint.pprint(doc)
    print(" ")


if __name__ == "__main__":
    '''
    db, col = get_db_col()
    q_all = {}
    print_results(find_data(col, q_all)[0:1])
    print("Number of documents in collection: ", col.count())
    print("Number of nodes in collection: ",
          col.find({"type": "node"}).count())
    print("Number of ways in collection: ",
          col.find({"type": "way"}).count())
    print("Number of unique users in collection: ",
          len(col.distinct("user")))
    q_users = [
            {"$group": {"_id": "$user", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}, {"$limit": 5}]
    print(" ")
    print("Top 5 contributing users:")
    print_results(aggr_data(col, q_users))
    print("Size of OSM file: ", find_filesize(OSMfile))
    print("Size of JSON file: ", find_filesize(JSONfile))
    '''
    client = MongoClient('localhost:27017')
    db = client[database_name]
    col = db[collection_name]
    print("Number of documents in collection: ", col.count())
    print("Number of nodes in collection: ",
      col.find({"type": "node"}).count())
    print("Number of ways in collection: ",
      col.find({"type": "way"}).count())
    print("Number of unique users in collection: ",
      len(col.distinct("user")))
    results=col.aggregate([
        {"$group": {"_id": "$user", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}, {"$limit": 5}])
    print(" ")
    print("Top 5 contributing users:")
    print(" ")
    for doc in results:
        pprint.pprint(doc)
    print(" ")



'''
