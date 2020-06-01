def viz_json(net, dendro=True, links=False):
  ''' make the dictionary for the clustergram.js visualization '''
  from . import calc_clust
  import numpy as np

  # linkage information
  net.viz['linkage'] = {}
  net.viz['linkage']['row'] = net.dat['node_info']['row']['Y'].tolist()
  net.viz['linkage']['col'] = net.dat['node_info']['col']['Y'].tolist()

  # node information
  for inst_rc in net.dat['nodes']:

    inst_keys = net.dat['node_info'][inst_rc]
    all_cats = [x for x in inst_keys if 'cat-' in x]

    for i in range(len(net.dat['nodes'][inst_rc])):
      inst_dict = {}
      inst_dict['name'] = net.dat['nodes'][inst_rc][i]
      inst_dict['ini'] = net.dat['node_info'][inst_rc]['ini'][i]
      inst_dict['clust'] = net.dat['node_info'][inst_rc]['clust'].index(i)
      inst_dict['rank'] = net.dat['node_info'][inst_rc]['rank'][i]

      if 'rankvar' in inst_keys:
        inst_dict['rankvar'] = net.dat['node_info'][inst_rc]['rankvar'][i]

      # fix for similarity matrix
      if len(all_cats) > 0:

        for inst_name_cat in all_cats:

          actual_cat_name = net.dat['node_info'][inst_rc][inst_name_cat][i]
          inst_dict[inst_name_cat] = actual_cat_name

          check_pval = 'pval_'+inst_name_cat.replace('-','_')

          if check_pval in net.dat['node_info'][inst_rc]:
            tmp_pval_name = inst_name_cat.replace('-','_') + '_pval'
            inst_dict[tmp_pval_name] = net.dat['node_info'][inst_rc][check_pval][actual_cat_name]

          tmp_index_name = inst_name_cat.replace('-', '_') + '_index'

          inst_dict[tmp_index_name] = net.dat['node_info'][inst_rc] \
              [tmp_index_name][i]


      if len(net.dat['node_info'][inst_rc]['value']) > 0:
        inst_dict['value'] = net.dat['node_info'][inst_rc]['value'][i]

      if len(net.dat['node_info'][inst_rc]['info']) > 0:
        inst_dict['info'] = net.dat['node_info'][inst_rc]['info'][i]

      net.viz[inst_rc + '_nodes'].append(inst_dict)

  # save data as links or mat
  ###########################
  if links is True:
    for i in range(len(net.dat['nodes']['row'])):
      for j in range(len(net.dat['nodes']['col'])):

        inst_dict = {}
        inst_dict['source'] = i
        inst_dict['target'] = j
        inst_dict['value'] = float(net.dat['mat'][i, j])

        if np.isnan(inst_dict['value_orig']):
          inst_dict['value_orig'] = 'NaN'

        net.viz['links'].append(inst_dict)

  else:
    net.viz['mat'] = net.dat['mat'].tolist()


