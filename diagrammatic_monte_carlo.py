'''
program: diagrammatic_monte_carlo.py
created: 2016-07-13 -- 19:30 CEST
author: tc
'''

import random
import sys
import cPickle

from probability_distributions import prob as P


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


def verify_detailed_balance(ntrials=10000, tol=1e-10):
    '''
    Generate several virtual Monte Carlo moves, moving between the n-
    and the (n+1)-dimensional sectors, and explicitly verify that the
    detailed-balance condition holds.
    '''
    for trial in xrange(ntrials):
        n = random.randint(0, 10)
        x = [random.uniform(0.0, 5.0) for dummy in xrange(n + 1)]
        fwd = P(n, x[:-1]) * apriori_prob(n, n + 1, x) * prob_acc(n, n + 1, x)
        bwd = P(n + 1, x) * apriori_prob(n + 1, n, x) * prob_acc(n + 1, n, x)
        if abs(fwd - bwd) > tol:
            sys.exit()
    print 'verified DB for %i trials (tol=%g)' % (ntrials, tol)


# Preliminary check
verify_detailed_balance()

# MC parameters
nsteps = 10 ** 7 * 5
measure_every = 10 * 5

# Parameter for fixed-n steps
delta = 0.3

# Observables
histo_n = {}
data = {n: [] for n in xrange(20)}

# Initialize state and run the MC loop
n = 0
x = []
for step in xrange(nsteps):
    assert n == len(x)

    # Fixed-n move
    xnew = [random.gauss(x[i], delta) for i in xrange(n)]
    if random.random() * P(n, x) < P(n, xnew):
        x = xnew[:]

    # Variable-n move
    if random.random() < 0.5:
        # n -> (n + 1)
        xnew = sample_apriori_prob(n, n + 1, x)
        if random.random() < prob_acc(n, n + 1, xnew):
            n += 1
            x = xnew[:]
    else:
        # n -> (n-1)
        if random.random() < prob_acc(n, n - 1, x):
            n -= 1
            x = x[:n]

    # Take some measurements
    histo_n[n] = histo_n.get(n, 0) + 1
    if step % measure_every == 0:
        if n < 5:
            data[n].append(x)

with open('data_order_occupations.pickle', 'w') as out:
    cPickle.dump(histo_n, out)

with open('data_positions.pickle', 'w') as out:
    cPickle.dump(data, out)
