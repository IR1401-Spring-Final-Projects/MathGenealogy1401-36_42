import pandas as pd
import os

import seaborn as sns
from matplotlib import pyplot as plt


path_to_file = os.path.dirname(os.path.abspath(__file__))
path_split = '/' if '/' in path_to_file else '\\'

cluster_df = pd.read_csv(path_to_file + path_split + 'communities.csv')
topic_df = pd.read_csv(path_to_file + path_split +'topic.csv', index_col=0)


def get_leiden_cluster(id: int):
    global cluster_df
    result = cluster_df[cluster_df['id'] == id]
    _, ax = plt.subplots()
    sns.scatterplot(
            x = "tsne-one", y = "tsne-two",
            hue='leiden_label',
            palette=sns.color_palette("hls", cluster_df['leiden_label'].nunique()),
            data=cluster_df,
            legend='auto',
            alpha=0.3,
            ax=ax
    )
    ax.plot(result['tsne-one'], result['tsne-two'], 'o', color='black')
    plt.show()
    return result['leiden_label'].values[0], ax



def get_infomap_cluster(id: int):
    global cluster_df
    result = cluster_df[cluster_df['id'] == id]
    _, ax = plt.subplots()
    sns.scatterplot(
            x = "tsne-one", y = "tsne-two",
            hue='infomap_label',
            palette=sns.color_palette("hls", cluster_df['infomap_label'].nunique()),
            data=cluster_df,
            legend='auto',
            alpha=0.3,
            ax=ax
    )
    ax.plot(result['tsne-one'], result['tsne-two'], 'X', color='black')
    plt.show()
    return result['infomap_label'].values[0], ax


def get_topic_cluster(id: int):
    global topic_df
    try:
        result = topic_df.loc[id]
        return result.values.tolist()
    except:
        return [0] * 16
