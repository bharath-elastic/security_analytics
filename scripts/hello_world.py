from elasticsearch import Elasticsearch
from datetime import datetime
from random import choice
from time import sleep
from pytz import timezone

# make 10,000 messages
def index_messages():
    for i in range(10000):
        message = choice(greet_str)
        #ts = tz.localize(datetime.now())
        ts = datetime.now()
        doc = { 'ts': ts, 'message': message }
        sleep(1)
        resp = es.index(index=cfg['index'], doc_type=cfg['type'], id=i, body=doc)
        print(resp['result'])

if __name__ == '__main__':
    cfg = {'index': 'hello', 'type': '_doc', 'tz': 'US/Eastern'}
    greet_str = 'hello world!,' * 9 + 'hello world!'
    greet_str = greet_str.split(',', maxsplit=9)
    greet_str.append('intruder')
    tz = timezone(cfg['tz'])
    es = Elasticsearch()
    index_messages()

