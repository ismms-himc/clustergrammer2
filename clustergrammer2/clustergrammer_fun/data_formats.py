from . import make_unique_labels

def df_to_dat(net, df, define_cat_colors=False):
  '''
  This is always run when data is loaded.
  '''
  from . import categories

  # print('df_to_dat!!!!!!!!!!!!!!!!!!!!!!!!')

  # check if df has unique values
  df = make_unique_labels.main(net, df)

  net.dat['mat'] = df.values
  net.dat['nodes']['row'] = df.index.tolist()
  net.dat['nodes']['col'] = df.columns.tolist()

  for axis in ['row', 'col']:

    if type(net.dat['nodes'][axis][0]) is tuple:
      # get the number of categories from the length of the tuple
      # subtract 1 because the name is the first element of the tuple
      num_cat = len(net.dat['nodes'][axis][0]) - 1

      if axis == 'row':
        net.dat['node_info'][axis]['full_names'] = df.index.tolist()
      elif axis == 'col':
        net.dat['node_info'][axis]['full_names'] = df.columns.tolist()

      # makes short names

      for inst_cat in range(num_cat):
        cat_name = 'cat-' + str(inst_cat)
        cat_value = [i[inst_cat + 1] for i in net.dat['nodes'][axis]]
        net.dat['node_info'][axis][cat_name] = cat_value

      # nodes are cleaned up
      net.dat['nodes'][axis] = [i[0] for i in net.dat['nodes'][axis]]

  categories.dict_cat(net, define_cat_colors=define_cat_colors)

def dat_to_df(net):
  import pandas as pd

  # print('dat_to_df')

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