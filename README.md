# MathGeneology

An information retrieval system on mathematicans.

Report: https://docs.google.com/document/d/19Ke8gJUIaqr_dQS64QV73YkvOVUSRVgHLV7Q5rjTZ2M/edit?usp=sharing

Search engine performance evaluation: https://docs.google.com/spreadsheets/d/1uD838Tocjd9i4Xyt3WchrziguA3zWE1TUSTAMOh2pW0/edit#gid=0

# Dependencies and Models
This project requires some dependecies and pre-trained models to work properly. 
## Dependencies
To install the dependencies simply run this command:

    pip install -r requirements.txt

## Pre-trained models
This system uses multiple models to work. All of them should be downloaded for the proper execution of the program.
### nltk models
To download the required nltk models simply run this command:

    python3 download_nltk_models.py

### Classification pre-trained models
There are some classification models trained by us that should be downloaded.

first install gdown using `pip install gdown`, then proceed as below considering the model you want to use:
1. To use "distilbert_base_uncased", first download the trained model using `gdown 132xBqgzsccaZg-E5hmsihoTCvJI7jQUD` and unzip the file, then set the variable MODEL_TO_USE to "distilbert_base_uncased" in bert_classify.py and run it. This model achieves an F-score of 0.09 and an accuracy of 40%
2. To use "bert_base_uncased", first download the trained model using `gdown 154XTPXWaHnALT3IX8tX32J7-ht_Cz3vI` and unzip the file, then set the variable MODEL_TO_USE to "bert_base_uncased" in bert_classify.py and run it. This model achieves an F-score of 0.13 and an accuracy of 31%

### Running Elasticsearch

1. First ensure that elastic search is up and running on port 9200
2. Write password for `elastic` user in config.ini file in `/elastic` dir
3. Write ssl_fingerprint of `elastic` server in config.ini. you can find the fingerprint by running `run_elastic.py`. if there's a mismatch between provided and expected ssl_fingerprint, a line in output prints the expected ssl_fingerprint. Replace this token in config.ini and you can connect to elastic search.
4. Run `run_elastic.py` and query answers for `topic_queries.py` queries will show up in terminal. 

### Note that every time you run `run_elastic.py`, index is cleared and then files are reinserted into index. if you don't want this behaviour, comment line 4 in `run_elastic.py` (`index_files()`).


# Running the interface

Our interface is a widget based jupyter notebook. So, to use the interface run jupyter notebook:

    jupyter notebook

Then select `interface.ipynb` to use the interface.

To see all parts of the interface just run all cells.

