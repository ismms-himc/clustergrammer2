
import numpy as np
import pandas as pd
from copy import deepcopy

from . import initialize_net
from . import load_data
from . import export_data
from . import load_vect_post
from . import make_clust_fun
from . import normalize_fun
from . import data_formats
from . import enrichr_functions as enr_fun
from . import iframe_web_app
from . import run_filter
from . import downsample_fun
from . import categories

class Network(object):
  '''
  version 1.13.5

  Clustergrammer.py takes a matrix as input (either from a file of a Pandas DataFrame), normalizes/filters, hierarchically clusters, and produces the :ref:`visualization_json` for :ref:`clustergrammer_js`.

  Networks have two states:

    1. the data state, where they are stored as a matrix and nodes
    2. the viz state where they are stored as viz.links, viz.row_nodes, and viz.col_nodes.

  The goal is to start in a data-state and produce a viz-state of
  the network that will be used as input to clustergram.js.
  '''

  def __init__(self, widget=None):
    initialize_net.main(self, widget)

  def reset(self):
    '''
    This re-initializes the Network object.
    '''
    initialize_net.main(self)

  def load_file(self, filename):
    '''
    Load TSV file.
    '''
    load_data.load_file(self, filename)

  def load_file_as_string(self, file_string, filename=''):
    '''
    Load file as a string.
    '''
    load_data.load_file_as_string(self, file_string, filename=filename)


  def load_stdin(self):
    '''
    Load stdin TSV-formatted string.
    '''
    load_data.load_stdin(self)

  def load_tsv_to_net(self, file_buffer, filename=None):
    '''
    This will load a TSV matrix file buffer; this is exposed so that it will
    be possible to load data without having to read from a file.
    '''
    load_data.load_tsv_to_net(self, file_buffer, filename)

  def load_vect_post_to_net(self, vect_post):
    '''
    Load data in the vector format JSON.
    '''
    load_vect_post.main(self, vect_post)

  def load_data_file_to_net(self, filename):
    '''
    Load Clustergrammer's dat format (saved as JSON).
    '''
    inst_dat = self.load_json_to_dict(filename)
    load_data.load_data_to_net(self, inst_dat)

  def cluster(self, dist_type='cosine', run_clustering=True,
                 dendro=True, views=['N_row_sum', 'N_row_var'],
                 linkage_type='average', sim_mat=False, filter_sim=0.1,
                 calc_cat_pval=False, run_enrichr=None, enrichrgram=None):
    '''
    The main function performs hierarchical clustering, optionally generates filtered views (e.g. row-filtered views), and generates the :``visualization_json``.
    '''
    initialize_net.viz(self)

    make_clust_fun.make_clust(self, dist_type=dist_type, run_clustering=run_clustering,
                                   dendro=dendro,
                                   requested_views=views,
                                   linkage_type=linkage_type,
                                   sim_mat=sim_mat,
                                   filter_sim=filter_sim,
                                   calc_cat_pval=calc_cat_pval,
                                   run_enrichr=run_enrichr,
                                   enrichrgram=enrichrgram)

  def make_clust(self, dist_type='cosine', run_clustering=True,
                 dendro=True, views=['N_row_sum', 'N_row_var'],
                 linkage_type='average', sim_mat=False, filter_sim=0.1,
                 calc_cat_pval=False, run_enrichr=None, enrichrgram=None):
    '''
    ... Will be deprecated, renaming method cluster ...
    The main function performs hierarchical clustering, optionally generates filtered views (e.g. row-filtered views), and generates the :``visualization_json``.
    '''
    print('make_clust method will be deprecated in next version, please use cluster method.')
    initialize_net.viz(self)

    make_clust_fun.make_clust(self, dist_type=dist_type, run_clustering=run_clustering,
                                   dendro=dendro,
                                   requested_views=views,
                                   linkage_type=linkage_type,
                                   sim_mat=sim_mat,
                                   filter_sim=filter_sim,
                                   calc_cat_pval=calc_cat_pval,
                                   run_enrichr=run_enrichr,
                                   enrichrgram=enrichrgram)

  def produce_view(self, requested_view=None):
    '''
    This function is under development and will produce a single view on demand.
    '''
    print('\tproduce a single view of a matrix, will be used for get requests')

    if requested_view != None:
      print('requested_view')
      print(requested_view)

  def swap_nan_for_zero(self):
    '''
    Swaps all NaN (numpy NaN) instances for zero.
    '''
    # # may re-instate this in some form
    # self.dat['mat_orig'] = deepcopy(self.dat['mat'])

    self.dat['mat'][np.isnan(self.dat['mat'])] = 0

  def load_df(self, df):
    '''
    Load Pandas DataFrame.
    '''
    # self.__init__()
    self.reset()

    df_dict = {}
    df_dict['mat'] = deepcopy(df)
    # always define category colors if applicable when loading a df
    data_formats.df_to_dat(self, df_dict, define_cat_colors=True)

  def export_df(self):
    '''
    Export Pandas DataFrame/
    '''
    df_dict = data_formats.dat_to_df(self)
    return df_dict['mat']

  def df_to_dat(self, df, define_cat_colors=False):
    '''
    Load Pandas DataFrame (will be deprecated).
    '''
    data_formats.df_to_dat(self, df, define_cat_colors)

  def set_cat_color(self, axis, cat_index, cat_name, inst_color):

    if axis == 0:
      axis = 'row'
    if axis == 1:
      axis = 'col'

    try:
      # process cat_index
      cat_index = cat_index - 1
      cat_index = 'cat-' + str(cat_index)

      self.viz['cat_colors'][axis][cat_index][cat_name] = inst_color

    except:
      print('there was an error setting the category color')

  def dat_to_df(self):
    '''
    Export Pandas DataFrams (will be deprecated).
    '''
    return data_formats.dat_to_df(self)

  def export_net_json(self, net_type='viz', indent='no-indent'):
    '''
    Export dat or viz JSON.
    '''
    return export_data.export_net_json(self, net_type, indent)

  def export_viz_to_widget(self, which_viz='viz'):
    '''
    Export viz JSON, for use with clustergrammer_widget. Formerly method was
    named widget.
    '''

    return export_data.export_net_json(self, which_viz, 'no-indent')

  def widget(self, which_viz='viz'):
    '''
    Generate a widget visualization using the widget. The export_viz_to_widget
    method passes the visualization JSON to the instantiated widget, which is
    returned and visualized on the front-end.
    '''
    if hasattr(self, 'widget_class') == True:
      self.widget_instance = self.widget_class(network = self.export_viz_to_widget(which_viz))

      return self.widget_instance
    else:
      print('Can not make widget because Network has no attribute widget_class')
      print('Please instantiate Network with clustergrammer_widget using: Network(clustergrammer_widget)')


  def widget_df(self):
    '''
    Export a DataFrame from the front-end visualization. For instance, a user
    can filter to show only a single cluster using the dendrogram and then
    get a dataframe of this cluster using the widget_df method.
    '''

    if hasattr(self, 'widget_instance') == True:

      if self.widget_instance.mat_string != '':

        tmp_net = deepcopy(Network())

        df_string = self.widget_instance.mat_string

        tmp_net.load_file_as_string(df_string)

        df = tmp_net.export_df()

        return df

      else:
        return self.export_df()

    else:
      if hasattr(self, 'widget_class') == True:
        print('Please make the widget before exporting the widget DataFrame.')
        print('Do this using the widget method: net.widget()')

      else:
        print('Can not make widget because Network has no attribute widget_class')
        print('Please instantiate Network with clustergrammer_widget using: Network(clustergrammer_widget)')

  def write_json_to_file(self, net_type, filename, indent='no-indent'):
    '''
    Save dat or viz as a JSON to file.
    '''
    export_data.write_json_to_file(self, net_type, filename, indent)

  def write_matrix_to_tsv(self, filename=None, df=None):
    '''
    Export data-matrix to file.
    '''
    return export_data.write_matrix_to_tsv(self, filename, df)

  def filter_sum(self, inst_rc, threshold, take_abs=True):
    '''
    Filter a network's rows or columns based on the sum across rows or columns.
    '''
    inst_df = self.dat_to_df()
    if inst_rc == 'row':
      inst_df = run_filter.df_filter_row_sum(inst_df, threshold, take_abs)
    elif inst_rc == 'col':
      inst_df = run_filter.df_filter_col_sum(inst_df, threshold, take_abs)
    self.df_to_dat(inst_df)

  def filter_N_top(self, inst_rc, N_top, rank_type='sum'):
    '''
    Filter the matrix rows or columns based on sum/variance, and only keep the top
    N.
    '''
    inst_df = self.dat_to_df()

    inst_df = run_filter.filter_N_top(inst_rc, inst_df, N_top, rank_type)

    self.df_to_dat(inst_df)

  def filter_threshold(self, inst_rc, threshold, num_occur=1):
    '''
    Filter the matrix rows or columns based on num_occur values being above a
    threshold (in absolute value).
    '''
    inst_df = self.dat_to_df()

    inst_df = run_filter.filter_threshold(inst_df, inst_rc, threshold,
      num_occur)

    self.df_to_dat(inst_df)

  def filter_cat(self, axis, cat_index, cat_name):
    '''
    Filter the matrix based on their category. cat_index is the index of the category, the first category has index=1.
    '''
    run_filter.filter_cat(self, axis, cat_index, cat_name)

  def filter_names(self, axis, names):
    '''
    Filter the visualization using row/column names. The function takes, axis ('row'/'col') and names, a list of strings.
    '''
    run_filter.filter_names(self, axis, names)

  def clip(self, lower=None, upper=None):
    '''
    Trim values at input thresholds using pandas function
    '''
    df = self.export_df()
    df = df.clip(lower=lower, upper=upper)
    self.load_df(df)

  def normalize(self, df=None, norm_type='zscore', axis='row', keep_orig=False):
    '''
    Normalize the matrix rows or columns using Z-score (zscore) or Quantile Normalization (qn). Users can optionally pass in a DataFrame to be normalized (and this will be incorporated into the Network object).
    '''
    normalize_fun.run_norm(self, df, norm_type, axis, keep_orig)

  def downsample(self, df=None, ds_type='kmeans', axis='row', num_samples=100, random_state=1000):
    '''
    Downsample the matrix rows or columns (currently supporting kmeans only). Users can optionally pass in a DataFrame to be downsampled (and this will be incorporated into the network object).
    '''

    return downsample_fun.main(self, df, ds_type, axis, num_samples, random_state)

  def random_sample(self, num_samples, df=None, replace=False, weights=None, random_state=100, axis='row'):
    '''
    Return random sample of matrix.
    '''

    if df is None:
      df = self.dat_to_df()

    if axis == 'row':
      axis = 0
    if axis == 'col':
      axis = 1

    df = self.export_df()
    df = df.sample(n=num_samples, replace=replace, weights=weights, random_state=random_state,  axis=axis)

    self.load_df(df)

  def add_cats(self, axis, cat_data):
    '''
    Add categories to rows or columns using cat_data array of objects. Each object in cat_data is a dictionary with one key (category title) and value (rows/column names) that have this category. Categories will be added onto the existing categories and will be added in the order of the objects in the array.

    Example ``cat_data``::


        [
          {
            "title": "First Category",
            "cats": {
              "true": [
                "ROS1",
                "AAK1"
              ]
            }
          },
          {
            "title": "Second Category",
            "cats": {
              "something": [
                "PDK4"
              ]
            }
          }
        ]


    '''
    for inst_data in cat_data:
      categories.add_cats(self, axis, inst_data)

  def dendro_cats(self, axis, dendro_level):
    '''
    Generate categories from dendrogram groups/clusters. The dendrogram has 11
    levels to choose from 0 -> 10. Dendro_level can be given as an integer or
    string.
    '''
    categories.dendro_cats(self, axis, dendro_level)

  def Iframe_web_app(self, filename=None, width=1000, height=800):

    link = iframe_web_app.main(self, filename, width, height)

    return link

  def enrichrgram(self, lib, axis='row'):
    '''
    Add Enrichr gene enrichment results to your visualization (where your rows
    are genes). Run enrichrgram before clustering to incldue enrichment results
    as row categories. Enrichrgram can also be run on the front-end using the
    Enrichr logo at the top left.

    Set lib to the Enrichr library that you want to use for enrichment analysis.
    Libraries included:

      * ChEA_2016
      * KEA_2015
      * ENCODE_TF_ChIP-seq_2015
      * ENCODE_Histone_Modifications_2015
      * Disease_Perturbations_from_GEO_up
      * Disease_Perturbations_from_GEO_down
      * GO_Molecular_Function_2015
      * GO_Biological_Process_2015
      * GO_Cellular_Component_2015
      * Reactome_2016
      * KEGG_2016
      * MGI_Mammalian_Phenotype_Level_4
      * LINCS_L1000_Chem_Pert_up
      * LINCS_L1000_Chem_Pert_down

    '''

    df = self.export_df()
    df, bar_info = enr_fun.add_enrichr_cats(df, axis, lib)
    self.load_df(df)

    self.dat['enrichrgram_lib'] = lib
    self.dat['row_cat_bars'] = bar_info

  @staticmethod
  def load_gmt(filename):
    return load_data.load_gmt(filename)

  @staticmethod
  def load_json_to_dict(filename):
    return load_data.load_json_to_dict(filename)

  @staticmethod
  def save_dict_to_json(inst_dict, filename, indent='no-indent'):
    export_data.save_dict_to_json(inst_dict, filename, indent)