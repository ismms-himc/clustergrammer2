from . import make_unique_labels

def df_to_dat(net, df, define_cat_colors=False):
  '''
  This is always run when data is loaded.
  '''
  from . import categories

  # check if df has unique values
  df['mat'] = make_unique_labels.main(net, df['mat'])

  net.dat['mat'] = df['mat'].values
  net.dat['nodes']['row'] = df['mat'].index.tolist()
  net.dat['nodes']['col'] = df['mat'].columns.tolist()

  for axis in ['row', 'col']:

    if type(net.dat['nodes'][axis][0]) is tuple:
      # get the number of categories from the length of the tuple
      # subtract 1 because the name is the first element of the tuple
      num_cat = len(net.dat['nodes'][axis][0]) - 1

      net.dat['node_info'][axis]['full_names'] = net.dat['nodes'][axis]

      for axisat in range(num_cat):
        net.dat['node_info'][axis]['cat-' + str(axisat)] = \
          [i[axisat + 1] for i in net.dat['nodes'][axis]]

      net.dat['nodes'][axis] = [i[0] for i in net.dat['nodes'][axis]]

  if 'mat_orig' in df:
    net.dat['mat_orig'] = df['mat_orig'].values

  categories.dict_cat(net, define_cat_colors=define_cat_colors)

def dat_to_df(net):
  import pandas as pd

  df = {}
  nodes = {}
  for axis in ['row', 'col']:
    if 'full_names' in net.dat['node_info'][axis]:
      nodes[axis] = net.dat['node_info'][axis]['full_names']
    else:
      nodes[axis] = net.dat['nodes'][axis]

  df['mat'] = pd.DataFrame(data=net.dat['mat'], columns=nodes['col'],
      index=nodes['row'])

  if 'mat_orig' in net.dat:
    df['mat_orig'] = pd.DataFrame(data=net.dat['mat_orig'],
      columns=nodes['col'], index=nodes['row'])

  return df

def mat_to_numpy_arr(self):
  ''' convert list to numpy array - numpy arrays can not be saved as json '''
  import numpy as np
  self.dat['mat'] = np.asarray(self.dat['mat'])