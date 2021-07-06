#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Nicolas Fernandez.

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'nbextension/static',
        'dest': 'clustergrammer2',
        'require': 'clustergrammer2/extension'
    }]
