#!/usr/bin/env python

'''
program: probability_distributions.py
created: 2016-07-13 -- 19 CEST
author: tc
'''

import math


def Zn(n):
    return math.exp(-n)


def prob(n, x):
    mu = 0.0
    sigma_sq = 0.25
    arg = sum((x[i] - mu) ** 2 for i in xrange(n))
    arg /= (2.0 * sigma_sq)
    return Zn(n) * math.exp(- arg) * (2.0 * math.pi * sigma_sq) ** (-n / 2.0)
