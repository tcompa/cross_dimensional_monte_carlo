# cross_dimensional_monte_carlo
The goal of a typical Markov-Chain Monte Carlo algorithm is to generate samples drawn from a given probability distribution in N dimensions.
Here I show an example of how the Metropolis algorithm can be adapted to the case where the distribution of interest is rather a combination of probability distributions in 0, 1, 2, ..., N dimensions.

This idea (or its more sophisticated versions) exists in different fields with different names:

1. The path-integral formulation for a many-body quantum system can be set up so that two different classes of configurations exist: The configurations with only closed paths, and those where one of the paths is open. The latter is necessary to measure off-diagonal observables.
For N three-dimensional atoms, a closed configuration has 3×N×P position variables (where P is the number of imaginary-time slices), while the position degrees of freedom for an open configuration are 3×N×(P+1). Thus the algorithm needs to be able to switch back and forth between these two configuration spaces with different dimensionality.
See for instance [this paper](http://dx.doi.org/10.1103/PhysRevE.74.036701) (open version [here](https://arxiv.org/abs/physics/0605225)).

2. In a more general case, physical observables can be expressed as a series of terms (represented via Feynman diagrams) which involve integrals of increasing dimensionality. Also in this case, it is possible to write algorithms which travel in the space of diagrams, and keep changing the dimensionality of the state.
See [this work](http://www.sciencedirect.com/science/article/pii/S1875389210006498)  (pdf [here](http://www.sciencedirect.com/science/article/pii/S1875389210006498/pdf?md5=c183b79725279562072f349d5c65d22c&pid=1-s2.0-S1875389210006498-main.pdf)) for more details.

3. In the Bayesian-inference field, this is known as [reversible-jump](http://biomet.oxfordjournals.org/content/82/4/711.short), or [trans-dimensional](https://www-sigproc.eng.cam.ac.uk/foswiki/pub/Main/SJG/hssschapter.pdf) Monte Carlo.

### Contents
1. The main program ([cross_dimensional_monte_carlo.py](cross_dimensional_monte_carlo.py)) is written in pure python, so that it can be run via [pypy](http://pypy.org) for a gain in performance.
2. The sampling procedure is decoupled from the definition of the probability distribution. The latter is defined in [probability_distributions.py](probability_distributions.py), and can be changed at will.
3. [show_order_occupations.py](show_order_occupations.py) shows the probability of being in a N-dimensional sector, as a function of N.
4. [show_radial_distributions.py](show_radial_distributions.py) shows an example of an observable (the probability distribution for the N-dimensional radius), measured in sectors with different dimensionality.

Questions and comments are welcome!
