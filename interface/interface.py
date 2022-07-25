import ipywidgets as widgets
from IPython.display import display, Markdown, clear_output
from elastic import elastic_search
from clustering import cluster
import TFIDF
import bert
import bert_classifier
import boolean
import fast_text
import make_matrix

BIOGRAPHY_DIR = 'text_biographies'
# elastic_search.index_files()
try:
    es = elastic_search.get_connection()
except :
    pass

with open('topic.html', 'r') as f:
    topic_html = f.read()

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
    with cluster_result:
        clear_output()
        query = cluster_query.value
        laiden_result = cluster.get_leiden_cluster(query)
        infomap_result = cluster.get_infomap_cluster(query)
        topic_result = cluster.get_topic_cluster(query)
        text = ' # Laiden Result \n' + str(laiden_result[0]) + "\n # Infomap Result \n" + \
               str(infomap_result[0]) +"\n # Topic Result \n"+ str(topic_result)
        display(Markdown(text))


def on_get_query_expansion(_):
    #TODO
    pass


def on_get_elastic(_):
    with elastic_result:
        clear_output()
        query = elastic_query.value
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


def on_get_link(_):
    with link_result:
        clear_output()
        query = link_query.value
        make_matrix.create_mat_with_sensitivity(int(query))

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
topic_cluster = widgets.HTML('<a href=topic.html target="_blank"> Show Topic Plot </a>')
cluster_query = widgets.IntText(description="Id")
cluster_button = widgets.Button(description="Find Label")
cluster_button.on_click(on_get_clustering)
cluster_result = widgets.Output()

cluster_page = widgets.VBox([
    topic_cluster,
    widgets.HBox([
        cluster_query, cluster_button
    ]),
    cluster_result
])

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

# page_rank
link_query = widgets.Text(description="Sensitivity")
link_button = widgets.Button(description="Create matrix")
link_result = widgets.Output()
link_button.on_click(on_get_link)

link_page = widgets.VBox([
    widgets.HBox([
        link_query, link_button
    ]),
    link_result
])



