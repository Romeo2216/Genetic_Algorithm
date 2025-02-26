# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(GA solving TSP example)
"""
from ga_solver import GAProblem
import cities

class TSProblem(GAProblem):
    """Implementation of GAProblem for the traveling salesperson problem"""
    def __init__(self, match: cities, gene_repeats=False):
        """Initializes a TSProblem instance

        Args:
            match (cities): a cities instance
        """
        self._match = match
        self._gene_repeats = gene_repeats

    def get_gene_repeats(self):
        """Returns the gene_repeats attribute"""
        return self._gene_repeats
    
    def evaluate_individual(self, chromosome):
        """Evaluates an individual's fitness"""
        return - cities.road_length(city_dict, chromosome)
    
    def generate_individual(self):
        """Generates a random individual"""
        return cities.default_road(city_dict)
    
    def get_possible_genes(self):
        """Returns the possible genes for this problem"""
        return cities.default_road(city_dict)

if __name__ == '__main__':

    from ga_solver import GASolver

    city_dict = cities.load_cities("genetic_part3\cities.txt")
    problem = TSProblem(match=cities,gene_repeats=False)
    solver = GASolver(problem)
    solver.reset_population()
    solver.evolve_until(threshold_fitness=10000)
    best = solver.get_best_individual()
    cities.draw_cities(city_dict, best.chromosome)
