import networkx as nx
import pandas as pd


class ActorGraphMetrics:
    def __init__(self, df):
        self.df = df
        self.graph = self._create_graph()
        self.actor_attributes = self._calculate_actor_attributes()

    def _create_graph(self):
        graph = nx.from_pandas_edgelist(self.df, 'source', 'target', 'weight')
        return graph

    def _calculate_actor_attributes(self):
        actor_attributes = pd.DataFrame(index=self.graph.nodes)

        actor_attributes['DegreeCentrality'] = pd.Series(nx.degree_centrality(self.graph))
        actor_attributes['BetweennessCentrality'] = pd.Series(nx.betweenness_centrality(self.graph))
        actor_attributes['EigenvectorCentrality'] = pd.Series(nx.eigenvector_centrality(self.graph))
        actor_attributes['ClusteringCoefficient'] = pd.Series(nx.clustering(self.graph))
        return round(actor_attributes, 3)

    def get_actor_attributes(self):
        return self.actor_attributes


def create_actor_graph_metrics_dict(df):
    df = df.reset_index()
    actor_dict = {}
    for _, row in df.iterrows():
        actor = row[0].replace(" ","_")
        attributes = {col: val for col, val in row[1:].iteritems()}
        actor_dict[actor] = attributes
    return actor_dict
