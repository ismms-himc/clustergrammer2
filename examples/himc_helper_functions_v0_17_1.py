# Version: 0.17.1
# This is a set of scripts that are used in processing 10x single cell data
# improved dehsahing pipeline

import gzip
from scipy import io
from scipy.sparse import csc_matrix
from ast import literal_eval as make_tuple
import pandas as pd
import numpy as np
from copy import deepcopy
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import random
from functools import lru_cache

def get_version():
    print('0.17.1', 'two dimensional clustering bug fix')

def make_dir(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)

def load_crv3_feature_matrix(inst_path, to_csc=True, hto_list=None,
                             drop_default_lane=True, add_lane_to_barcodes=None, sp={}, df={}):

    # Read Barcodes
    ###########################
    filename = inst_path + 'barcodes.tsv.gz'
    f = gzip.open(filename, 'rt')
    lines = f.readlines()
    f.close()

    # if we are adding a lane, then we always want to drop the default cr lane
    if add_lane_to_barcodes is not None:
        drop_default_lane = True

    barcodes = []
    for inst_bc in lines:
        inst_bc = inst_bc.strip().split('\t')

        # remove dash from barcodes if necessary
        if drop_default_lane:
            if '-' in inst_bc[0]:
                inst_bc[0] = inst_bc[0].split('-')[0]


        barcodes.append(inst_bc[0])

    if add_lane_to_barcodes is not None:
        barcodes = [x + '-' + add_lane_to_barcodes for x in barcodes]

    # Load Matrix
    #################
    mat = io.mmread(inst_path + 'matrix.mtx.gz')
    mat_csr = mat.tocsr()

    # Get Indexes of Feature Types
    ##################################
    filename = inst_path + 'features.tsv.gz'
    f = gzip.open(filename, 'rt')
    lines = f.readlines()
    f.close()

    feature_indexes = {}
    feature_lines = {}

    for index in range(len(lines)):

        inst_line = lines[index].strip().split('\t')

        if len(inst_line) > 1:

            inst_feat = inst_line[2].replace('Gene Expression', 'gex')
            inst_feat = inst_feat.replace('Antibody Capture', 'adt').replace('Custom', 'custom')

            if hto_list is not None:
                if inst_feat == 'custom' or inst_feat == 'adt':
                    inst_feat = ('hto' if inst_line[0] in hto_list else 'adt')

            if inst_feat not in feature_indexes:
                feature_indexes[inst_feat] = []

            feature_indexes[inst_feat].append(index)

        else:
            inst_feat = 'gex'

            if inst_feat not in feature_indexes:
                feature_indexes[inst_feat] = []

            feature_indexes[inst_feat].append(index)

    inst_sp = {}

    for inst_feat in feature_indexes:
        inst_sp[inst_feat] = {}

        inst_sp[inst_feat]['barcodes'] = barcodes

        inst_indexes = feature_indexes[inst_feat]

        # Separate feature lists
        ser_lines = pd.Series(lines)
        ser_lines_found = ser_lines[inst_indexes]
        lines_found = list(ser_lines_found.array)

        # save feature lines
        feature_lines[inst_feat] = lines_found

        # save as compressed sparse column matrix (for barcode filtering)
        mat_filt = (mat_csr[inst_indexes, :].tocsc() if to_csc else mat_csr[inst_indexes, :])

        inst_sp[inst_feat]['mat'] = mat_filt

    # Make unique feature names
    for inst_feat in feature_lines:
        feat_lines = feature_lines[inst_feat]
        feat_lines = [x.strip().split('\t') for x in feat_lines]

        if len(feat_lines[0]) > 1:
            # find non-unique initial feature names (add id later if necessary)
            ini_names = [x[1] for x in feat_lines]

            ini_name_count = pd.Series(ini_names).value_counts()
            duplicate_names = ini_name_count[ini_name_count > 1].index.tolist()

            new_names = [x[1] if x[1] not in duplicate_names else x[1] + '_' + x[0] for x in feat_lines]
        else:
            new_names = [x[0] for x in feat_lines]

        # quick hack to clean up names
        new_names = [x.replace('_TotalSeqB', '') for x in new_names]

        inst_sp[inst_feat]['features'] = new_names

        # save feature lines
        if len(feat_lines[0]) > 1:
            cols = [inst_feat + '-ID', inst_feat + '-name', 'feature-type']
            df['meta_' + inst_feat] = pd.DataFrame(feat_lines, index=new_names, columns=cols)
        else:
            df['meta_' + inst_feat] = pd.DataFrame(feat_lines, index=new_names, columns=[inst_feat + '-ID'])

    sp['ini'] = inst_sp

    return sp, df

def load_crv2_gene_matrix(inst_path):
    '''
    Loads gene expression data from 10x in sparse matrix format and returns a
    Pandas dataframe
    '''

    import pandas as pd
    from scipy import io
    from scipy import sparse
    from ast import literal_eval as make_tuple

    # matrix
    mat = io.mmread( inst_path + 'matrix.mtx').tocsc()


    # genes
    filename = inst_path + 'genes.tsv'
    f = open(filename, 'r')
    lines_genes = f.readlines()
    f.close()

    # make unique gene names
    #############################
    gene_list = [x.strip().split('\t') for x in lines_genes]

    # find non-unique initial gene names
    ini_names = [x[1] for x in gene_list]

    ini_name_count = pd.Series(ini_names).value_counts()
    duplicate_names = ini_name_count[ini_name_count > 1].index.tolist()
    genes = [x[1] if x[1] not in duplicate_names else x[1] + '_' + x[0] for x in gene_list]


    # barcodes
    filename = inst_path + 'barcodes.tsv'
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    cell_barcodes = []
    for inst_bc in lines:
        inst_bc = inst_bc.strip().split('\t')

        # remove dash from barcodes if necessary
        if '-' in inst_bc[0]:
          inst_bc[0] = inst_bc[0].split('-')[0]

        cell_barcodes.append(inst_bc[0])

    # parse tuples if necessary
    try:
        cell_barcodes = [make_tuple(x) for x in cell_barcodes]
    except:
        pass

    try:
        genes = [make_tuple(x) for x in genes]
    except:
        pass

    # generate feature_data
    feature_data = {}
    feature_data['gex'] = {}
    feature_data['gex']['features'] = genes
    feature_data['gex']['barcodes'] = cell_barcodes
    feature_data['gex']['mat'] = mat

    return feature_data

def plot_metadata(meta_cell, metadata_type='gex-umi-sum', logy=True, logx=False, min_umi=0, max_umi=1e9, figsize=(10,5)):

    ser_meta = meta_cell[metadata_type]

    # filter
    ser_meta = ser_meta[ser_meta >= min_umi]
    ser_meta = ser_meta[ser_meta <= max_umi]
    ser_meta = ser_meta.sort_values(ascending=False)

    ser_meta.plot(logy=logy, logx=logx, figsize=figsize)

def plot_umi_levels(feature_data, feature_type='gex', logy=True, logx=False,
                    figsize=(10,5), min_umi=0, max_umi=1e9, zscore_features=False):
    '''
    This function takes a feature data format or dictionary of DataFrames and plots
    UMI levels
    '''

    if 'mat' in feature_data[feature_type]:
        mat_csc = feature_data[feature_type]['mat']

        if zscore_features:
            print('z-scoring feature_data')
            inst_df = pd.DataFrame(data=mat_csc.todense(), columns=feature_data[feature_type]['barcodes'])

            net.load_df(inst_df)
            net.normalize(axis='row', norm_type='zscore')
            inst_df = net.export_df()

            # sort
            ser_sum = inst_df.sum(axis=0).sort_values(ascending=False)

        else:
            # drop cells with fewer than threshold events
            ser_sum = mat_csc.sum(axis=0)
            arr_sum = np.asarray(ser_sum[0,:])

            # sort
            ser_sum = pd.Series(arr_sum[0], index=feature_data[feature_type]['barcodes']).sort_values(ascending=False)

        # filter
        ser_sum = ser_sum[ser_sum >= min_umi]
        ser_sum = ser_sum[ser_sum <= max_umi]

    else:
        inst_df = feature_data[feature_type]

        if zscore_features:
            print('zscore features')
            net.load_df(inst_df)
            net.normalize(axis='row', norm_type='zscore')
            inst_df = net.export_df()

        # sort
        ser_sum = inst_df.sum(axis=0).sort_values(ascending=False)

        # filter
        ser_sum = ser_sum[ser_sum >= min_umi]
        ser_sum = ser_sum[ser_sum <= max_umi]

    ser_sum.plot(logy=logy, logx=logx, figsize=figsize)
    return ser_sum

def filter_barcodes_by_umi(feature_data, feature_type, min_umi=0, max_umi=1e8,
                                      make_sparse=True, zscore_features=False):

    # feature data format
    ########################
    if 'mat' in feature_data[feature_type]:

        # sparse matrix
        ##################
        mat_csc = feature_data[feature_type]['mat']

        if zscore_features:
            print('*** warning, z-scoring not supported in feature_data format')

        # drop barcodes with fewer than threshold UMI
        ser_sum = mat_csc.sum(axis=0)
        arr_sum = np.asarray(ser_sum[0,:])
        ser_sum = pd.Series(arr_sum[0])
        ser_keep = ser_sum[ser_sum >= min_umi]
        ser_keep = ser_keep[ser_keep <= max_umi]

        # these indexes will be used to filter all features
        keep_indexes = ser_keep.index.tolist()

        # filter barcodes
        barcodes = feature_data[feature_type]['barcodes']
        ser_barcodes = pd.Series(barcodes)
        barcodes_filt = ser_barcodes[keep_indexes].get_values()

        # return Dictionary of DataFrames
        filtered_data = {}
        for inst_feat in feature_data:

            if 'meta' not in inst_feat:

                inst_mat = feature_data[inst_feat]['mat']
                mat_filt = inst_mat[:, keep_indexes]
                feature_names = feature_data[inst_feat]['features']

                inst_data = {}
                inst_data['mat'] = mat_filt
                inst_data['barcodes'] = barcodes_filt
                inst_data['features'] = feature_names

                filtered_data[inst_feat] = inst_data

    else:

        # dense matrix
        ###############
        # drop barcodes with fewer than threshold UMI
        inst_df = feature_data[feature_type]

        if zscore_features:
            print('z-scoring features')
            net.load_df(inst_df)
            net.normalize(axis='row', norm_type='zscore')
            inst_df = net.export_df()

        ser_sum = inst_df.sum(axis=0)
        ser_keep = ser_sum[ser_sum >= min_umi]
        ser_keep = ser_keep[ser_keep <= max_umi]
        keep_cols = ser_keep.index.tolist()

        # filter data
        filtered_data = {}
        for inst_feat in feature_data:

            filtered_data[inst_feat] = feature_data[inst_feat][keep_cols]

    return filtered_data

def convert_to_dense(feat_data, df=None):
    # initialize df if necessary
    if df is None:
        df = {}
    for inst_feat in feat_data:
        mat = feat_data[inst_feat]['mat']
        rows = feat_data[inst_feat]['features']
        cols = feat_data[inst_feat]['barcodes']

        dense_mat = mat.todense()
        df[inst_feat] = pd.DataFrame(dense_mat, index=rows, columns=cols)

    return df

def check_feature_data_size(feature_data):
    for inst_feat in feature_data:
        if 'meta' not in inst_feat:
            print(inst_feat)
            print(len(feature_data[inst_feat]['features']), len(feature_data[inst_feat]['barcodes']))
            print(feature_data[inst_feat]['mat'].shape, '\n')

def get_mito_genes(gene_list):
    # Removing Mitochondrial Genes
    ini_mito_list = ['MTRNR2L11', 'MTRF1', 'MTRNR2L12', 'MTRNR2L13', 'MTRF1L',
                     'MTRNR2L6', 'MTRNR2L7','MTRNR2L10', 'MTRNR2L8', 'MTRNR2L5',
                     'MTRNR2L1', 'MTRNR2L3', 'MTRNR2L4']

    list_mito_genes = list(map(lambda x:x.lower(), ini_mito_list))

    found_mito_genes = [x for x in gene_list if 'mt-' == x[:3].lower() or
                 x.split('_')[0].lower() in list_mito_genes]

    return found_mito_genes

def mito_prop_and_suspected_dead(df_gex, meta_cell, mito_thresh=0.9,
                                 plot_mito=True, s=5, alpha=0.2):

    print('find mito genes')
    all_genes = df_gex.index.tolist()
    mito_genes = get_mito_genes(all_genes)

    print('cacl mito sum')
    mito_sum = df_gex.loc[mito_genes].sum(axis=0)

    gex_sum = meta_cell['gex-umi-sum']

    mito_proportion = mito_sum/gex_sum

    print('assign live-dead')


    meta_cell['dead-cell-mito'] = mito_proportion.apply(lambda x: 'dead-cell' if x >= mito_thresh else 'live-cell')

    meta_cell['gex-mito-proportion-umi'] = mito_proportion

    if plot_mito:
        # mito_proportion.sort_values(ascending=False).plot()

        all_cells = meta_cell.index.tolist()
        color_list = ['red' if meta_cell.loc[x,'dead-cell-mito'] == 'dead-cell' else 'blue' for x in all_cells]

        meta_cell.plot(kind='scatter',
                       x='gex-umi-sum-ash',
                       y='gex-mito-proportion-umi',
                       alpha=alpha,
                       s=s,
                       figsize=(10,10),
                       c=color_list)

    ser_dead_counts = meta_cell['dead-cell-mito'].value_counts()
    print('live-cell', ser_dead_counts['live-cell'])
    if 'dead-cell' in ser_dead_counts:
        print('dead-cell', ser_dead_counts['dead-cell'])


    return meta_cell

def label_suspected_red_blood_cells(df, heme_genes=['HBA1', 'HBA2', 'HBB', 'HBD', 'HBQ1'],
                                    thresh=100,
                                    keep='below',
                                    x_max=1e4,
                                    y_max=1500):

    # Added HBD and HBQ based on HCA bone marrow signatures

    # save heme gene umi levels (no umi or ash normalization)
    heme_genes = [x for x in df['gex'].index.tolist() if x in heme_genes]
    ser_heme = df['gex'].loc[heme_genes].sum(axis=0)
    df['meta_cell']['heme-ab-umi'] = ser_heme


    keep_barcodes, drop_barcodes = one_dim_filter(df['meta_cell'],
                                                 name='heme-ab-umi',
                                                 thresh=thresh,
                                                 keep=keep,
                                                 x_max=x_max,
                                                 y_max=y_max)

    df['meta_cell'].loc[keep_barcodes, 'red-blood-cell'] = 'False'
    df['meta_cell'].loc[drop_barcodes, 'red-blood-cell'] = 'True'

def get_ig_genes(genes):
    ig_genes = [x for x in genes if x[:2] == 'IG']
    return ig_genes

def set_hto_thresh(df_hto_ash, meta_hto, hto_name, scale_factor, thresh=1, xlim=7, ylim =100):

    ser_hto = deepcopy(df_hto_ash.loc[hto_name]) * (1/scale_factor)

    n, bins, patches = plt.hist(ser_hto, bins=100, range=(0, xlim))

    colors = []
    for inst_bin in bins:
        if inst_bin <= thresh:
            colors.append('red')
        else:
            colors.append('blue')

    # apply the same color for each class to match the map
    for patch, color in zip(patches, colors):
        patch.set_facecolor(color)

    # hto threshold after arcsinh, and scale
    meta_hto.loc[hto_name, 'hto-threshold-ash-scale'] = thresh
    # hto threshold after arcinh
    meta_hto.loc[hto_name, 'hto-threshold-ash'] = thresh * scale_factor
    # hto threshold in umi level
    meta_hto.loc[hto_name, 'hto-threshold-umi'] = np.sinh(thresh * scale_factor) * 5

    # save scale factor (to align peaks of HTO histograms)
    meta_hto.loc[hto_name, 'scale-factor'] = scale_factor

    plt.ylim((0,ylim))

def ini_meta_cell(df):
    list_ser = []

    # look for available data types
    found_types = list(set(['gex', 'adt', 'hto']).intersection(df.keys()))
    for inst_type in found_types:

        # calc umi sum
        inst_ser = df[inst_type].sum(axis=0)
        inst_ser.name = inst_type + '-umi-sum'

        list_ser.append(inst_ser)

    df['meta_cell'] = pd.DataFrame(data=list_ser).transpose()
    if 'gex' in df.keys():
        df_gex = deepcopy(df['gex'])
        df_gex[df_gex >= 1] = 1
        ser_gene_num = df_gex.sum(axis=0)
        df['meta_cell']['num_expressed_genes'] = ser_gene_num
    return df

def meta_cell_gex_wo_mito_ribo(df_gex_ini, meta_cell):

    df_gex = deepcopy(df_gex_ini)

    # calc umi sum
    ser_umi_sum = df_gex.sum(axis=0)

    meta_cell['gex-umi-sum-no-ribo-mito'] = ser_umi_sum

    # count number of measured genes

    df_gex[df_gex >= 1] = 1
    ser_gene_num = df_gex.sum(axis=0)

    meta_cell['num_expressed_genes_no-ribo-mito'] = ser_gene_num

    return meta_cell

def ini_meta_gene(df_gex_ini):

    df_gex = deepcopy(df_gex_ini)

    # Mean UMI
    ser_gene_mean = df_gex.mean(axis=1)
    ser_gene_mean.name = 'mean'

    # Variance UMI
    ser_gene_var = df_gex.mean(axis=1)
    ser_gene_var.name = 'variance'

    # fraction of cells measured
    df_gex[df_gex >= 1] = 1
    ser_gene_meas = df_gex.sum(axis=1)/df_gex.shape[1]
    ser_gene_meas.name = 'fraction of cells measured'

    meta_gene = pd.concat([ser_gene_mean, ser_gene_var, ser_gene_meas], axis=1)

    return meta_gene



def plot_signal_vs_noise(df, alpha=0.25, s=10, hto_range=7, inf_replace=1000):

    fig, axes = plt.subplots(nrows=1, ncols=2)

    list_first = []
    list_second = []
    list_cells = []
    for inst_cell in df.columns.tolist():
        inst_ser = df[inst_cell].sort_values(ascending=False)
        inst_first  = inst_ser.get_values()[0]
        inst_second = inst_ser.get_values()[1]

        list_first.append(inst_first)
        list_second.append(inst_second)
        list_cells.append(inst_cell)

    ser_first  = pd.Series(data=list_first,  index=list_cells, name='first highest HTO')
    ser_second = pd.Series(data=list_second, index=list_cells, name='second highest HTO')

    df_comp = pd.concat([ser_first, ser_second], axis=1).transpose()

    df_comp.transpose().plot(kind='scatter', figsize=(5,5),
                             x='first highest HTO', y='second highest HTO',
                             ylim=(0,hto_range), xlim=(0,hto_range), alpha=alpha, s=s, ax=axes[0])

    sn_ratio = np.log2(df_comp.loc['first highest HTO']/df_comp.loc['second highest HTO'])


    # replace positive infinities with set value
    sn_ratio = sn_ratio.replace(np.Inf, inf_replace)
    sn_ratio.hist(bins=100, ax=axes[1], figsize=(15,7))

    return df_comp, sn_ratio

def filter_ribo_mito_from_gex(df):

    # save avg values to meta_cell
    if 'gex-mito-avg' not in df['meta_cell']:

        df_gex = deepcopy(df['gex'])
        meta_cell = deepcopy(df['meta_cell'])

        all_genes = df_gex.index.tolist()

        ini_genes = deepcopy(all_genes)

        ribo_rpl = [x for x in all_genes if x.lower().startswith('rpl')]
        ribo_rps = [x for x in all_genes if x.lower().startswith('rps')]
        ribo_genes = ribo_rpl + ribo_rps

        # calculate average ribo gene expression
        ser_ribo = df_gex.loc[ribo_genes].mean(axis=0)

        keep_genes = [x for x in all_genes if x not in ribo_genes]

        df_gex = df_gex.loc[keep_genes]

        all_genes = df_gex.index.tolist()

        mito_genes = get_mito_genes(all_genes)

        # calculate average mito gene expression
        ser_mito = df_gex.loc[mito_genes].mean(axis=0)

        keep_genes = [x for x in all_genes if x not in mito_genes]

        # save mito and ribo genes
        mr_genes = sorted(list(set(ini_genes).difference(keep_genes)))
        df_mr = df['gex'].loc[mr_genes]

        # drop mito and ribo genes
        df_gex = df['gex'].loc[keep_genes]

        meta_cell['gex-ribo-avg'] = ser_ribo
        meta_cell['gex-mito-avg'] = ser_mito

        df['gex'] = df_gex
        df['meta_cell'] = meta_cell
        df['gex-mr'] = df_mr
    else:
        print('already filtered mito and ribo genes')

    return df


def add_cats_from_meta(barcodes, df_meta, add_cat_list):
    '''
    Add categories from df_meta.
    '''

    # get metadata of interest (add_cat_list) from barcodes of interest
    df_cats = df_meta.loc[barcodes][add_cat_list]

    # get list of cats
    list_cat_ini = [list(x) for x in df_cats.values]

    # add titles to cats
    list_cat_titles = [ list([str(x) + ': ' + str(y) for x,y in zip(add_cat_list, a)]) for a in list_cat_ini]

    # add barcodes to new columns
    new_cols = [tuple([x] + y) for x,y in zip(barcodes, list_cat_titles)]

    return new_cols


def make_cyto_export(df, num_var_genes=500, inf_replace=10):

    keep_meta_base = ['gex-umi-sum',
                      'gex-num-unique',
                      'gex-mito-proportion-umi',
                      'gex-mito-avg',
                      'gex-ribo-avg',
                      'hto-umi-sum',
                      'hto-sn',
                      'adt-umi-sum'
                      ]

    df_cyto = None

    for inst_type in ['gex', 'adt', 'hto', 'meta_cell']:
        if inst_type in df.keys():
            inst_df = deepcopy(df[inst_type])

            # filter for top var genes
            if inst_type == 'gex':
                keep_var_genes = inst_df.var(axis=1).sort_values(ascending=False).index.tolist()[:num_var_genes]

                inst_df = inst_df.loc[keep_var_genes]

            if 'meta' not in inst_type:
                inst_df.index = [inst_type.upper() + '_' + x for x in inst_df.index.tolist()]

            else:
                keep_meta = [metadata for metadata in keep_meta_base if metadata in inst_df.columns]
                inst_df = inst_df[keep_meta].transpose()
                inst_df.index = [ x.split('-')[0].upper() + '_der_' +
                                 '_'.join( x.split('-')[1:]).replace('num_unique', 'unique_gene_count')
                                 for x in inst_df.index.tolist()]

            print(inst_type, inst_df.shape)

            if df_cyto is None:
                df_cyto = inst_df
            else:
                df_cyto = df_cyto.append(inst_df)

    df_export = df_cyto.transpose()

    cells = df_export.index.tolist()
    index_cells = [str(x/100) for x in range(len(cells))]
    df_export.index = index_cells

    # Add noise
    data_columns = [x for x in df_export.columns if '_der_' not in x]

    not_derived_dataframe_shape = df_export[data_columns].shape

    # center the noise about zero
    rand_mat = np.random.rand(not_derived_dataframe_shape[0], not_derived_dataframe_shape[1]) - 0.5

    df_noise = pd.DataFrame(data=rand_mat, index=index_cells, columns=data_columns).round(2)
    df_export[data_columns] += df_noise

    ser_index = pd.Series(data=index_cells, index=cells)
    df['meta_cell']['Cytobank-Index'] = ser_index

    df_export.index.name = 'cell_index'

    # replace inf and nans
    df_export[df_export == np.inf] = inf_replace
    df_export.fillna(0, inplace=True)


    df['cyto-export'] = df_export

    return df

# # alternate lambda function
# def sum_field(dataframe, field):
#     return dataframe[field].sum(axis=0)

# list_ser_functions = {**{inst_type+'-umi-sum':(lambda y,inst_type=inst_type: sum_field(y,inst_type))\
#                          for inst_type in ['gex', 'adt', 'hto']},
#                      }

# for key,value in list_ser_functions.items():
#     list_ser.append(value(df))
# df['meta_cell'] = pd.DataFrame(data=list_ser).transpose()


def load_prod_vdj(inst_path):
    inst_df = pd.read_csv(inst_path)
    print('all contigs', inst_df.shape)
    ser_prod = inst_df['productive']

    keep_contigs = ser_prod[ser_prod == True].index.tolist()
    inst_df = inst_df.loc[keep_contigs]
    print('productive contigs', inst_df.shape)
    return inst_df

def concat_contig(ser_row):
    inst_v = str(ser_row['v_gene'])
    inst_d = str(ser_row['d_gene'])
    inst_j = str(ser_row['j_gene'])
    inst_c = str(ser_row['c_gene'])
    inst_cdr3 = str(ser_row['cdr3'])

    # do not include c gene in clonotype definition (do not include c_gene)
    inst_contig = inst_v + '_' + inst_d + '_' + inst_j + '_' + inst_cdr3

    return inst_contig

def get_unique_contigs(inst_df):
    '''
    Define contigs as the merge of v, d, j, and cdr3 genes
    Then, find all unique contigs.
    '''
    all_contigs = []
    for inst_index in inst_df.index.tolist():
        ser_row = inst_df.loc[inst_index]
        inst_contig = concat_contig(ser_row)
        all_contigs.append(inst_contig)
    unique_contigs = sorted(list(set(all_contigs)))
    return unique_contigs

def assign_ids_to_contigs(unique_contigs):
    '''
    Generate a unique contig id for all contigs
    return dictionary of contig-to-id and vice versa
    '''
    contig_id_dict = {}
    id_contig_dict = {}
    for inst_index in range(len(unique_contigs)):
        inst_id = 'contig-id-' + str(inst_index)
        inst_contig = unique_contigs[inst_index]
        contig_id_dict[inst_contig] = inst_id
        id_contig_dict[inst_id] = inst_contig

    return contig_id_dict, id_contig_dict

def get_bc_contig_combos(inst_df, contig_id_dict):
    '''
    Loop through the merged (across samples) filtered contigs
    which has one row per contig

    Define the contig (concat vdj genes) and find its unique id
    using contig_id_dict

    Assemble list of contigs associated with each barcode (dict
    with barcode keys)
    '''
    bc_contig_combos = {}
    for inst_row in inst_df.index.tolist():
        ser_row = inst_df.loc[inst_row]
        inst_bc = ser_row['barcode']
        inst_contig = concat_contig(ser_row)
        inst_id = contig_id_dict[inst_contig]

        if inst_bc not in bc_contig_combos:
            bc_contig_combos[inst_bc] = []

        bc_contig_combos[inst_bc].append(inst_id)

    return bc_contig_combos

def generate_new_clonotypes(bc_contig_combos):
    '''
    Define contig combinations as a new set of clones
    Number the new clones (rank by abundance)

    Look up contig combo for each barcode (e.g. clone)
    Look up new clone name for contig comb
    '''

    # find most abundant contig combos (clones)
    contig_id_combos = []
    for inst_bc in bc_contig_combos:
        inst_combo = '_'.join(sorted(bc_contig_combos[inst_bc]))
        contig_id_combos.append(inst_combo)
    ser_combos = pd.Series(contig_id_combos).value_counts()

    # number new clones (contig combos) based on abundance
    inst_id = 1
    combo_clone_dict = {}
    for inst_combo in ser_combos.index.tolist():
        new_clone_name = 'custom-clone-' + str(inst_id)
        combo_clone_dict[inst_combo] = new_clone_name
        inst_id = inst_id + 1

    # make dictionary of new clones for each barcode
    cell_new_clone = {}
    for inst_bc in bc_contig_combos:
        inst_combo = '_'.join(sorted(bc_contig_combos[inst_bc]))
        new_clone = combo_clone_dict[inst_combo]
        cell_new_clone[inst_bc] = new_clone

    return cell_new_clone

def add_uniform_noise(df_ini):
    df = deepcopy(df_ini)
    rows = df.index.tolist()
    cols = df.columns.tolist()

    # generate random matrix
    np.random.seed(99)
    num_rows = df.shape[0]
    num_cols = df.shape[1]
    mat = np.random.rand(num_rows, num_cols)

    # make random noise dataframe centered about zero
    df_noise = pd.DataFrame(data=mat, columns=cols, index=rows).round(2) - 0.5

    df_new = df + df_noise

    return df_new

def filter_sparse_matrix_by_list(feat, feature_type='gex', keep_rows='all', keep_cols='all'):
    '''
    This function filters sparse data by lists of rows/cols.
    '''

    feat_filt = deepcopy(feat)

    # get all cols from any feature
    tmp_feat = list(feat_filt.keys())[0]
    cols = feat_filt[tmp_feat]['barcodes']

    # Feature (row) Level Filtering
    #################################
    # apply to single feature
    if isinstance(keep_rows, list):

        # get initial feature list
        rows_orig = feat_filt[feature_type]['features']

        index_dict = dict((value, idx) for idx,value in enumerate(rows_orig))
        rows_idx = [index_dict[x] for x in keep_rows]

        # copy feature data of interest
        inst_mat = deepcopy(feat_filt[feature_type]['mat'])
        inst_mat = inst_mat[rows_idx,:]

        # filter rows for single feature
        feat_filt[feature_type]['barcodes'] = cols
        feat_filt[feature_type]['features'] = keep_rows
        feat_filt[feature_type]['mat'] = inst_mat

    # Cell (col) Level Filtering
    #################################
    # apply to all features
    if isinstance(keep_cols, list):

        index_dict = dict((value, idx) for idx,value in enumerate(cols))
        cols_idx = [index_dict[x] for x in keep_cols]

        # filter all features by columns
        for inst_feat in feat:

            # get initial feature list
            rows_orig = feat_filt[inst_feat]['features']

            inst_mat = deepcopy(feat_filt[inst_feat]['mat'])
            inst_mat = inst_mat[:,cols_idx]

            # filter single feature by columns
            feat_filt[inst_feat]['barcodes'] = keep_cols
            feat_filt[inst_feat]['features'] = rows_orig
            feat_filt[inst_feat]['mat'] = inst_mat

    return feat_filt

def preserve_genes_most_variant(input_df, genes_most_variant=500):
    gene_variance = (input_df['gex']['mat'].power(2)).mean(1) - (
        np.power(input_df['gex']['mat'].mean(1), 2))
    gene_variance_sorted = sorted([(index, variance) for index, variance in enumerate(gene_variance)],
                                  key=(lambda x: x[1]), reverse=True)
    feature_data_gene_variance_filtered = filter_sparse_matrix_by_list(input_df,
                                                                          feature_type='gex',
                                                                          keep_rows=[input_df['gex'][
                                                                                         'features'][
                                                                                         each_gene_variance[0]] for
                                                                                     each_gene_variance in
                                                                                     gene_variance_sorted[
                                                                                     :genes_most_variant]])

    return feature_data_gene_variance_filtered

def filter_ribo_mito_from_list(all_genes):

    # find ribosomal genes
    ribo_rpl = [x for x in all_genes if 'RPL' in x]
    ribo_rps = [x for x in all_genes if 'RPS' in x]
    ribo_genes = ribo_rpl + ribo_rps


    # Find mitochondrial genes
    list_mito_genes = ['MTRNR2L11', 'MTRF1', 'MTRNR2L12', 'MTRNR2L13', 'MTRF1L', 'MTRNR2L6', 'MTRNR2L7',
                    'MTRNR2L10', 'MTRNR2L8', 'MTRNR2L5', 'MTRNR2L1', 'MTRNR2L3', 'MTRNR2L4']

    mito_genes = [x for x in all_genes if 'MT-' == x[:3] or
                 x.split('_')[0] in list_mito_genes]


    # filter genes
    keep_genes = [x for x in all_genes if x not in ribo_genes]
    keep_genes = [x for x in keep_genes if x not in mito_genes]

    return keep_genes


def calc_feat_sum_and_unique_count_across_cells(feat_data, inst_feat):
    # barcodes = (feat_data[inst_feat]['barcodes'] if 'barcodes' in feat_data[inst_feat].keys() else feat_data[inst_feat].columns)
    barcodes = feat_data[inst_feat]['barcodes']
    mat = deepcopy(feat_data[inst_feat]['mat'])

    # sum umi of measured features
    arr_sum = np.asarray(mat.sum(axis=0))[0]
    ser_sum = pd.Series(arr_sum, index=barcodes, name=inst_feat + '-umi-sum')

    # save ash version of umi sum
    ser_sum_ash = np.arcsinh(ser_sum/5)
    ser_sum_ash.name = inst_feat + '-umi-sum-ash'

    # count number of measured features
    mat[mat > 1] = 1
    arr_count = np.asarray(mat.sum(axis=0))[0]
    ser_count = pd.Series(arr_count, index=barcodes, name=inst_feat + '-num-unique')

    inst_df = pd.concat([ser_sum, ser_sum_ash, ser_count], axis=1)

    return inst_df


def sample_meta(df_meta_ini, sample_name):
    list_index = []
    list_data = []

    df_meta = deepcopy(df_meta_ini)

    # proprtion of singlets
    #########################
    ser_cell_per = df_meta['cell-per-bead'].value_counts()

    num_singlets = ser_cell_per.loc['singlet']
    num_total = ser_cell_per.sum()

    # number of singlets
    list_index.append('number-singlets')
    list_data.append(num_singlets)

    # get singlets only
    df_meta = df_meta[df_meta['cell-per-bead'] == 'singlet']

    # proportion of dead cells
    ##############################
    ser_dead = df_meta['dead-cell-mito'].value_counts()
    prop_dead = 1 - ser_dead['live-cell'] / ser_dead.sum()

    list_index.append('proportion-dead')
    list_data.append(prop_dead)

    # assemble initial metadata series
    ser_meta_ini = pd.Series(list_data, index=list_index)

    # Calculate average metadata
    meta_list = ['gex-umi-sum', 'gex-num-unique', 'gex-mito-proportion-umi', 'gex-ribo-avg', 'gex-mito-avg']
    ser_meta_mean = df_meta[meta_list].mean()

    ser_meta_mean.index = [x + '-mean' for x in ser_meta_mean.index.tolist()]

    ser_meta = pd.concat([ser_meta_ini, ser_meta_mean])
    ser_meta.name = sample_name

    return ser_meta

def merge_lanes(lane_dirs, merge_dir, data_types=['gex', 'adt', 'hto', 'meta_cell'],
    return_df=True):

    lane_dirs = sorted(lane_dirs)

    if return_df:
        df = {}

    for inst_type in data_types:

        df_merge = None

        print('\n' + inst_type + '\n----------------')

        # collect data
        for inst_dir in lane_dirs:

            inst_lane = inst_dir.split('/')[-1]
            inst_file = inst_dir + '/' + inst_type + '.parquet'
            if os.path.exists(inst_file):

                inst_df = pd.read_parquet(inst_file)

                # if meta add lane category
                if 'meta' in inst_type:
                    ser_lane = pd.Series(data=inst_lane, index=inst_df.index.tolist())
                    inst_df['Lane_10x'] = ser_lane

                print(inst_lane, inst_df.shape)

                # merge on the fly
                if df_merge is None:
                    df_merge = deepcopy(inst_df)
                else:
                    if 'meta' in inst_type:
                        df_merge = pd.concat([df_merge, inst_df], axis=0, sort=True)
                    else:
                        df_merge = pd.concat([df_merge, inst_df], axis=1)
                print('df_merge', df_merge.shape)

        print('merged', inst_type, df_merge.shape)

        # sort columns and rows
        cols = sorted(df_merge.columns.tolist())
        rows = sorted(df_merge.index.tolist())
        df_merge = df_merge.loc[rows, cols]

        df_merge.to_parquet(merge_dir + '/' + inst_type + '.parquet')

        if return_df:
            # save to dictionary
            df[inst_type] = df_merge

    if return_df:
        return df

def load_kb_vel_feature_matrix(inst_path, inst_sample, to_csc=True):

    # Load barcodes
    #################
    filename = inst_path + inst_sample + '.barcodes.txt'
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    barcodes = []
    for inst_bc in lines:
        inst_bc = inst_bc.strip().split('\t')

        barcodes.append(inst_bc[0])


    # Load genes
    #################
    filename = inst_path + inst_sample + '.genes.txt'
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    genes = []
    for inst_gene in lines:
        inst_gene = inst_gene.strip().split('\t')

        genes.append(inst_gene[0])

    # Load Matrix
    #################
    mat = io.mmread(inst_path + inst_sample +'.mtx').transpose()
    mat = mat.tocsc()

    print(len(genes), len(barcodes), mat.shape)

    feature_data = {}
    feature_data['gex'] = {}
    feature_data['gex']['mat'] = mat
    feature_data['gex']['features'] = genes
    feature_data['gex']['barcodes'] = barcodes

    return feature_data

def find_suspected_adt_multiplets(adt_name, df, thresh=0.75, num_pos_marker_multiplet=30, find_debris=False,
                                 x_max=25, y_max=3000):
    '''
    This function identifies susspected ADT multiplets based on the ditribution of the
    number of markers a cell is 'positive' for. Positive is defined as above a certain
    threshold. adt_name defines what adt dataset should be used for this function and
    is usually a z-scored filtered ADT dataset. We can toggle whether we will identify debris.
    '''

    df_adt = df[adt_name]

    # binarize
    df_bin = deepcopy(df_adt)
    df_bin[df_bin < thresh] = 0
    df_bin[df_bin >= thresh] = 1

    sum_bin = df_bin.sum(axis=0)

    found_debris = sum_bin[sum_bin == 0].index.tolist()
    found_multi  = sum_bin[sum_bin >= num_pos_marker_multiplet].index.tolist()
    drop_cells = found_debris + found_multi
    if find_debris:
        print('debris', len(found_debris))
    print('multiplet', len(found_multi))

    drop_dict = {}
    list_cell_per_event = []
    for inst_cell in df_bin.columns.tolist():

        if inst_cell in found_multi:
            inst_type = 'multiplet'
        else:
            inst_type = 'singlet'

        if find_debris:
            if inst_cell in found_debris:
                inst_type = 'debris'

        list_cell_per_event.append(inst_type)

    ser_cell_per_bead = pd.Series(list_cell_per_event, index=df_bin.columns.tolist())


    df['meta_cell']['adt-cell-per-bead'] = ser_cell_per_bead
    df['meta_cell']['adt-num-positive'] = sum_bin

    # plot distribution
    keep_adt_positive = one_dim_filter(df['meta_cell'],
                                      name='adt-num-positive',
                                      thresh=num_pos_marker_multiplet,
                                      x_max=x_max, y_max=y_max, keep='below')

    return df

def two_dim_filter(df_data_ini, x_name, y_name, x_thresh=None, y_thresh=None, x_keep='above', y_keep='above', plot_num_cells='all', x_max=None, y_max=None, is_meta=True,
                   title=None):

    '''
    Working on generalizing function for two dimensional gating from metadata and any other data source.
    '''

    if title is None:
        title = ''


    if is_meta == True:
        df_data = df_data_ini
    else:
        df_data = deepcopy(df_data_ini.transpose())

    # auto set x and y thresholds
    if x_max is None:
        if 'ash' in x_name:
            x_max = 10
        else:
            x_max = 100

    if y_max is None:
        if 'ash' in y_name:
            y_max = 10
        else:
            y_max = 100


    # convert to non-ash values for interpretation
    if 'ash' in x_name:
        x_thresh_umi = np.sinh(x_thresh) * 5
    else:
        x_thresh_umi = None

    if 'ash' in y_name:
        y_thresh_umi = np.sinh(y_thresh) * 5
    else:
        y_thresh_umi = None


    # initialize everything to red (what will be dropped, debris)
    ser_colors = pd.Series('red', index=df_data.index.tolist())

    color_list = []
    ser_x = df_data[x_name]
    if x_keep == 'above':
        x_pass = ser_x[ser_x >= x_thresh].index.tolist()
    elif x_keep == 'below':
        x_pass = ser_x[ser_x < x_thresh].index.tolist()

    ser_y = df_data[y_name]
    if y_keep == 'above':
        y_pass = ser_y[ser_y >= y_thresh].index.tolist()
    elif y_keep == 'below':
        y_pass = ser_y[ser_y < y_thresh].index.tolist()

    if 'ash' in x_name:
        print(x_name, ' thresh ash: ', x_thresh, ' UMI: ', x_thresh_umi.round(0))
    else:
        print(x_name, ' thresh: ', x_thresh)

    if 'ash' in y_name:
        print(y_name, ' thresh ash: ', y_thresh, ' UMI: ', y_thresh_umi.round(0))
    else:
        print(y_name, ' thresh: ', y_thresh)


    print(x_name, ' keep: ', len(x_pass))
    print(y_name, ' keep: ', len(y_pass))

    keep_barcodes = list(set(x_pass + y_pass))
    print('keep_barcodes: ', len(keep_barcodes))

    ser_colors[keep_barcodes] = 'blue'

    # only include top 100K cells
    if plot_num_cells == 'all':
        plot_cells = df_data.index.tolist()
    else:
        plot_cells = df_data[x_name].sort_values(ascending=False).index.tolist()[:int(plot_num_cells)]

    ser_colors = ser_colors[plot_cells]

    color_list = ser_colors.get_values()

    df_data.loc[plot_cells].plot(kind='scatter', x=x_name, y=y_name,
                         s=1, alpha=0.5, figsize=(10,10),
                         ylim=(0,y_max), xlim=(0,x_max), c=color_list, title=title)

    drop_barcodes = sorted(list(set(df_data.index.tolist()).difference(keep_barcodes)))

    return keep_barcodes, drop_barcodes

def make_ct_list(df_hto, meta_hto):
    '''assign cells to debris/singlet/multiplet based on threshold only (hto-ash-scale)'''

    ser_list = []

    for inst_row in df_hto.index.tolist():

        # get data for a HTO
        inst_ser = deepcopy(df_hto.loc[inst_row])

        # load threshold level for this HTO
        inst_thresh = meta_hto.loc[inst_row, 'hto-threshold-ash-scale']

        # binarize HTO values about threshold
        inst_ser[inst_ser < inst_thresh] = 0
        inst_ser[inst_ser >= inst_thresh] = 1

        # assemble list of series to make dataframe later
        ser_list.append(inst_ser)

        # find cells that are positive for this HTO
        pos_hto = inst_ser[inst_ser==1].index.tolist()

    # generate binarized dataframe
    df_binary = pd.concat(ser_list, axis=1).transpose()

    # find singlets
    ser_sum = df_binary.sum(axis=0)
    ct_list = {}
    ct_list['debris']    = ser_sum[ser_sum == 0].index.tolist()
    ct_list['singlet']   = ser_sum[ser_sum == 1].index.tolist()
    ct_list['multiplet'] = ser_sum[ser_sum > 1].index.tolist()

    return ct_list

def calc_s2n_and_s2t(df_hto, meta_hto, meta_cell, inf_replace):

    # signal-to-noise refers to the highest vs second highest HTO
    #
    # signal-to-threshold refers to the highest HTO vs the
    # manually set threshold for that HTO

    # do not use ash data, calc signal to noise on HTO UMI data
    # find the highest hto
    ser_max_hto = df_hto.idxmax(axis=0)
    meta_cell['hto-max-name'] = ser_max_hto

    list_first = []
    list_second = []
    list_thresh = []
    list_cells = []

    for inst_cell in df_hto.columns.tolist():
        inst_ser = df_hto[inst_cell].sort_values(ascending=False)
        inst_first  = inst_ser.array[0]
        inst_second = inst_ser.array[1]


        inst_max_hto_name = ser_max_hto[inst_cell]
        inst_max_hto_thresh = meta_hto['hto-threshold-ash-scale'][inst_max_hto_name]

        list_first.append(inst_first)
        list_second.append(inst_second)
        list_thresh.append(inst_max_hto_thresh)
        list_cells.append(inst_cell)

    ser_first  = pd.Series(data=list_first,  index=list_cells, name='first highest HTO')
    ser_second = pd.Series(data=list_second, index=list_cells, name='second highest HTO')
    ser_thresh = pd.Series(data=list_thresh, index=list_cells, name='threshold HTO')

    # df_comp = pd.concat([ser_first, ser_second, ser_thresh], axis=1).transpose()

    meta_cell['hto-max-umi-ash-scale'] = ser_first

    # calc signal-to-noise
    ###########################
    # sn_ratio = df_comp.loc['first highest HTO']/df_comp.loc['second highest HTO']
    sn_ratio = ser_first/ser_second
    meta_cell['hto-sn'] = sn_ratio
    # replace infinities with large number
    sn_ratio = sn_ratio.replace(np.Inf, inf_replace)

    # calc signal-to-threshold
    ###########################
    # sn_ratio = df_comp.loc['first highest HTO']/df_comp.loc['threshold HTO']
    st_ratio = ser_first/ser_thresh
    meta_cell['hto-st'] = st_ratio
    # replace infinities with large number
    st_ratio = st_ratio.replace(np.Inf, inf_replace)

    return meta_cell

def assign_htos(df_hto, meta_hto, meta_cell, sn_thresh, inf_replace=1000, perform_sn_adjustment=True):

    # assign cells to debris/singlet/multiplet based on threshold only (ash normalized)
    ######################################################################################
    ct_list = make_ct_list(df_hto, meta_hto)

    print('De-hash distributions: HTO Threshold Only')
    print('-----------------------------------------')
    print('debris', len(ct_list['debris']))
    print('singlet', len(ct_list['singlet']))
    print('multiplet', len(ct_list['multiplet']))

    # initialize dehash-thresh: debris/singlet/multiplet based on ct_list
    if 'dehash-thresh' not in meta_cell.columns.tolist():
        ser_type = pd.Series(np.nan, index=meta_cell.index)
        meta_cell['dehash-thresh'] = ser_type

    # save dehash-thresh
    ######################
    for inst_type in ct_list:
        meta_cell.loc[ct_list[inst_type], 'dehash-thresh'] = inst_type

    # Calc signal-to-noise and signal-to-threshold ratios
    ######################################################
    meta_cell = calc_s2n_and_s2t(df_hto, meta_hto, meta_cell, inf_replace)

    # Assign Cells to Samples based on Threshold Alone
    ####################################################
    list_samples = []
    for inst_cell in meta_cell.index.tolist():

        inst_type = meta_cell.loc[inst_cell, 'dehash-thresh']

        if inst_type == 'singlet':
            inst_hto = meta_cell.loc[inst_cell, 'hto-max-name']
            inst_sample = meta_hto.loc[inst_hto]['Associated Sample']
        else:
            inst_sample = 'N.A.'

        list_samples.append(inst_sample)

    ser_sample = pd.Series(list_samples, index=meta_cell.index.tolist())
    meta_cell['Sample-thresh'] = ser_sample

    if perform_sn_adjustment:
        # Assign Cells to Samples Based on Signal to Noise Adjustment
        cells = meta_cell.index.tolist()
        for inst_cell in cells:
            inst_type = meta_cell.loc[inst_cell, 'dehash-thresh']
            inst_sn = meta_cell.loc[inst_cell, 'hto-sn']
            inst_max_hto = meta_cell.loc[inst_cell, 'hto-max-name']

            # change singlet to multiplet if low sn
            if inst_type == 'singlet':
                if inst_sn < sn_thresh['singlets']:
                    # convert to multiplet
                    meta_cell.loc[inst_cell, 'dehash-thresh-sn'] = 'multiplet'
                    meta_cell.loc[inst_cell, 'Sample-thresh-sn'] = 'N.A.'
                else:
                    meta_cell.loc[inst_cell, 'dehash-thresh-sn'] = 'singlet'
                    meta_cell.loc[inst_cell, 'Sample-thresh-sn'] = meta_hto.loc[inst_max_hto]['Associated Sample']
            elif inst_type == 'debris':
                if inst_sn >= sn_thresh['debris']:
                    meta_cell.loc[inst_cell, 'dehash-thresh-sn'] = 'singlet'
                    meta_cell.loc[inst_cell, 'Sample-thresh-sn'] = meta_hto.loc[inst_max_hto]['Associated Sample']
                else:
                    meta_cell.loc[inst_cell, 'dehash-thresh-sn'] = 'debris'
                    meta_cell.loc[inst_cell, 'Sample-thresh-sn'] = 'N.A.'
            elif inst_type == 'multiplet':
                if inst_sn >= sn_thresh['multiplets']:
                    meta_cell.loc[inst_cell, 'dehash-thresh-sn'] = 'singlet'
                    meta_cell.loc[inst_cell, 'Sample-thresh-sn'] = meta_hto.loc[inst_max_hto]['Associated Sample']
                else:
                    meta_cell.loc[inst_cell, 'dehash-thresh-sn'] = 'multiplet'
                    meta_cell.loc[inst_cell, 'Sample-thresh-sn'] = 'N.A.'


        ser_counts = meta_cell['dehash-thresh-sn'].value_counts()

        print('De-hash distributions: HTO Threshold and SN')
        print('--------------------------------------------')
        print('debris', ser_counts['debris'])
        print('singlet', ser_counts['singlet'])
        print('multiplet', ser_counts['multiplet'])

    return meta_cell

def plot_hto_sn_vs_gex_umi(df):

    if 'hto-sn-ash' not in df['meta_cell']:
        df['meta_cell']['hto-sn-ash'] = np.arcsinh(df['meta_cell']['hto-sn']/5)

    color_dict = {
        "singlet":'blue',
        "debris":'red',
        "multiplet":'yellow',
    }

    list_dehash = list(df['meta_cell']['cell-per-bead'].get_values())
    color_list = [color_dict[x] for x in list_dehash]

    df['meta_cell'].plot(kind='scatter',
                         x='gex-umi-sum-ash',
                         y='hto-sn-ash', alpha=0.25, s=10, figsize=(10,10), c=color_list, ylim=(0,5))

def load_s3_parquet(bucket_path, filename, cols=None):

    import s3fs
    import pyarrow.parquet as pq
    fs = s3fs.S3FileSystem()

    if cols == None:
        df = pq.read_table(bucket_path + filename, use_pandas_metadata=True, filesystem=fs).to_pandas()
    else:
        df = pq.read_table(bucket_path + filename, use_pandas_metadata=True, filesystem=fs, columns=cols).to_pandas()

    return df

def add_filter(cat_title, inst_cat_search, cat_filter_list=None):
    '''
    Add a single filtering step; e.g. filter for barcodes with
    this category of this category type.

    To do: support exclusion of category by adding third element to tuple.
    '''
    if cat_filter_list == None:
        cat_filter_list = []

    if type(inst_cat_search) is list:
        inst_cat_search = tuple(inst_cat_search)

    cat_filter_list.append((cat_title, inst_cat_search))
    return cat_filter_list

def filter_meta_using_cat_filter_list(df_meta_ini, cat_filter_list):
    df_meta = deepcopy(df_meta_ini)

    for cat_tuple in cat_filter_list:
        inst_cat_type = cat_tuple[0]
        inst_cat_search = cat_tuple[1]

        if type(inst_cat_search) is not tuple:
            # find indexes of barcodes that match requested caetgory
            inst_cat = inst_cat_search
            cat_ser = df_meta[inst_cat_type]
            found_barcodes = cat_ser[cat_ser == inst_cat].index.tolist()
        else:
            # find indexes of barcodes that match requested categories
            found_barcodes = []
            for inst_cat in inst_cat_search:
                cat_ser = df_meta[inst_cat_type]
                inst_found = cat_ser[cat_ser == inst_cat].index.tolist()
                found_barcodes.extend(inst_found)

        # apply progressive filters to metadata
        df_meta = df_meta.loc[found_barcodes]

    return df_meta

def set_gex_debris_thresh(meta_cell, xlim=7, ylim=100, thresh=1):

    ser_gex_ash = meta_cell['gex-umi-sum-ash']

    n, bins, patches = plt.hist(ser_gex_ash, bins=100, range=(0, xlim))

    colors = []
    for inst_bin in bins:
        if inst_bin <= thresh:
            colors.append('red')
        else:
            colors.append('blue')

    # apply the same color for each class to match the map
    for patch, color in zip(patches, colors):
        patch.set_facecolor(color)


    plt.ylim((0,ylim))

    keep_barcodes = ser_gex_ash[ser_gex_ash >= thresh].index.tolist()

    print('gex-ash-umi thresh', thresh, '; gex-umi thresh', np.sinh(thresh) * 5)
    print('keeping', len(keep_barcodes), 'cells')

    return keep_barcodes

def one_dim_filter(meta_cell, name, thresh, keep, x_max=None, y_max=1500):

    if x_max is None:
        if 'ash' in name:
            x_max = 10
        else:
            x_max = 1000


    ser_data = meta_cell[name]

    n, bins, patches = plt.hist(ser_data, bins=100, range=(0, x_max))

    colors = []
    for inst_bin in bins:
        if keep == 'above':
            if inst_bin <= thresh:
                colors.append('red')
            else:
                colors.append('blue')
        else:
            if inst_bin > thresh:
                colors.append('red')
            else:
                colors.append('blue')

    # apply the same color for each class to match the map
    for patch, color in zip(patches, colors):
        patch.set_facecolor(color)

    plt.ylim((0,y_max))

    if keep == 'above':
        keep_barcodes = ser_data[ser_data >= thresh].index.tolist()
    elif keep == 'below':
        keep_barcodes = ser_data[ser_data < thresh].index.tolist()


    if 'ash' in name:

        print(name, thresh, '; gex-umi thresh', np.sinh(thresh) * 5)
    else:
        print(name, thresh)

    print('keeping', len(keep_barcodes), 'cells')

    drop_barcodes = sorted(list(set(meta_cell.index.tolist()).difference(keep_barcodes)))

    if len(drop_barcodes) > 0:
        print('dropping', len(drop_barcodes), 'cells')
    else:
        print('dropping no cells')

    return keep_barcodes, drop_barcodes

def sort_all_dataframes(df):
    for inst_type in df:
        print('sorting', inst_type)
        inst_df = df[inst_type]
        # sort columns and rows
        cols = sorted(inst_df.columns.tolist())
        rows = sorted(inst_df.index.tolist())
        inst_df = inst_df.loc[rows, cols]

    return df




def calc_meta_features_from_sp(sp, df):

    # initialize standard scaler that can calc mean/std from sparse csr/csc matrix
    scaler = StandardScaler(with_mean=False)

    for inst_type in ['filtered', 'debris']:

        for inst_feat in sp[inst_type].keys():

            # get row names
            rows = sp[inst_type][inst_feat]['features']

            # number of cells measured
            #################################
            inst_name = inst_feat + '-' + inst_type + '-num-meas'
            mat_bin = deepcopy(sp[inst_type][inst_feat]['mat'])
            mat_bin[mat_bin >= 1] = 1
            mat_sum = mat_bin.sum(axis=1)
            arr_sum = np.asarray(mat_sum[:,0])
            list_sum = [x[0] for x in arr_sum.tolist()]
            ser_num_meas = pd.Series(list_sum, index=rows)
            df['meta_'  + inst_feat][inst_name] = ser_num_meas

            # Initialize mean and std calc
            mat = sp[inst_type][inst_feat]['mat'].transpose().tocsr()
            scaler.fit(mat)

            # mean
            ######################
            inst_name = inst_feat + '-' + inst_type + '-mean'
            ser_mean = pd.Series(scaler.mean_, index=rows)
            df['meta_' + inst_feat][inst_name] = ser_mean

            # std
            ######################
            inst_name = inst_feat + '-' + inst_type + '-std'
            ser_std = pd.Series(np.sqrt(scaler.var_), index=rows)
            df['meta_' + inst_feat][inst_name] = ser_std

    return df

def make_df_from_cols(cols):
    inst_col = cols[0]

    cat_titles = []
    for inst_info in inst_col[1:]:
        inst_title = inst_info.split(': ')[0]
        cat_titles.append(inst_title)

    clean_cols = []
    for inst_col in cols:
        inst_clean = []
        for inst_info in inst_col:
            if ': ' in inst_info:
                inst_clean.append(inst_info.split(': ')[1])
            else:
                inst_clean.append(inst_info)
        clean_cols.append(tuple(inst_clean))

    df_ini = pd.DataFrame(data=clean_cols).set_index(0)
    mat = df_ini.values
    rows = df_ini.index.tolist()

    df_meta = pd.DataFrame(data=mat, index=rows, columns=cat_titles)

    return df_meta

def subsample_cats(df, cat_index, num_samples, sample_type='subsample', random_state=99):

    cols = df.columns.tolist()
    cats = sorted(list(set([x[cat_index] for x in cols])))

    all_ds_info = []
    ser_ds_info = None
    orig_cols = []

    if sample_type == 'subsample':
        keep_cols = []
        for inst_cat in cats:
            keep_cat_cols = [x for x in cols if x[cat_index] == inst_cat]

            if len(keep_cat_cols) > num_samples:
                keep_cat_cols = random.sample(keep_cat_cols, num_samples)

            keep_cols.extend(keep_cat_cols)

        df_sample = df[keep_cols]

    elif sample_type == 'downsample':

        df_list = []

        for inst_cat in cats:
            keep_cat_cols = [x for x in cols if x[cat_index] == inst_cat]
            df_cat = df[keep_cat_cols]
            orig_cols.extend(df_cat.columns.tolist())

            if df_cat.shape[1] > num_samples:
                net.load_df(df_cat)
                ds_info = net.downsample(axis='col', ds_type='kmeans', num_samples=num_samples, random_state=random_state)
                df_ds = net.export_df()

            else:
                net.load_df(df_cat)
                ds_info = net.downsample(axis='col', ds_type='kmeans', num_samples=df_cat.shape[1], random_state=random_state)
                df_ds = net.export_df()

            ds_info = [ inst_cat.split(': ')[1] + '_cluster-' + str(x) for x in list(ds_info)]
            all_ds_info.extend(ds_info)

            # clean df_ds columns
            new_cols = []
            for inst_col in df_ds.columns.tolist():
                new_col = list(inst_col)
                new_col[0] = inst_cat.split(': ')[1] + '_' + new_col[0].split(': ')[1]
                new_cols.append(tuple(new_col))
            df_ds.columns = new_cols

            df_list.append(df_ds)

        # concatenate df_sample
        df_sample = pd.concat(df_list, axis=1)

        # drop majority from column name
        df_sample.columns = [tuple(s.replace('Majority-','') for s in tup) for tup in df_sample.columns.tolist()]

        ser_ds_info = pd.Series(data=all_ds_info, index=orig_cols)


    elif sample_type == 'mean':

        df_list = []
        for inst_cat in cats:
            keep_cat_cols = [x for x in cols if x[cat_index] == inst_cat]
            df_cat = df[keep_cat_cols]

            ser_mean = df_cat.mean(axis=1)
            ser_mean.name = inst_cat.split(': ')[1]

            df_list.append(ser_mean)
        df_sample = pd.concat(df_list, axis=1)


    return df_sample, ser_ds_info