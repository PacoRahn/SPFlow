'''
Created on March 30, 2018

@author: Alejandro Molina
'''

import numpy as np

from spn.algorithms.StructureLearning import get_next_operation, learn_structure
from spn.algorithms.splitting.Clustering import get_split_rows_KMeans
from spn.algorithms.splitting.RDC import get_split_rows_RDC, get_split_cols_RDC_py, \
    get_split_rows_RDC_py
from spn.algorithms.splitting.Random import get_split_cols_binary_random_partition, \
    get_split_rows_binary_random_partition

from spn.structure.leaves.histogram.Histograms import create_histogram_leaf
from spn.structure.leaves.parametric.Parametric import create_parametric_leaf
from spn.structure.leaves.piecewise.PiecewiseLinear import create_piecewise_leaf


def learn_mspn_with_missing(data, ds_context, cols="rdc", rows="kmeans", min_instances_slice=200, threshold=0.3,
                            linear=False, ohe=False,
                            leaves=None, memory=None):
    if leaves is None:
        # leaves = create_histogram_leaf
        leaves = create_piecewise_leaf

    rand_gen = np.random.RandomState(17)

    def learn(data, ds_context, cols, rows, min_instances_slice, threshold, linear, ohe):
        split_cols = None
        if cols == "rdc":
            split_cols = get_split_cols_RDC_py(threshold, ohe=True, k=10, s=1 / 6,
                                               non_linearity=np.sin, n_jobs=1,
                                               rand_gen=rand_gen)
        if rows == "kmeans":
            split_rows = get_split_rows_RDC_py(n_clusters=2, ohe=True, k=10, s=1 / 6,
                                               non_linearity=np.sin, n_jobs=1,
                                               rand_gen=rand_gen)
        elif rows == "rdc":
            split_rows = get_split_rows_RDC(ohe=ohe)

        if leaves is None:
            leaves = create_histogram_leaf

        nextop = get_next_operation(min_instances_slice)

        return learn_structure(data, ds_context, split_rows, split_cols, leaves, nextop)

    if memory:
        learn = memory.cache(learn)

    return learn(data, ds_context, cols, rows, min_instances_slice, threshold, linear, ohe)


def learn_mspn(data, ds_context, cols="rdc", rows="kmeans", min_instances_slice=200, threshold=0.3, ohe=False,
               leaves=None, memory=None):
    if leaves is None:
        leaves = create_histogram_leaf

    def learn(data, ds_context, cols, rows, min_instances_slice, threshold, ohe):
        split_cols = None
        if cols == "rdc":
            split_cols = get_split_cols_RDC_py(threshold, ohe=ohe)
        if rows == "rdc":
            split_rows = get_split_rows_RDC_py(ohe=ohe)
        elif rows == "kmeans":
            split_rows = get_split_rows_KMeans()

        nextop = get_next_operation(min_instances_slice)

        return learn_structure(data, ds_context, split_rows, split_cols, leaves, nextop)

    if memory:
        learn = memory.cache(learn)

    return learn(data, ds_context, cols, rows, min_instances_slice, threshold, ohe)



def learn_parametric(data, ds_context, cols="rdc", rows="kmeans", min_instances_slice=200, threshold=0.3, ohe=False,
               leaves=None, memory=None):
    if leaves is None:
        leaves = create_parametric_leaf

    def learn(data, ds_context, cols, rows, min_instances_slice, threshold, ohe):
        split_cols = None
        if cols == "rdc":
            split_cols = get_split_cols_RDC_py(threshold, ohe=ohe)
        if rows == "rdc":
            split_rows = get_split_rows_RDC_py(ohe=ohe)
        elif rows == "kmeans":
            split_rows = get_split_rows_KMeans()

        nextop = get_next_operation(min_instances_slice)

        return learn_structure(data, ds_context, split_rows, split_cols, leaves, nextop)

    if memory:
        learn = memory.cache(learn)

    return learn(data, ds_context, cols, rows, min_instances_slice, threshold, ohe)


