import numpy as np
import pandas as pd
from copy import deepcopy

def main(net):
  '''
  calculate pvalue of category closeness
  '''
  # calculate the distance between the data points within the same category and
  # compare to null distribution
  for inst_rc in ['row', 'col']:

    inst_nodes = deepcopy(net.dat['nodes'][inst_rc])

    inst_index = deepcopy(net.dat['node_info'][inst_rc]['clust'])

    # reorder based on clustered order
    inst_nodes = [ inst_nodes[i] for i in inst_index]

    # make distance matrix dataframe
    dm = dist_matrix_lattice(inst_nodes)

    node_infos = list(net.dat['node_info'][inst_rc].keys())

    all_cats = []
    for inst_info in node_infos:
      if 'dict_cat_' in inst_info:
        all_cats.append(inst_info)

    for cat_dict in all_cats:

      tmp_dict = net.dat['node_info'][inst_rc][cat_dict]

      pval_name = cat_dict.replace('dict_','pval_')
      net.dat['node_info'][inst_rc][pval_name] = {}

      for cat_name in tmp_dict:

        subset = tmp_dict[cat_name]

        inst_median = calc_median_dist_subset(dm, subset)

        hist = calc_hist_distances(dm, subset, inst_nodes)

        pval = 0

        for i in range(len(hist['prob'])):
          if i == 0:
            pval = hist['prob'][i]
          if i >= 1:
            if inst_median >= hist['bins'][i]:
              pval = pval + hist['prob'][i]

        net.dat['node_info'][inst_rc][pval_name][cat_name] = pval

def dist_matrix_lattice(names):
  from scipy.spatial.distance import pdist, squareform

  lattice_size = len(names)
  mat = np.zeros([lattice_size, 1])
  mat[:,0] = list(range(lattice_size))

  inst_dm = pdist(mat, metric='euclidean')

  inst_dm[inst_dm < 0] = float(0)

  inst_dm = squareform(inst_dm)

  df = pd.DataFrame(data=inst_dm, columns=names, index=names)

  return df


def calc_median_dist_subset(dm, subset):
  return np.median(dm[subset].loc[subset].values)

def calc_hist_distances(dm, subset, inst_nodes):
  np.random.seed(100)

  num_null = 1000
  num_points = len(subset)

  median_dist = []
  for i in range(num_null):
    tmp = np.random.choice(inst_nodes, num_points, replace=False)
    median_dist.append( np.median(dm[tmp].loc[tmp].values)  )

  tmp_dist = sorted(deepcopy(median_dist))

  median_dist = np.asarray(median_dist)
  s1 = pd.Series(median_dist)
  hist = np.histogram(s1, bins=30)

  H = {}
  H['prob'] = hist[0]/np.float(num_null)
  H['bins'] = hist[1]

  return H