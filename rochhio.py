import re
import string
import glob

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from topic_queries import subject_queries
# Config
DATA_DIR = 'stemmed_biographies'
TOP_RANKS = 10
# TF-IDF
max_df = 0.95        # Ignore words with high df. (Similar effect to stopword filtering)
min_df = 5           # Ignore words with low df.
smooth_idf = True    # Smooth idf weights by adding 1 to df.
sublinear_tf = True  # Replace tf with 1 + log(tf).

# Rocchio (Below is a param set called Ide Dec-Hi)
alpha = 1
beta = 0.75
gamma = 0.15
rel_count = 5   # Use top-5 relevant documents to update query vector.
nrel_count = 1  # Use only the most non-relevant document to update query vector.
iters = 5

filenames = [filename for filename in glob.glob(f'{DATA_DIR}/*')]
files = []
for filename in filenames:
    file = open(filename, 'r')
    files.append(file.read())
    file.close()

vectorizer = TfidfVectorizer(strip_accents='unicode', stop_words='english')
doc_tfidfs = vectorizer.fit_transform(files).toarray()
queries = subject_queries
query_vecs = vectorizer.transform(queries).toarray()

cos_sim = cosine_similarity(query_vecs, doc_tfidfs)
rankings = np.flip(cos_sim.argsort(), axis=1)


for _ in range(iters):
    # Update query vectors with Rocchio algorithm
    rel_vecs = doc_tfidfs[rankings[:, :rel_count]].mean(axis=1)
    nrel_vecs = doc_tfidfs[rankings[:, -nrel_count:]].mean(axis=1)
    query_vecs = alpha * query_vecs + beta * rel_vecs - gamma * nrel_vecs
    # Rerank documents based on cosine similarity
    cos_sim = cosine_similarity(query_vecs, doc_tfidfs)
    rankings = np.flip(cos_sim.argsort(axis=1), axis=1)

def print_docs(docs):
    for doc in docs:
        if doc == 'None' or doc is None:
            continue
        print(doc.replace('_', ' '))

if __name__ == '__main__':
    for query_name, ranking in zip(queries, rankings):
        ranked_docs = [filenames[idx].split('/')[1] for idx in ranking]
        ranked_docs = ranked_docs[:TOP_RANKS]

        print(f'query name: {query_name}, docs:\n{print_docs(ranked_docs)}')
        print('*'*20)


def get_query(query_name):
    query_vec = vectorizer.transform([query_name]).toarray()
    cos_si = cosine_similarity(query_vec, doc_tfidfs)
    rankin = np.flip(cos_si.argsort(), axis=1)[0]
    ranked_doc = [filenames[idx].split('/')[1] for idx in rankin]
    ranked_doc = ranked_doc[:TOP_RANKS]
    names = []
    for doc in ranked_doc:
        if doc == 'None' or doc is None:
            continue
        names.append(doc.replace('_', ' '))
    return names