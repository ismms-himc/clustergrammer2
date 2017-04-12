def make_clust(net, dist_type='cosine', run_clustering=True, dendro=True,
                          requested_views=['pct_row_sum', 'N_row_sum'],
                          linkage_type='average', sim_mat=False, filter_sim=0.1,
                          calc_cat_pval=False, sim_mat_views=['N_row_sum'],
                          run_enrichr=None, enrichrgram=None):
  '''
  This will calculate multiple views of a clustergram by filtering the
  data and clustering after each filtering. This filtering will keep the top
  N rows based on some quantity (sum, num-non-zero, etc).
  '''
  from copy import deepcopy
  import scipy
  from . import calc_clust, run_filter, make_views, make_sim_mat, cat_pval
  from . import enrichr_functions as enr_fun

  df = net.dat_to_df()

  threshold = 0.0001
  df = run_filter.df_filter_row_sum(df, threshold)
  df = run_filter.df_filter_col_sum(df, threshold)

  # default setting
  define_cat_colors = False

  if run_enrichr is not None:
    df = enr_fun.add_enrichr_cats(df, 'row', run_enrichr)

    define_cat_colors = True

  # calculate initial view with no row filtering
  net.df_to_dat(df, define_cat_colors=True)


  inst_dm = calc_clust.cluster_row_and_col(net, dist_type=dist_type,
                                linkage_type=linkage_type,
                                run_clustering=run_clustering,
                                dendro=dendro, ignore_cat=False,
                                calc_cat_pval=calc_cat_pval)

  all_views = []
  send_df = deepcopy(df)

  if 'N_row_sum' in requested_views:
    all_views = make_views.N_rows(net, send_df, all_views,
                                  dist_type=dist_type, rank_type='sum')

  if 'N_row_var' in requested_views:
    all_views = make_views.N_rows(net, send_df, all_views,
                                  dist_type=dist_type, rank_type='var')

  if 'pct_row_sum' in requested_views:
    all_views = make_views.pct_rows(net, send_df, all_views,
                                    dist_type=dist_type, rank_type='sum')

  if 'pct_row_var' in requested_views:
    all_views = make_views.pct_rows(net, send_df, all_views,
                                    dist_type=dist_type, rank_type='var')

  which_sim = []

  if sim_mat == True:
    which_sim = ['row', 'col']
  elif sim_mat == 'row':
    which_sim = ['row']
  elif sim_mat == 'col':
    which_sim = ['col']

  if sim_mat is not False:
    sim_net = make_sim_mat.main(net, inst_dm, which_sim, filter_sim, sim_mat_views)

    net.sim = {}

    for inst_rc in which_sim:
      net.sim[inst_rc] = sim_net[inst_rc].viz

      if inst_rc == 'row':
        other_rc = 'col'
      elif inst_rc == 'col':
        other_rc = 'row'

      # keep track of cat_colors
      net.sim[inst_rc]['cat_colors'][inst_rc] = net.viz['cat_colors'][inst_rc]
      net.sim[inst_rc]['cat_colors'][other_rc] = net.viz['cat_colors'][inst_rc]

  else:
    net.sim = {}

  net.viz['views'] = all_views

  if enrichrgram != None:
    # toggle enrichrgram functionality from back-end
    net.viz['enrichrgram'] = enrichrgram

  if 'enrichrgram_lib' in net.dat:
    net.viz['enrichrgram'] = True
    net.viz['enrichrgram_lib'] = net.dat['enrichrgram_lib']

  if 'row_cat_bars' in net.dat:
    net.viz['row_cat_bars'] = net.dat['row_cat_bars']
