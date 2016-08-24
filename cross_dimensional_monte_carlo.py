'''
program: cross_dimensional_monte_carlo.py
created: 2016-07-13 -- 19:30 CEST
author: tc
'''

import random
import cPickle

from probability_distributions import prob as P


# Parameters for the a-priori distributions
xmin = 0.0
xmax = 10.0


def apriori_prob(nold, nnew, x):
    '''
    Return the *normalized* a-priori probability distribution for the
    last component of x (this is chosen to be the uniform distribution
    between xmin and xmax).
    '''
    assert min(nold, nnew) >= 0
    assert abs(nold - nnew) == 1
    if nnew == nold + 1:
        if xmin <= x[-1] and x[-1] <= xmax:
            return 1.0 / (xmax - xmin)
        else:
            return 0.0
    elif nnew == nold - 1:
        return 1.0


def sample_apriori_prob(nold, nnew, x):
    '''
    Sample the a-priori probability distribution for the last component
    of x (chosen to be the uniformly distributed between xmin and xmax).
    '''
    assert nnew == nold + 1
    assert len(x) == nold
    return x + [random.uniform(xmin, xmax)]


def prob_acc(nold, nnew, x):
    '''
    Return the Metropolis acceptance probability for a move passing
    from n=nold to n=nnew.
    '''
    if nnew < 0:
        return 0.0
    assert abs(nold - nnew) == 1
    fwd = P(nold, x[:nold]) * apriori_prob(nold, nnew, x)
    bwd = P(nnew, x[:nnew]) * apriori_prob(nnew, nold, x)
    if fwd == 0.0:
        return 0.0
    return min(1.0, bwd / fwd)


# Set MC parameters
nsteps = 10 ** 6
delta = 0.3

# Initialize observables (sector occupation number, and positions)
histo_n = {}
measure_pos_every = 10
nmax_for_pos = 5
pos = {}

# Initialize configuration
n = 0
x = []
# Run the MC loop
for step in xrange(nsteps):
    assert n == len(x)
    # Fixed-n move
    xnew = [random.gauss(x[i], delta) for i in xrange(n)]
    if random.random() * P(n, x) < P(n, xnew):
        x = xnew[:]
    # Variable-n move (either n->n+1 or n->n-1)
    if random.random() < 0.5:
        xnew = sample_apriori_prob(n, n + 1, x)
        if random.random() < prob_acc(n, n + 1, xnew):
            n += 1
            x = xnew[:]
    else:
        if random.random() < prob_acc(n, n - 1, x):
            n -= 1
            x = x[:n]
    # Measure observables
    histo_n[n] = histo_n.get(n, 0) + 1
    if step % measure_pos_every == 0 and 0 < n and n < nmax_for_pos:
        pos[n] = pos.get(n, []) + [x[:]]

for n in sorted(histo_n.keys()):
    print 'Occupation number of sector %i:\t%i' % (n, histo_n[n])

with open('data_order_occupations.pickle', 'w') as out:
    cPickle.dump(histo_n, out)

with open('data_positions.pickle', 'w') as out:
    cPickle.dump(pos, out)
