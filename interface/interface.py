import ipywidgets as widgets
from ipywidgets import interact, interact_manual
from IPython.display import display, Markdown, clear_output
import pandas as pd
import bert_classifier, boolean, TFIDF, bert, fast_text


#Functions
def on_get_classifier(_):
    with classifier_result:
        clear_output()
        query = classifier_query.value
        print(bert_classifier.predict(query))
        # display(bert_classifier.predict(query))


def on_get_clustering(_):
    #TODO
    pass


def on_get_hw3(_):
    with hw3_result:
        clear_output()
        query = hw3_query.value
        type = hw3_type.value
        if type == 'Boolean':
            print(boolean.query_result(query))
        elif type == 'TFIDF':
            print(TFIDF.query_result(query))
        elif type == 'Bert':
            print(bert.query_result(query))
        elif type == 'Fast_Text':
            print(fast_text.get_query(query))
    pass


#Widgets

#classifier
classifier_query = widgets.Text(description="Query")
classifier_button = widgets.Button(description="Classify")
classifier_button.on_click(on_get_classifier)
classifier_result = widgets.Output()

classifier_page = widgets.VBox([
    widgets.HBox([
        classifier_query, classifier_button
    ]),
    classifier_result
])

#clustering


#query expansion


#elastic

# hw3
hw3_query = widgets.Text(description="Query")
hw3_type = widgets.Dropdown(description="Method",
                            options=['Boolean', 'TFIDF', 'Bert', 'Fast_Text'], value='Boolean')
hw3_button = widgets.Button(description="Search")
hw3_button.on_click(on_get_hw3)
hw3_result = widgets.Output()

hw3_page = widgets.VBox([
    widgets.HBox([
        hw3_query, hw3_type, hw3_button
    ]),
    hw3_result
])

#



