from datetime import datetime
from scipy import signal
from elasticsearch import Elasticsearch, helpers
import os, uuid
from time import sleep
import json
# declare a client instance of the Python Elasticsearch library
client = Elasticsearch("localhost:9200")


dict_doc = {}


def addelastic(count,buffitem):


    dict_doc["id"] = count
    dict_doc["timestamp"] = datetime.utcnow()
    dict_doc["TX"]=buffitem[0]
    dict_doc["RX"]=buffitem[1]
    dict_doc["SNR"]=buffitem[2]
    print(dict_doc)
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    try:
        es.index(index='test_human', doc_type='_doc', body=dict_doc)
    except Exception as e:
        print(e)


def query_elastic():
    query_all = {
    'size' : 10000,
    'query': {
    'match_all' : {}
    }
    }

    print("\nSleeping for a few seconds to wait for indexing request to finish.")
    sleep(2)

# pass the query_all dict to search() method
    resp = client.search(
    index = "test_human",
    body = query_all
    )

    print ("search() response:", json.dumps(resp, indent=4))

# print the number of docs in index
    print ("Length of docs returned by search():", len(resp['hits']['hits']))

