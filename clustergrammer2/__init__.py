#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Nicolas Fernandez.
# Distributed under the terms of the Modified BSD License.

from .example import ExampleWidget
from ._version import __version__, version_info

from .nbextension import _jupyter_nbextension_paths

# set up clustergrammer2
from .clustergrammer_fun import *
net = Network(ExampleWidget)
