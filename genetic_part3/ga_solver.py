# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(generic genetic algorithm module)
"""

import random
import itertools
from tqdm import tqdm
import numpy as np

class Individual:
    """Represents an Individual for a genetic algorithm"""

    def __init__(self, chromosome: list, fitness: float):
        """Initializes an Individual for a genetic algorithm

        Args:
            chromosome (list[]): a list representing the individual's
            chromosome
            fitness (float): the individual's fitness (the higher the value,
            the better the fitness)
        """
        self.chromosome = chromosome
        self.fitness = fitness

    def __lt__(self, other):
        """Implementation of the less_than comparator operator"""
        return self.fitness < other.fitness

    def __repr__(self):
        """Representation of the object for print calls"""
        return f'Indiv({self.fitness:.1f},{self.chromosome})'


class GAProblem:
    """Defines a Genetic algorithm problem to be solved by ga_solver"""
        
    def evaluate_individual(self, individual: Individual):
        """Evaluates an individual's fitness"""
        
    def generate_individual(self):
        """Generates a random individual"""

    def get_possible_genes(self):
        """Returns the possible genes for this problem"""

    def get_gene_repeats(self):
        """Returns the gene_repeats attribute"""


class GASolver:
    def __init__(self, problem: GAProblem, selection_rate=0.5, mutation_rate=0.1, pop_size=50):
        """Initializes an instance of a ga_solver for a given GAProblem

        Args:
            problem (GAProblem): GAProblem to be solved by this ga_solver
            selection_rate (float, optional): Selection rate between 0 and 1.0. Defaults to 0.5.
            mutation_rate (float, optional): mutation_rate between 0 and 1.0. Defaults to 0.1.
        """
        self._problem = problem
        self._pop_size = pop_size
        self._selection_rate = selection_rate
        self._mutation_rate = mutation_rate
        self._population = []

    def reset_population(self):
        """ Initialize the population with pop_size random Individuals """

        for i in range(self._pop_size):

            # Generate a random individual using the problem's method
            chromosomes = self._problem.generate_individual()
            
            # Evaluate the fitness of the generated individual
            fitness = self._problem.evaluate_individual(chromosomes)

            # Create a new Individual object with the generated chromosome and fitness
            new_individual = Individual(chromosomes, fitness)
    
            # Add the new individual to the population
            self._population.append(new_individual)

    def evolve_for_one_generation(self):
        """ Apply the process for one generation : 
            -	Sort the population (Descending order)
            -	Selection: Remove x% of population (less adapted)
            -   Reproduction: Recreate the same quantity by crossing the 
                surviving ones 
            -	Mutation: For each new Individual, mutate with probability 
                mutation_rate i.e., mutate it if a random value is below   
                mutation_rate
        """

        # Sort the population in descending order based on fitness
        self._population.sort(key=lambda x: x.fitness, reverse=True)

        # Selection: Keep only the top individuals based on the selection rate
        self._population = self._population[:int(len(self._population) * self._selection_rate)]
        
        # Generate all possible combinations of parent indices for reproduction
        nombres = range(0, len(self._population) - 1)
        combinaisons = list(itertools.combinations(nombres, 2))

        # Reproduce until the population size is restored
        while len(self._population) < self._pop_size:
        
            # Randomly select a pair of parents from the combinations
            index = random.choice(combinaisons)
            combinaisons.remove(index)
            
            parent1 = self._population[index[0]]
            parent2 = self._population[index[1]]

            # Perform crossover at a random point
            x_point = random.randint(0, len(parent1.chromosome) - 1)

            if self._problem.get_gene_repeats():
            # If genes can repeat, simply combine segments from both parents
                new_chrom = parent1.chromosome[0:x_point] + parent2.chromosome[x_point:]
            else:
            # If genes cannot repeat, ensure unique genes in the offspring
                segment1 = parent1.chromosome[:x_point]
                segment2 = [gene for gene in parent2.chromosome if gene not in segment1]
                new_chrom = segment1 + segment2

            # Mutation: Apply mutation with a probability equal to mutation_rate
            mutation = random.random()
            if mutation < self._mutation_rate:
                if self._problem.get_gene_repeats():
                    # For problems allowing gene repeats, replace a random gene
                    valid_genes = self._problem.get_possible_genes()
                    new_gene = random.choice(valid_genes)
                    index = random.randint(0, len(new_chrom) - 1)
                    new_chrom[index] = new_gene  
                else:
                    # For problems without gene repeats, swap two random genes
                    index1, index2 = np.random.randint(0, len(new_chrom), 2)
                    new_chrom[index1], new_chrom[index2] = new_chrom[index2], new_chrom[index1]

            # Evaluate the fitness of the new individual
            new_fitness = self._problem.evaluate_individual(new_chrom)

            # Create a new individual and add it to the population
            new_individual = Individual(new_chrom, new_fitness)
            self._population.append(new_individual)

        pass  # REPLACE WITH YOUR CODE

    def show_generation_summary(self):
        """ Print some debug information on the current state of the population """
        pass  # REPLACE WITH YOUR CODE

    def get_best_individual(self):
        """ Return the best Individual of the population """
        self._population.sort(key=lambda x: x.fitness, reverse=True)

        return self._population[0]

    def evolve_until(self, max_nb_of_generations=500, threshold_fitness=None):
        """ Launch the evolve_for_one_generation function until one of the two condition is achieved : 
            - Max nb of generation is achieved
            - The fitness of the best Individual is greater than or equal to
              threshold_fitness
        """
        pbar = tqdm(total=max_nb_of_generations)
        while max_nb_of_generations > 0 and self.get_best_individual().fitness < threshold_fitness:

            self.evolve_for_one_generation()

            pbar.update(1)
            max_nb_of_generations += -1
