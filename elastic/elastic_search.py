from codecs import ignore_errors
from datetime import datetime
import math
from re import I
from elasticsearch import Elasticsearch
import configparser
import os
from topic_queries import subject_queries


CONFIG_FILE_PATH = './elastic/config.ini'
RAW_BIOGRAPHIES_PATH = "raw_biographies/"
INDEX_NAME = 'mathematicians'


class Mathematician:

    def __init__(self, name, biography):
        self.name = name
        self.biography = biography


def read_config_file():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    return config


def connect_to_elastic_search(config):
    es = Elasticsearch(
            'https://localhost:9200',
            basic_auth=(config['ELASTIC']['user'], config['ELASTIC']['password']),
            ssl_assert_fingerprint=(config['ELASTIC'] ['ssl_fingerprint'])
    )
    return es


def insert_test_doc(es):
    doc = {
        'author': 'author_name',
        'text': 'Interensting content...',
        'timestamp': datetime.now(),
    }
    resp = es.index(
            index="test-index",
            id=1, document=doc)
    print(resp['result'])


def get_file_names():
    return os.listdir(RAW_BIOGRAPHIES_PATH)


def get_biography(file_path):
    f = open(file_path, mode="r")
    text = f.read()
    f.close()
    return text


def get_file_path(file_name):
    return RAW_BIOGRAPHIES_PATH + file_name


def get_all_mathematicians():
    file_names = sorted(get_file_names())
    file_paths = list(map(get_file_path, file_names))
    biographies = zip(file_names, map(get_biography, file_paths))

    mathemticians = []
    for name, biography in biographies:
        mathematician = Mathematician(name, biography)
        mathemticians.append(mathematician)
    
    return mathemticians

def insert_mathematician(es, mathematician):
    doc = {
        'name': mathematician.name,
        'biography': mathematician.biography
    }

    resp = es.index(
        index=INDEX_NAME,
        document=doc
    )


def insert_all(es, mathematicians):
    for mathematician in mathematicians:
        insert_mathematician(es, mathematician)
    print("inserted all to index")


def clean_index(es: Elasticsearch):
    es.options(ignore_status=[400,404]).indices.delete(index=INDEX_NAME)


def create_index(es: Elasticsearch):
    es.indices.create(
        index=INDEX_NAME
    )

def print_result_for_query(es: Elasticsearch, query):
    resp = es.search(
        index=INDEX_NAME,
        query= {
            "match": {
                "biography": query
            }
        }
    )
    print("-" * 20)
    print(f"results for query {query}\n\n")

    results = resp['hits']['hits']
    for result in results:
        name = result['_source']['name']
        score = result['_score']
        print(name, score)
    print("-" * 20)


def find_results_for_queries(es: Elasticsearch):
    for query in subject_queries:
        print_result_for_query(es, query)

def get_connection():
    config = read_config_file()
    es = connect_to_elastic_search(config)
    return es

def index_files():
    mathematicians = get_all_mathematicians()
    es = get_connection()
    clean_index(es)
    create_index(es)
    insert_all(es, mathematicians)

def run():
    es = get_connection()
    find_results_for_queries(es)