'''
program: show_radial_distributions.py
created: 2016-07-13 -- 19:30 CEST
author: tc
'''

import math
import cPickle
import numpy
import matplotlib.pyplot as plt

sigma_sq = 0.25
sigma = math.sqrt(sigma_sq)

with open('data_positions.pickle', 'r') as read:
    data = cPickle.load(read)

for n in xrange(1, 5):
    if n not in data.keys():
        continue
    x = numpy.array(data[n])
    assert x.shape[1] == n

    # Compute radii and their histogram
    r = (x ** 2).sum(axis=1) ** 0.5
    h, e = numpy.histogram(r / sigma, bins=128, normed=True)
    c = 0.5 * (e[1:] + e[:-1])
    plt.plot(c, h, label='$n=%i$' % n)

    # Compute exact radial distribution
    surface_unit_sphere = n * math.pi ** (n / 2.0) / math.gamma(n / 2.0 + 1)
    gaussian_prefactor = 1.0 / (2.0 * math.pi * sigma_sq) ** (n / 2.0)
    h_ex = (numpy.exp(- c ** 2 / 2.0) * c ** (n - 1.0) *
            gaussian_prefactor * surface_unit_sphere * sigma ** n)
    plt.plot(c, h_ex, ls='--', c='k')

plt.xlabel('$r/\\sigma$', fontsize=18)
plt.ylabel('$P(r) \\times \\sigma$', fontsize=18)

plt.legend(loc='best', frameon=True)
plt.xlim(0.0, 4.0)
plt.ylim(bottom=0.0)
plt.grid()
plt.savefig('fig_radial_distribution.pdf', bbox_inches='tight')
plt.show()
