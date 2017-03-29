import ipywidgets as widgets
import json
from traitlets import Unicode
from clustergrammer import Network

@widgets.register('hello.Hello')
class clustergrammer_widget(widgets.DOMWidget, Network):
    """
    Clustergrammer-Widget generates an interactive heatmap in the Jupyter
    notebook. Clustergrammer-Widget inherits from Clustergrammer.py which can
    be used to load data, filter, normalize, and cluster.
    """
    _view_name = Unicode('hello_view').tag(sync=True)
    _model_name = Unicode('hello_model').tag(sync=True)
    _view_module = Unicode('clustergrammer_widget').tag(sync=True)
    _model_module = Unicode('clustergrammer_widget').tag(sync=True)

    string_mat = Unicode('').tag(sync=True)

    viz_title = Unicode('updating python by restarting kernel').tag(sync=True)

    network = Unicode('').tag(sync=True)

    def widget_df(self):
      print('exporting current dataframe')

    def cluster(self):
      '''
      Cluster the matrix and assign the visualization JSON to network for front
      end rendering.
      '''
      self.make_clust()
      self.network = self.widget()