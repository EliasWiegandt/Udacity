#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from pymongo import MongoClient
# import pprint
# import os
#
#
# client = MongoClient('localhost:27017')
# db = client[database_name]
# col = db[collection_name]
# print("Number of documents in collection: ", col.count())
# print("Number of nodes in collection: ",
#   col.find({"type": "node"}).count())
# print("Number of ways in collection: ",
#   col.find({"type": "way"}).count())
# print("Number of unique users in collection: ",
#   len(col.distinct("user")))
# results=col.aggregate([
#     {"$group": {"_id": "$user", "count": {"$sum": 1}}},
#     {"$sort": {"count": -1}}, {"$limit": 5}])
# print(" ")
# print("Top 5 contributing users:")
# print(" ")
# for doc in results:
#     pprint.pprint(doc)
# print(" ")


mapping_danish_letters = {
            u'\xf8': "oe",
            u'\xe5': "aa",
            u'\xe3': "ae"}

def clean_danish_letters(text):
    '''
    Behavior:   takes a text and replaces danish æ, ø and å
                with their ASCII equivalents ae, oe and aa.
    Input:      text (string)
    Output:     text_clean (string)
    '''
    text_clean = text
    for letter in text:
        if mapping_danish_letters.get(letter, False):
            text_clean = text_clean.replace(letter,
                                            mapping_danish_letters[letter])
    return text_clean
str_raw=u'N\xf8rrebro'
str_clean=clean_danish_letters(str_raw)
print(str_clean)
