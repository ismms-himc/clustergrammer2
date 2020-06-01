from . import make_unique_labels
import pandas as pd
from . import categories

def df_to_dat(net, df, define_cat_colors=False):
  '''
  This is always run when data is loaded.
  '''

  # check if df has unique values
  df = make_unique_labels.main(net, df)

  net.dat['mat'] = df.values
  net.dat['nodes']['row'] = df.index.tolist()
  net.dat['nodes']['col'] = df.columns.tolist()

  # parse categories from tuple
  ##################################
  if net.meta_cat == False:
    for axis in ['row', 'col']:

      inst_nodes = net.dat['nodes'][axis]

      if type(inst_nodes[0]) is tuple:

        if axis == 'row':
          net.dat['node_info'][axis]['full_names'] = df.index.tolist()
        elif axis == 'col':
          net.dat['node_info'][axis]['full_names'] = df.columns.tolist()

        # get the number of categories from the length of the tuple
        # subtract 1 because the name is the first element of the tuple
        num_cat = len(inst_nodes[0]) - 1
        for inst_cat in range(num_cat):
          cat_name = 'cat-' + str(inst_cat)
          cat_index = inst_cat + 1
          cat_values = [x[cat_index] for x in inst_nodes]
          net.dat['node_info'][axis][cat_name] = cat_values

        # clean up nodes after parsing categories
        net.dat['nodes'][axis] = [x[0] for x in inst_nodes]

  else:
    # print('meta_cat!!!!!!!!')

    for axis in ['row', 'col']:

      inst_nodes = net.dat['nodes'][axis]

      if axis == 'row':
        net.dat['node_info'][axis]['full_names'] = df.index.tolist()
      elif axis == 'col':
        net.dat['node_info'][axis]['full_names'] = df.columns.tolist()

      if axis == 'row':
        inst_cats = net.meta_row.columns.tolist()
      else:
        inst_cats = net.meta_col.columns.tolist()

      num_cat = len(inst_cats)
      for inst_cat in range(num_cat):
        cat_name = 'cat-' + str(inst_cat)
        cat_index = inst_cat + 1
        # cat_value = [x[cat_index] for x in inst_nodes]

        cat_title = inst_cats[inst_cat]
        if axis == 'row':
          cat_values = net.meta_row[cat_title].apply(lambda x: cat_title + ': ' + x).values.tolist()
        else:
          cat_values = net.meta_col[cat_title].apply(lambda x: cat_title + ': ' + x).values.tolist()

        net.dat['node_info'][axis][cat_name] = cat_values

  categories.dict_cat(net, define_cat_colors=define_cat_colors)

def dat_to_df(net):

  nodes = {}
  for axis in ['row', 'col']:
    if 'full_names' in net.dat['node_info'][axis]:
      nodes[axis] = net.dat['node_info'][axis]['full_names']
    else:
      nodes[axis] = net.dat['nodes'][axis]

  df = pd.DataFrame(data=net.dat['mat'], columns=nodes['col'],
      index=nodes['row'])

  return df

def mat_to_numpy_arr(self):
  ''' convert list to numpy array - numpy arrays can not be saved as json '''
  import numpy as np
  self.dat['mat'] = np.asarray(self.dat['mat'])