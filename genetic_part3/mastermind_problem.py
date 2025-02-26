# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(GA solving Mastermind example)
"""
from ga_solver import GAProblem
import mastermind as mm


class MastermindProblem(GAProblem):
    """Implementation of GAProblem for the mastermind problem"""

    def __init__(self, match: mm, gene_repeats=False):
        """Initializes a MastermindProblem instance

        Args:
            match (mm.MastermindMatch): a MastermindMatch instance
        """
        self._match = match
        self._gene_repeats = gene_repeats

    def get_gene_repeats(self):
        """Returns the gene_repeats attribute"""
        return self._gene_repeats
    
    def evaluate_individual(self, chromosome):
        """Evaluates an individual's fitness"""
        return self._match.rate_guess(chromosome)
    
    def generate_individual(self):
        """Generates a random individual"""
        return self._match.generate_random_guess()
    
    def get_possible_genes(self):
        """Returns the possible genes for this problem"""
        return mm.get_possible_colors()


if __name__ == '__main__':

    from ga_solver import GASolver

    match = mm.MastermindMatch(secret_size=12)
    problem = MastermindProblem(match, gene_repeats=True)
    solver = GASolver(problem)

    solver.reset_population()
    solver.evolve_until(threshold_fitness=match.max_score())
    best = solver.get_best_individual()

    print(f"Best guess {best.chromosome}")
    print(f"Score {best.fitness}")


"""
print(
        f"Best guess {mm.decode_guess(solver.getBestDNA())} {solver.get_best_individual()}")
    print(
        f"Problem solved? {match.is_correct(solver.get_best_individual().chromosome)}")

"""
    