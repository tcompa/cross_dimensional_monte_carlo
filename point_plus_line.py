#!/usr/bin/env python


import math
import random

Z0 = 2.0
Z1 = 8.0

mu1 = 0.0
sigma1 = 1.2

#sigma01 = random.uniform(0.7, 3.0)
#sigma10 = random.uniform(0.7, 3.0)
sigma01 = 1.5
sigma10 = 0.9
print 'sigma01:', sigma01
print 'sigma10:', sigma10


def P0():
    return Z0

def P1(x):
    return Z1 * math.exp(- (x - mu1) ** 2 / (2.0 * sigma1 ** 2)) / math.sqrt(2.0 * math.pi * sigma1 ** 2)

def sample_P_proposal_01():
    return random.gauss(0.0, sigma01)

def P_proposal_01(x):
    return math.exp(-x ** 2 / (2.0 * sigma01 ** 2)) / math.sqrt(2.0 * math.pi * sigma01 ** 2)

def norm_Apriori_01():
    #return math.sqrt(2.0 * math.pi * sigma01 ** 2)
    return 1.0

def P_proposal_10(x):
    return math.exp(- x ** 2 / (2.0 * sigma10 ** 2)) / math.sqrt(2.0 * math.pi * sigma10 ** 2)

def norm_Apriori_10():
    #return math.sqrt(2.0 * math.pi * sigma10 ** 2)
    return 1.0

def P_acc_01(x):
    fwd = P1(x) * P_proposal_10(x)
    bwd = P0() * P_proposal_01(x)
    return min(1.0, fwd / bwd)

def P_acc_10(x):
    fwd = P0() * P_proposal_01(x)
    bwd = P1(x) * P_proposal_10(x)
    return min(1.0, fwd / bwd)

def verify_detailed_balance(ntrials=1000, tol=1e-10):
    for trial in xrange(ntrials):
        x = random.uniform(-10.0, 10.0)

        flux01 = P0() * P_proposal_01(x) * P_acc_01(x)
        flux10 = P1(x) * P_proposal_10(x) * P_acc_10(x)
        assert abs(flux01 - flux10) < tol
    print 'verified DB for %i trials (tol=%g)' % (ntrials, tol)


verify_detailed_balance()

# MC parameters
nsteps = 100000

# parameter for 1D simulation
delta = 0.5

#initialize state
n = 1
x = 10.0

# observables
histo = {0:0, 1:0}
xall = []


for step in xrange(nsteps):

    # do trivial move
    if n == 1:
        xnew = random.gauss(x, delta)
        if random.uniform(0.0, 1.0) * P1(x) < P1(xnew):
            x = xnew

    # do open/close move
    if n == 0:
        assert x is None
        if random.uniform(0.0, 1.0) < norm_Apriori_01() / norm_Apriori_10():
            xnew = sample_P_proposal_01()
            if random.uniform(0.0, 1.0) < P_acc_01(xnew):
                n = 1
                x = xnew
        else:
            pass
    else:
        assert x is not None
        if random.uniform(0.0, 1.0) < norm_Apriori_10() / norm_Apriori_01():
            if random.uniform(0.0, 1.0) < P_acc_10(x):
                n = 0
                x = None
        else:
            pass

    # measure
    histo[n] += 1
    if n == 1:
        xall.append(x)



for k in sorted(histo.keys()):
    print k, histo[k] / float(sum(histo.values()))

import matplotlib.pyplot as plt
import numpy
plt.hist(xall, normed=True, bins=150)
xx = numpy.linspace(min(xall), max(xall), 1000)
yy = [P1(a) / Z1 for a in xx]
plt.plot(xx, yy)
plt.show()
