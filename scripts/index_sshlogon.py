import argparse, json, csv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from datetime import datetime
from time import sleep
from random import random

def index_csv(args):
    with open(args.csv_file, 'r') as f:
        dictf = csv.DictReader(f)
        for doc in dictf:
            sleep(random()*2)
            doc['@timestamp'] = datetime.now()
            doc['message'] = doc['message'].replace('_ts_', str(datetime.now()))
            resp = es.index(index=args.index, doc_type=args.type, body=doc)
            print(resp['result'])

parser = argparse.ArgumentParser()
parser.add_argument("csv_file")
parser.add_argument("index")
parser.add_argument("type", default='_doc')
args = parser.parse_args()
es = Elasticsearch()
index_csv(args)
