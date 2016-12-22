#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from strangers_kaggle.skeleton import fib

__author__ = "eldavojohn"
__copyright__ = "eldavojohn"
__license__ = "none"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
