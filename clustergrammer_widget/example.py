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

    def cluster(self, dist_type='cosine', run_clustering=True,
                 dendro=True, views=['N_row_sum', 'N_row_var'],
                 linkage_type='average', sim_mat=False, filter_sim=0.1,
                 calc_cat_pval=False, run_enrichr=None):
      '''
      Cluster the matrix and assign the visualization JSON to network for front
      end rendering.
      '''
      self.make_clust(dist_type=dist_type, run_clustering=run_clustering,
                                   dendro=dendro,
                                   views=views,
                                   linkage_type=linkage_type,
                                   sim_mat=sim_mat,
                                   filter_sim=filter_sim,
                                   calc_cat_pval=calc_cat_pval,
                                   run_enrichr=run_enrichr)

      # pass visualization JSON to widget
      self.network = self.widget()