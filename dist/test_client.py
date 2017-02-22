#!/usr/bin/python
# coding:  utf-8

from client import Client
from secmongo import SecMongo
from bson.json_util import dumps
from secmongo.index.avltree import AVLTree
from secmongo.index.encryptednode import EncryptedNode
import linecache
import json
import re
import time


def main():
    #
    # Input data
    #
    docs = [
        {
            "name": "John Snow",
            "age":  18,
            "address": "Castle Black, over a table",

        },
        {
            "name": "Eddard Stark",
            "age":  40,
            "address": "King's landing, in a spear",
        },
        {
            "name": "Catherine Stark",
            "age":  34,
            "address": "Hell, 123",
        },
        {
            "name": "Rob Stark",
            "age":  20,
            "address": "Hell, 124",
        },
        {
            "name": "Aria Stark",
            "age":  12,
            "address": "Braavos",
        },
        {
            "name": "Sansa Stark",
            "age":  16,
            "address": "North",
        },
        {
            "name": "Theon Greyjoy",
            "age":  19,
            "address": "No Dick's land",
        },
        {
            "name": "Tywin Lannister",
            "age":  55,
            "address": "King's landing",
        },
        {
            "name": "Cersei Lannister",
            "age":  35,
            "address": "King's landing",
        },
        {
            "name": "Jaime Lannister",
            "age":  35,
            "address": "King's landing",
        },
        {
            "name": "Robert Baratheon",
            "age":  41,
            "address": "King's landing",
        },
        {
            "name": "Joffrey Baratheon",
            "age":  17,
            "address": "King's landing",
        },
        {
            "name": "Lady Melissandre",
            "age":  201,
            "address": "Castle Black, naked",
        }
    ]
    # Setup client
    client = Client(Client.keygen())
    client.set_attr("name", "static")
    client.set_attr("address", "static")
    client.set_attr("age", "index")

    # Setup the MongoDB driver
    s = SecMongo(add_cipher_param=pow(client.ciphers["h_add"].keys["pub"]["n"],
                                      2),
                 url='mongodb://localhost:27017')
    s.open_database("test_sec")
    s.set_collection("gameofthrones2")
    s.drop_collection()

    s.load_scripts()

    print("Starting now.")
    start = time.time()
    for i, doc in enumerate(docs):
        enc_doc = client.encrypt(doc)
        inserted_doc = s.insert(enc_doc)
        node = EncryptedNode(client.ciphers["index"].encrypt(doc["age"]),
                             inserted_doc)
        s.insert_index(node)

    print("Insert time: ", time.time() - start)
    result = [client.decrypt(x)["name"] for x in s.find()]
    print("")

    print("People of 35 years old:")
    for doc in s.find(index=client.get_ctL(35)):
        print(client.decrypt(doc))

if __name__ == '__main__':
    main()
