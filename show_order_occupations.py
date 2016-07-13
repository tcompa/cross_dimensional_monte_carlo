'''
program: show_order_occupations.py
created: 2016-07-13 -- 19:30 CEST
author: tc
'''

import math
import cPickle
import numpy
import matplotlib.pyplot as plt


with open('data_order_occupations.pickle', 'r') as read:
    histo_n = cPickle.load(read)

nmax = max(histo_n.keys())
all_n = numpy.arange(nmax + 1.0)

Z_by_Z0_MC = numpy.array([histo_n[n] for n in all_n]) / float(histo_n[0])
plt.scatter(all_n, Z_by_Z0_MC, label='MC', zorder=4, s=50)

Z_by_Z0_exact = numpy.exp(-all_n)
plt.plot(all_n, Z_by_Z0_exact, label='exact', c=u'C1')

plt.xlabel('$n$', fontsize=18)
plt.ylabel('$Z_n/Z_0$', fontsize=18)

plt.legend(loc='best', frameon=True)
plt.yscale('log')
plt.grid()
plt.savefig('fig_order_occupations.pdf', bbox_inches='tight')
plt.show()
