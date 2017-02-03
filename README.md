# fairdiv-indivisible-items

The purpose of this repo is to provide easy-to-play-with pieces of
code, to illustrate various fair division notions and protocols.
More specifically, we follow the following chapter:

> Bouveret, Sylvain, Chevaleyre, Yann et Maudet, Nicolas (2016). Fair
> Allocation of Indivisible Goods. In Brandt, Felix, Conitzer,
> Vincent, Endriss, Ulle, Lang, Jérôme et Procaccia, Ariel D.,
> éditeurs, Handbook of Computational Social Choice,
> Chapitre 12.Cambridge University Press. 

## Organisation
The code is divided in four main modules:
* `problem.py` allows to define various problems
* `fairnessmeasures.py` defines different functions to compute
  fairness measures
* `mipsolving.py` implements MIP formulations for fair optimisation problems
* `protocols.py` implements several protocols discussed in the chapter
  (adjusted winner, picking sequences, Liption et al., etc.)
  
It is accompanied with a Jupyter Notebook illustrating the different
notions. 

## Dependencies
Requires to have installed:
* Pulp 

