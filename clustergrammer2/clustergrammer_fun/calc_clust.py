def cluster_row_and_col(net, dist_type='cosine', linkage_type='average',
                        dendro=True, run_clustering=True, run_rank=True,
                        ignore_cat=False, calc_cat_pval=False, links=False):
  ''' cluster net.dat and make visualization json, net.viz.
  optionally leave out dendrogram colorbar groups with dendro argument '''

  import scipy
  from copy import deepcopy
  from scipy.spatial.distance import pdist
  from . import categories, make_viz, cat_pval

  dm = {}
  for axis in ['row', 'col']:

    tmp_mat = deepcopy(net.dat['mat'])
    dm[axis] = calc_distance_matrix(tmp_mat, axis, dist_type)

    # save directly to dat structure
    node_info = net.dat['node_info'][axis]

    node_info['ini'] = list(range( len(net.dat['nodes'][axis]), -1, -1))

    # cluster
    if run_clustering is True:
      node_info['clust'], node_info['Y'] = clust_and_group(net,
                                                           dm[axis],
                                                           linkage_type=linkage_type)
    else:
      dendro = False
      node_info['clust'] = node_info['ini']

    # sorting
    if run_rank is True:
      node_info['rank'] = sort_rank_nodes(net, axis, 'sum')
      node_info['rankvar'] = sort_rank_nodes(net, axis, 'var')
    else:
      node_info['rank'] = node_info['ini']
      node_info['rankvar'] = node_info['ini']

    ##################################
    if ignore_cat is False:
      categories.calc_cat_clust_order(net, axis)

  if calc_cat_pval is True:
    cat_pval.main(net)

  # make the visualization json
  make_viz.viz_json(net, dendro, links)

  return dm

def calc_distance_matrix(tmp_mat, axis, dist_type='cosine'):
  from scipy.spatial.distance import pdist
  import numpy as np

  if axis == 'row':
    inst_dm = pdist(tmp_mat, metric=dist_type)
  elif axis == 'col':
    inst_dm = pdist(tmp_mat.transpose(), metric=dist_type)

  inst_dm[inst_dm < 0] = float(0)

  return inst_dm

def clust_and_group(net, inst_dm, linkage_type='average'):
  import scipy.cluster.hierarchy as hier
  Y = hier.linkage(inst_dm, method=linkage_type)
  Z = hier.dendrogram(Y, no_plot=True)
  inst_clust_order = Z['leaves']

  return inst_clust_order, Y

def sort_rank_nodes(net, rowcol, rank_type):
  import numpy as np
  from operator import itemgetter
  from copy import deepcopy

  tmp_nodes = deepcopy(net.dat['nodes'][rowcol])
  inst_mat = deepcopy(net.dat['mat'])

  sum_term = []
  for i in range(len(tmp_nodes)):
    inst_dict = {}
    inst_dict['name'] = tmp_nodes[i]

    if rowcol == 'row':
      if rank_type == 'sum':
        inst_dict['rank'] = np.sum(inst_mat[i, :])
      elif rank_type == 'var':
        inst_dict['rank'] = np.var(inst_mat[i, :])
    else:
      if rank_type == 'sum':
        inst_dict['rank'] = np.sum(inst_mat[:, i])
      elif rank_type == 'var':
        inst_dict['rank'] = np.var(inst_mat[:, i])

    sum_term.append(inst_dict)

  sum_term = sorted(sum_term, key=itemgetter('rank'), reverse=False)

  tmp_sort_nodes = []
  for inst_dict in sum_term:
    tmp_sort_nodes.append(inst_dict['name'])

  sort_index = []
  for inst_node in tmp_nodes:
    sort_index.append(tmp_sort_nodes.index(inst_node))

  return sort_index
