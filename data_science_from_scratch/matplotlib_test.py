#!/usr/bin/env python
# -*- coding: utf8 -*-

__author__ = 'admin'

from matplotlib import pyplot as plt
from functools import reduce

def matplotlib_test():
    years = [1950, 1960, 1970, 1980, 1990, 2000, 2010]
    gdp = [300.2, 543.3, 1075.9, 2862.5, 5979.6, 10289.7, 14958.3]
    plt.plot(years, gdp, color='green', marker='o', linestyle='solid')
    plt.title("test GDP")
    plt.ylabel("d")
    plt.show()

def vector_add(v, w):
    """+"""
    return [v_i + w_i for v_i, w_i in zip(v, w)]

def vector_subtract(v, w):
    """-"""
    return [v_i - w_i for v_i, w_i in zip(v, w)]

def f(x, y):
    return x + y

def vector_sum(v):
    return reduce(f, v)


if __name__ == '__main__':
    #matplotlib_test()
    #print(vector_add([1, 2, 3], [4, 5, 6]))
    print(vector_sum([1, 2, 3]))