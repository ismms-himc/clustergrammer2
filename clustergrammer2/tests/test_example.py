#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Nicolas Fernandez.
# Distributed under the terms of the Modified BSD License.

import pytest

from ..example import CGM2


def test_example_creation_blank():
    w = CGM2()
    assert w.value == 'Hello World'
