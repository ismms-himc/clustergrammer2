import pandas as pd
import numpy as np
from sklearn.cluster import MiniBatchKMeans
# string used to format titles
super_string = ': '

def main(net, df=None, ds_type='kmeans', axis='row', num_samples=100, random_state=1000):

  if df is None:
    df = net.export_df()

  # # run downsampling
  # random_state = 1000

  ds_df, ds_data = run_kmeans_mini_batch(df, num_samples, axis, random_state)

  net.load_df(ds_df)

  return ds_data

def run_kmeans_mini_batch(df, num_samples=100, axis='row', random_state=1000):


  # gather downsampled axis information
  if axis == 'row':
    X = df
    orig_labels = df.index.tolist()
    non_ds_labels = df.columns.tolist()

  else:
    X = df.transpose()
    orig_labels = df.columns.tolist()
    non_ds_labels = df.index.tolist()

  cat_index = 1

  # run until the number of returned clusters with data-points is equal to the
  # number of requested clusters
  num_returned_clusters = 0
  while num_samples != num_returned_clusters:

    clusters, num_returned_clusters, cluster_data, cluster_pop = \
      calc_mbk_clusters(X, num_samples, random_state)

    random_state = random_state + random_state

  clust_numbers = range(num_returned_clusters)
  clust_labels = [ 'cluster-' + str(i) for i in clust_numbers]

  if type(orig_labels[0]) is tuple:
    found_cats = True
  else:
    found_cats = False

  # Gather categories if necessary
  ########################################
  # check if there are categories
  if found_cats:
    all_cats = generate_cat_data(cluster_data, orig_labels, num_samples)

  # genrate cluster labels, e.g. add number in each cluster and majority cat
  # if necessary
  cluster_labels = []
  for i in range(num_returned_clusters):

    inst_name = 'Cluster: ' + clust_labels[i]
    num_in_clust_string =  'number in clust: '+ str(cluster_pop[i])

    inst_tuple = (inst_name,)

    if found_cats:
      for cat_data in all_cats:
        cat_values = cat_data['counts'][i]
        max_cat_fraction = cat_values.max()
        max_index = np.where(cat_values == max_cat_fraction)[0][0]
        max_cat_name = cat_data['types'][max_index]

        # add category title if available
        cat_name_string = 'Majority-'+ cat_data['title'] +': ' + max_cat_name

        inst_tuple = inst_tuple + (cat_name_string,)

    inst_tuple = inst_tuple + (num_in_clust_string,)

    cluster_labels.append(inst_tuple)

  # ds_df is always downsampling the rows, if the user wants to downsample the
  # columns, the df will be switched back later
  ds_df = pd.DataFrame(data=clusters, index=cluster_labels, columns=non_ds_labels)

  # swap back for downsampled columns
  if axis == 'col':
    ds_df = ds_df.transpose()

  return ds_df, cluster_data

def generate_cat_data(cluster_data, orig_labels, num_samples):

  # generate an array of orig_labels, using an array so that I can gather
  # label subsets using indices
  orig_array = np.asarray(orig_labels)

  example_label = orig_labels[0]

  # find out how many string categories are available
  num_cats = 0
  for i in range(len(example_label)):

    if i > 0:
      inst_cat = example_label[i]
      if super_string in inst_cat:
        inst_cat = inst_cat.split(super_string)[1]

      string_cat = True
      try:
        float(inst_cat)
        string_cat = False
      except:
        string_cat = True

      if string_cat:
        num_cats = num_cats + 1

  all_cats = []

  for cat_index in range(num_cats):

    # index zero is for the names
    cat_index = cat_index + 1

    cat_data = {}

    if super_string in example_label[cat_index]:
      cat_data['title'] = example_label[cat_index].split(super_string)[0]
    else:
      cat_data['title'] = 'Category'

    # if there are string categories, then keep track of how many of each category
    # are found in each of the downsampled clusters.
    cat_data['types'] = []

    # gather possible categories
    for inst_label in orig_labels:

      inst_cat = inst_label[cat_index]

      if super_string in inst_cat:
        inst_cat = inst_cat.split(super_string)[1]

      # get first category
      cat_data['types'].append(inst_cat)

    cat_data['types'] = sorted(list(set(cat_data['types'])))

    num_cats = len(cat_data['types'])

    # initialize cat_data['counts'] dictionary
    cat_data['counts'] = {}
    for inst_clust in range(num_samples):
      cat_data['counts'][inst_clust] = np.zeros([num_cats])

    # populate cat_data['counts']
    for inst_clust in range(num_samples):

      # get the indicies of all original labels that fall in the cluster
      found = np.where(cluster_data == inst_clust)
      found_indicies = found[0]

      clust_names = orig_array[found_indicies]

      for inst_name in clust_names:

        # get first category name
        inst_name = inst_name[cat_index]

        if super_string in inst_name:
          inst_name = inst_name.split(super_string)[1]

        tmp_index = cat_data['types'].index(inst_name)

        cat_data['counts'][inst_clust][tmp_index] = cat_data['counts'][inst_clust][tmp_index] + 1

    # calculate fractions
    for inst_clust in range(num_samples):
      # get array
      counts = cat_data['counts'][inst_clust]
      inst_total = np.sum(counts)
      cat_data['counts'][inst_clust] = cat_data['counts'][inst_clust] / inst_total

    all_cats.append(cat_data)

  return all_cats

def calc_mbk_clusters(X, n_clusters, random_state=1000):

  # kmeans is run with rows as data-points and columns as dimensions
  mbk = MiniBatchKMeans(init='k-means++', n_clusters=n_clusters,
                         max_no_improvement=100, verbose=0,
                         random_state=random_state)

  # need to loop through each label (each k-means cluster) and count how many
  # points were given this label. This will give the population size of each label
  mbk.fit(X)
  cluster_data = mbk.labels_
  clusters = mbk.cluster_centers_

  mbk_cluster_names, cluster_pop = np.unique(cluster_data, return_counts=True)

  num_returned_clusters = len(cluster_pop)

  return clusters, num_returned_clusters, cluster_data, cluster_pop