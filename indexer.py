# load csv data into elasticsearch
import os, argparse
from csv import DictReader
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from config import esconfig
from datetime import datetime, timedelta

DOC_TYPE = '_doc'
conn_cols = ['ts','uid','id.orig_h','id.orig_p',
'id.resp_h','id.resp_p','proto','service',
'duration','orig_bytes','resp_bytes','conn_state',
'local_orig','missed_bytes','history','orig_pkts',
'orig_ip_bytes','resp_pkts','resp_ip_bytes','tunnel_parents','threat','sample']

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='name of delimited file')
    parser.add_argument('-i', '--index', help='elasticsearch index name(default=dir_name)')
    parser.add_argument('-s', '--shift', type=int, help='shift time by (in days)')
    args = parser.parse_args()
    return args

def harvest(file_name):
    with open(file_name, 'r') as f:
        dictf = DictReader(f, fieldnames=conn_cols,delimiter='\t')
        for doc in dictf:
            yield doc

def shift_time(doc):
    ts = datetime.fromtimestamp(int(doc.pop('ts').split('.')[0]))
    doc['@timestamp'] = ts + timedelta(days=args.shift)
    return(doc)

def make_actions(docs):
    for doc in docs:
        if args.shift != None:
            doc = shift_time(doc)
        action =  { "_index": index_name, "_type": DOC_TYPE }
        action["_source"] = doc
        yield action

def get_credentials():
    user = input('Username: ')
    if user:
        pwd = getpass.getpass()
        return (user, pwd)
    else:
        return(None,None)

def get_clients(user,pwd):
    host = esconfig[0]['host']
    port = esconfig[0]['port']
    if user:
        es = Elasticsearch([host], http_auth=(user,pwd), port=port)
    else:
        es = Elasticsearch(esconfig)
    return es

args = parse_args()
if args.index == None:
    index_name = args.dir_name
else:
    index_name = args.index
user, pwd = get_credentials()
es = get_clients(user,pwd)
actions = make_actions(harvest(args.file))
b = bulk(es, actions)
