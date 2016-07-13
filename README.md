# cross_dimensional_monte_carlo
The goal of a typical Markov-Chain Monte Carlo algorithm is to generate samples drawn from a probability distribution in N dimensions.
Here I show an example of how the Metropolis algorithm can be adapted to the case where the distribution of interest is rather a combination of probability distributions in 0, 1, 2, ..., N dimensions.  

### Statistical Physics
This idea (in more sophisticated versions) is often used in statistical-physics simulations of quantum systems, in the broad class of Diagrammatic Monte Carlo algorithms.
Two relevant examples are:

1. A path-integral quantum Monte Carlo simulation (for bosonic particles, for instance) can be generalized so that both diagonal and off-diagonal configurations (i.e., closed or open paths) are visited. For N three-dimensional atoms, a closed configuration has 3×N×P position variables (where P is the number of imaginary-time slices), while the position variables in an open configuration are 3×N×(P+1). Thus the algorithm needs to be able to switch back and forth between these two configuration spaces with different dimensionality.
2. In a more general case, physical observables can be expressed as a series of terms (represented via Feynman diagrams) which involve integrals of increasing dimensionality. Also in this case, it is possible to write algorithms which travel in the space of diagrams, and keep changing the dimensionality of the state.

### Comments
1. The main program ([cross_dimensional_monte_carlo.py](cross_dimensional_monte_carlo.py)) is written in pure python, meaning that it can be run via [pypy](http://pypy.org/) for a gain in performance.
2. The sampling procedure is decoupled from the definition of the probability distribution. The latter is defined in [probability_distributions.py](probability_distributions.py), and can be changed at will.
3. [show_order_occupations.py](show_order_occupations.py) shows the probability of being in a N-dimensional sector, as a function of N.
4. [show_radial_distributions.py](show_radial_distributions.py) shows an example of an observable (the probability distribution for the N-dimensional radius), measured in sectors with different dimensionality.

Questions and comments are welcome!
