#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
#from pymongo import MongoClient

OSMfile = "copenhagen_denmark_custom_sample.osm"
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
address_headers = ['housenumber', 'postcode', 'street', 'website']
other_headers = ['amenity', 'phone', 'cuisine', 'name']
user_headers = ['id', 'version', 'changeset',
                'timestamp', 'user', 'uid',
                'visible', 'type']
pos_header = ['lat', 'lon']
database_name = "OpenStreetMap"
collection_name = "copenhagen"

mapping_danish_letters = {
            u'\xf8': "oe",
            u'\xe5': "aa",
            u'\xe3': "ae"}


def insert_into_database(data):
    '''
    Behavior:   Takes data and insert into collection specified
                in global variables.
    Input:      data (list of dictionaries)
    Output:     None
    '''
    db, col = get_db_col()
    col.insert(data)
    return None


def drop_collection():
    '''
    Behavior:   Removes collection (specified in global variables)
                from database.
    Input:      None
    Output:     None
    '''
    db, col = get_db_col()
    col.drop()
    return None


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


def shape_element(element):
    '''
    Behavior:   takes an xml.etree element and searches it for data,
                which is then inserted into dictionaries.
    Input:      Element (element returned when xml file is read by xml.etree)
    Output:     Node (dictionary with data from the input)
    '''
    if element.tag == "node" or element.tag == "way":
        node = {}
        node['type'] = element.tag
        address_dict, other_dict = k_tag_dict(element)
        user_dict = user_entry(element)
        nd_refs = nd_ref_list(element)
        if user_dict is not None:
            if user_dict:
                for key_user in user_dict.keys():
                    node[key_user] = clean_text(user_dict[key_user])
        if other_dict is not None:
            if other_dict:
                for key_other in other_dict.keys():
                    node[key_other] = clean_text(other_dict[key_other])
        if len(address_dict) > 0:
            node["address"] = address_dict
        if len(nd_refs) > 0:
            node['nd_ref'] = nd_refs
        return node
    else:
        return None


def process_map(file_in, pretty=False):
    '''
    Important:  Taken from Udacity course material.
    Behavior:   Extracts information from OSM file.
    Input:      filen_in (string with name of OSM file),
                pretty (boolean for how JSON are to be printed)
    Output:     data (list of dictionaries)
    '''
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


def k_tag_dict(element):
    '''
    Behavior:   Takes element and returns dictionary of data
                tagged with the 'k' tag.
    Input:      element (element returned when xml file is read by xml.etree)
    Output:     address (dictionary of data), other (dictionary of data)
    '''
    address = {}
    other = {}
    for inner in element.findall('tag'):
        if ('k' in inner.attrib) and ('v' in inner.attrib):
            tag_k = inner.attrib['k']
            tag_k_split = tag_k.split(":")
            if len(tag_k_split) == 2:
                for split_string in tag_k_split:
                    if split_string in address_headers:
                        address[split_string] = clean_text(inner.attrib['v'])
                        if (split_string == 'postcode' and
                                len(inner.attrib['v']) != 4):
                            print(inner.attrib['v'])
            else:
                if tag_k in other_headers:
                    other[tag_k] = inner.attrib['v']
    return address, other


def nd_ref_list(element):
    '''
    Behavior:   Returns list of nd_refs related to
                the data point, if it is a way.
    Input:      element (element returned when xml file is read by xml.etree)
    Output:     nd_ref (list of nd_refs related to the data)
    '''
    nd_ref = []
    if element.tag == 'way':
        for inner in element.findall('nd'):
            nd_ref.append(inner.attrib['ref'])
    return nd_ref


def user_entry(element):
    '''
    Behavior:   Takes element and returns dictionary of data related
                to the user or the position of the entry in the data.
    Input:      element (element returned when xml file is read by xml.etree)
    Output:     user (dictionary of data)
    '''
    user = {}
    pos_dict = {}
    pos = []
    for attrib in element.attrib:
        if attrib in user_headers:
            user[attrib] = element.attrib[attrib]
        if attrib in pos_header:
            pos_dict[attrib] = element.attrib[attrib]
    if len(pos_dict) == len(pos_header):
        for header in pos_header:
            pos.append(pos_dict[header])
        user['pos'] = pos
    return user


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


def clean_RE_letters(text):
    '''
    Behavior:   takes a text and checks it for characters
                that might be problematic.
    Input:      text (string)
    Output:     text_clean (string)
    '''
    text_clean = text
    if problemchars.match(text_clean):
        text_clean = clean_phone_number(text_clean)
    return text_clean


def clean_phone_number(text):
    '''
    Behavior:   takes a text, removes all spaces. If first
                letter is '+' it is assumed to be a phone number,
                '+' is replaced with '00'.
    Input:      text (string)
    Output:     text_clean (string)
    '''
    text_process = text
    text_start = ""
    while text_process != text_start:
        text_start = text_process
        text_process = text_process.replace(" ", "")
    text_clean = text_process
    if text_clean[0] == '+':
        text_clean = text_clean.replace('+', '00')
        text_clean = text_clean[0:4] + ' ' + text_clean[4:]
    return text_clean


def clean_text(text):
    '''
    Behavior:   takes input, checks if it is text and process it if it is.
    Input:      text (can be any kind of object)
    Output:     text_clean (string), text (if input is not a string,
                it is simply returned unchanged)
    '''
    if isinstance(text, str):
        text_clean = text.strip()
        text_clean = clean_danish_letters(text_clean)
        text_clean = clean_RE_letters(text_clean)
        return text_clean
    else:
        return text


if __name__ == "__main__":
    #drop_collection()
    data = process_map(OSMfile, True)
    #insert_into_database(data)
    print(data[0:3])
