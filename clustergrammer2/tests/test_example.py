#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Nicolas Fernandez.
# Distributed under the terms of the Modified BSD License.

import pytest

from clustergrammer2.tests.expected_values import expected_columns, expected_rows, expected_content

from ..example import ExampleWidget
from clustergrammer2 import net

def test_example_creation_blank():
    w = ExampleWidget()
    assert w.value == 'Hello World'

def test_load_file():
    net.load_file('./examples/rc_two_cats.txt')
    dataframe = net.export_df()
    net.load_df(dataframe)
    dataframe = net.export_df()
    dataframe_columns:list = list(dataframe)

    # Ensure that the columns are identical
    assert len(dataframe_columns)==len(expected_columns)
    assert all([dataframe_columns[index]==expected_columns[index] for index in range(len(dataframe_columns))])

    for row_index, df_row in enumerate(dataframe.iterrows()):

        # Ensure that the row names are identical
        assert df_row[0] == expected_rows[row_index]
        for column_index, column_name in enumerate(expected_columns):

            # Ensure that the content is identical. Expect a small conversion error from reading from different sources
            assert abs(df_row[1][column_name] - expected_content[row_index,column_index])<1e-14
