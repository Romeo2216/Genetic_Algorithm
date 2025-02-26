# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(GA solving TSP example)
"""
from ga_solver import GAProblem
import pendu

class PProblem(GAProblem):
    """Implementation of GAProblem for the traveling salesperson problem"""
    def __init__(self, instance: pendu, gene_repeats=False):
        """Initializes a TSProblem instance

        Args:
            (cities): a cities instance
        """
        self._instance = instance
        self._gene_repeats = gene_repeats

    def get_gene_repeats(self):
        """Returns the gene_repeats attribute"""
        return self._gene_repeats
    
    def evaluate_individual(self, chromosome):
        """Evaluates an individual's fitness"""
        return self._instance.guest_similarity(answer, chromosome)
    
    def generate_individual(self):
        """Generates a random individual"""
        return self._instance.default_word(answer)
    
    def get_possible_genes(self):
        """Returns the possible genes for this problem"""
        return self._instance.possible_letters()

if __name__ == '__main__':

    from ga_solver import GASolver

    answer = pendu.choose_word("pouvoir")
    problem = PProblem(pendu, gene_repeats=True)
    solver = GASolver(problem)
    solver.reset_population()
    solver.evolve_until(threshold_fitness=len(answer))
    best = solver.get_best_individual()
    
    print(f"Best guess {best.chromosome}")
    print(f"Score {best.fitness}")
