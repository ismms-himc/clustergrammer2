def check_categories(lines):
  '''
  find out how many row and col categories are available
  '''
  # count the number of row categories
  rcat_line = lines[0].split('\t')

  # calc the number of row names and categories
  num_rc = 0
  found_end = False

  # skip first tab
  for inst_string in rcat_line[1:]:
    if inst_string == '':
      if found_end is False:
        num_rc = num_rc + 1
    else:
      found_end = True

  max_rcat = 15
  if max_rcat > len(lines):
    max_rcat = len(lines) - 1

  num_cc = 0
  for i in range(max_rcat):
    ccat_line = lines[i + 1].split('\t')

    # make sure that line has length greater than one to prevent false cats from
    # trailing new lines at end of matrix
    if ccat_line[0] == '' and len(ccat_line) > 1:
      num_cc = num_cc + 1

  num_labels = {}
  num_labels['row'] = num_rc + 1
  num_labels['col'] = num_cc + 1

  return num_labels

def dict_cat(net):
  '''
  make a dictionary of node-category associations
  '''
  for inst_rc in ['row', 'col']:
    inst_keys = list(net.dat['node_info'][inst_rc].keys())
    all_cats = [x for x in inst_keys if 'cat-' in x]

    for inst_name_cat in all_cats:
      dict_cat = {}
      tmp_cats = net.dat['node_info'][inst_rc][inst_name_cat]
      tmp_nodes = net.dat['nodes'][inst_rc]

      for i in range(len(tmp_cats)):
        inst_cat = tmp_cats[i]
        inst_node = tmp_nodes[i]

        if inst_cat not in dict_cat:
          dict_cat[inst_cat] = []

        dict_cat[inst_cat].append(inst_node)

      tmp_name = 'dict_' + inst_name_cat.replace('-', '_')
      net.dat['node_info'][inst_rc][tmp_name] = dict_cat

def calc_cat_clust_order(net, inst_rc):
  '''
  cluster category subset of data
  '''
  from .__init__ import Network
  from copy import deepcopy
  from . import calc_clust, run_filter

  inst_keys = list(net.dat['node_info'][inst_rc].keys())
  all_cats = [x for x in inst_keys if 'cat-' in x]

  if len(all_cats) > 0:

    for inst_name_cat in all_cats:

      tmp_name = 'dict_' + inst_name_cat.replace('-', '_')
      dict_cat = net.dat['node_info'][inst_rc][tmp_name]

      unordered_cats = dict_cat.keys()

      ordered_cats = order_categories(unordered_cats)

      # this is the ordering of the columns based on their category, not
      # including their clustering ordering within category
      all_cat_orders = []
      tmp_names_list = []
      for inst_cat in ordered_cats:

        inst_nodes = dict_cat[inst_cat]

        tmp_names_list.extend(inst_nodes)

      #   cat_net = deepcopy(Network())

      #   cat_net.dat['mat'] = deepcopy(net.dat['mat'])
      #   cat_net.dat['nodes'] = deepcopy(net.dat['nodes'])

      #   cat_df = cat_net.dat_to_df()

      #   sub_df = {}
      #   if inst_rc == 'col':
      #     sub_df['mat'] = cat_df['mat'][inst_nodes]
      #   elif inst_rc == 'row':
      #     # need to transpose df
      #     cat_df['mat'] = cat_df['mat'].transpose()
      #     sub_df['mat'] = cat_df['mat'][inst_nodes]
      #     sub_df['mat'] = sub_df['mat'].transpose()

      #   # filter matrix before clustering
      #   ###################################
      #   threshold = 0.0001
      #   sub_df = run_filter.df_filter_row_sum(sub_df, threshold)
      #   sub_df = run_filter.df_filter_col_sum(sub_df, threshold)

      #   # load back to dat
      #   cat_net.df_to_dat(sub_df)

      #   cat_mat_shape = cat_net.dat['mat'].shape

      #   print('***************')
      #   try:
      #     if cat_mat_shape[0]>1 and cat_mat_shape[1] > 1 and all_are_numbers == False:

      #       calc_clust.cluster_row_and_col(cat_net, 'cos')
      #       inst_cat_order = cat_net.dat['node_info'][inst_rc]['clust']
      #     else:
      #       inst_cat_order = list(range(len(cat_net.dat['nodes'][inst_rc])))

      #   except:
      #     inst_cat_order = list(range(len(cat_net.dat['nodes'][inst_rc])))


      #   prev_order_len = len(all_cat_orders)

      #   # add prev order length to the current order number
      #   inst_cat_order = [i + prev_order_len for i in inst_cat_order]
      #   all_cat_orders.extend(inst_cat_order)

      # # generate ordered list of row/col names, which will be used to
      # # assign the order to specific nodes
      # names_clust_list = [x for (y, x) in sorted(zip(all_cat_orders,
      #                     tmp_names_list))]

      names_clust_list = tmp_names_list

      # calc category-cluster order
      final_order = []

      for i in range(len(net.dat['nodes'][inst_rc])):

        inst_node_name = net.dat['nodes'][inst_rc][i]
        inst_node_num = names_clust_list.index(inst_node_name)

        final_order.append(inst_node_num)

      inst_index_cat = inst_name_cat.replace('-', '_') + '_index'

      net.dat['node_info'][inst_rc][inst_index_cat] = final_order


def order_categories(unordered_cats):
  '''
  If categories are strings, then simple ordering is fine.
  If categories are values then I'll need to order based on their values.
  The final ordering is given as the original categories (including titles) in a
  ordered list.
  '''

  no_titles = remove_titles(unordered_cats)

  all_are_numbers = check_all_numbers(no_titles)

  if all_are_numbers:
    ordered_cats = order_cats_based_on_values(unordered_cats, no_titles)
  else:
    ordered_cats = sorted(unordered_cats)

  return ordered_cats


def order_cats_based_on_values(unordered_cats, values_list):
  import pandas as pd

  try:
    # convert values_list to values
    values_list = [float(i) for i in values_list]

    inst_series = pd.Series(data=values_list, index=unordered_cats)

    inst_series.sort_values(inplace=True)

    ordered_cats = inst_series.index.tolist()

    # ordered_cats = unordered_cats
  except:
    # keep default ordering if error occurs
    print('error sorting cats based on values ')
    ordered_cats = unordered_cats

  return ordered_cats

def check_all_numbers(no_titles):
  all_numbers = True
  for tmp in no_titles:
    if is_number(tmp) == False:
      all_numbers = False

  return all_numbers

def remove_titles(cats):
  from copy import deepcopy

  # check if all have titles
  ###########################
  all_have_titles = True

  for inst_cat in cats:
    if is_number(inst_cat) == False:
      if ': ' not in inst_cat:
        all_have_titles = False
    else:
      all_have_titles = False

  if all_have_titles:
    no_titles = cats
    no_titles = [i.split(': ')[1] for i in no_titles]

  else:
    no_titles = cats

  return no_titles

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False