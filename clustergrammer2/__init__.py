#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Nicolas Fernandez.

from .example import CGM2
from ._version import __version__, version_info

from .nbextension import _jupyter_nbextension_paths

# set up clustergrammer2
from .clustergrammer_fun import *
net = Network(CGM2)
