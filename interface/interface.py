import ipywidgets as widgets
from IPython.display import display, Markdown, clear_output
from elastic import elastic_search
import TFIDF
import bert
import bert_classifier
import boolean
import fast_text

BIOGRAPHY_DIR = 'text_biographies'
# elastic_search.index_files()
es = elastic_search.get_connection()

def get_biography_from_name(name: str):
    name = name.replace(' ', '_')
    return f'{BIOGRAPHY_DIR}/{name}.txt'


def create_html_from_names(name_list):
    html = ""
    for name in name_list:
        html = html + '<a href='+get_biography_from_name(name)+' target="_blank"> ' + name + '</a> <br>'
    return html


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


def on_get_query_expansion(_):
    #TODO
    pass

def on_get_elastic(_):
    with elastic_result:
        clear_output()
        query = elastic_query.value
        print(elastic_search.get_result_for_query(es, query))
        display(Markdown(create_html_from_names(elastic_search.get_result_for_query(es, query))))

def on_get_hw3(_):
    with hw3_result:
        clear_output()
        query = hw3_query.value
        type = hw3_type.value
        if type == 'Boolean':
            display(Markdown(create_html_from_names(boolean.query_result(query))))
        elif type == 'TFIDF':
            display(Markdown(create_html_from_names(TFIDF.query_result(query))))
        elif type == 'Bert':
            display(Markdown(create_html_from_names(bert.query_result(query))))
        elif type == 'Fast_Text':
            display(Markdown(create_html_from_names(fast_text.get_query(query))))
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
elastic_query = widgets.Text(description="Query")
elastic_button = widgets.Button(description="Search")
elastic_button.on_click(on_get_elastic)
elastic_result = widgets.Output()

elastic_page = widgets.VBox([
    widgets.HBox([
        elastic_query, elastic_button
    ]),
    elastic_result
])

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



