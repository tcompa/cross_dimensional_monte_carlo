'''
program: probability_distributions.py
created: 2016-07-13 -- 19 CEST
author: tc
'''

import math


def Z(n):
    return 1.0 / (n + 1.0) ** 3


def prob(n, x):
    '''
    Compute the non-normalized probability distribution for a
    n-dimensional vector x. The normalization is equal to Z(n)
    '''
    mu = 0.0
    sigma_sq = 0.25
    arg = sum((x[i] - mu) ** 2 for i in xrange(n))
    arg /= (2.0 * sigma_sq)
    return Z(n) * math.exp(- arg) * (2.0 * math.pi * sigma_sq) ** (-n / 2.0)
