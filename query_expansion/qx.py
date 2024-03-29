import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re


def download_nltk_packages():
    nltk.download('wordnet')
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')


def tokenizer(sentence):
    return word_tokenize(sentence)

def pos_tagger(tokens):
    return nltk.pos_tag(tokens)

def stopword_treatment(tokens):
    stopword = stopwords.words('english')
    result = []
    for token in tokens:
        if token[0].lower() not in stopword:
            result.append(tuple([token[0].lower(), token[1]]))
    return result
pos_tag_map = {
    'NN': [ wn.NOUN ],
    'JJ': [ wn.ADJ, wn.ADJ_SAT ],
    'RB': [ wn.ADV ],
    'VB': [ wn.VERB ]
}

def pos_tag_converter(nltk_pos_tag):
    root_tag = nltk_pos_tag[0:2]
    try:
        pos_tag_map[root_tag]
        return pos_tag_map[root_tag]
    except KeyError:
        return ''

def get_synsets(tokens):
    synsets = []
    for token in tokens:
        wn_pos_tag = pos_tag_converter(token[1])
        if wn_pos_tag == '':
            continue
        else:
            synsets.append(wn.synsets(token[0], wn_pos_tag))
    return synsets

def get_tokens_from_synsets(synsets):
    tokens = {}
    for synset in synsets:
        for s in synset:
            if s.name() in tokens:
                tokens[s.name().split('.')[0]] += 1
            else:
                tokens[s.name().split('.')[0]] = 1
    return tokens

def get_hypernyms(synsets):
    hypernyms = []
    for synset in synsets:
        for s in synset:
            hypernyms.append(s.hypernyms())

    return hypernyms

def get_tokens_from_hypernyms(synsets):
    tokens = {}
    for synset in synsets:
        for s in synsets:
            for ss in s:
                if ss.name().split('.')[0] in tokens:
                    tokens[(ss.name().split('.')[0])] += 1
                else:
                    tokens[(ss.name().split('.')[0])] = 1
    return tokens

def underscore_replacer(tokens):
    new_tokens = {}
    for key in tokens.keys():
        mod_key = re.sub(r'_', ' ', key)
        new_tokens[mod_key] = tokens[key]
    return new_tokens

def generate_tokens(sentence):
    tokens = tokenizer(sentence)
    tokens = pos_tagger(tokens)
    tokens = stopword_treatment(tokens)
    synsets = get_synsets(tokens)
    synonyms = get_tokens_from_synsets(synsets)
    synonyms = underscore_replacer(synonyms)
    hypernyms = get_hypernyms(synsets)
    hypernyms = get_tokens_from_hypernyms(hypernyms)
    hypernyms = underscore_replacer(hypernyms)
    tokens = {**synonyms, **hypernyms}
    return tokens

# download_nltk_packages()
queries = [
    'deviation',
    'statistics',
    'calculus',
    'hypothetic',
    'negative',
    'summation',
    'arithmetic',
    'curve',
    'interpolation',
    'manifold',
    'prime number',
    'innovative',
    'strong',
]

if __name__ == '__main__':
    for q in queries:
        res = generate_tokens(q)
        print(res)