# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 11:24:15 2022

@author: agademer & tdrumond

Template for exercise 1
(genetic algorithm module specification)
"""

import random
import itertools
import mastermind as mm
from tqdm import tqdm

class Individual:
    """Represents an Individual for a genetic algorithm"""

    def __init__(self, chromosome: list, fitness: float):
        """Initializes an Individual for a genetic algorithm 

        Args:
            chromosome (list[]): a list representing the individual's chromosome
            fitness (float): the individual's fitness (the higher, the better the fitness)
        """
        self.chromosome = chromosome
        self.fitness = fitness

    def __lt__(self, other):
        """Implementation of the less_than comparator operator"""
        return self.fitness < other.fitness

    def __repr__(self):
        """Representation of the object for print calls"""
        return f'Indiv({self.fitness:.1f},{self.chromosome})'


class GASolver:
    def __init__(self, selection_rate=0.5, mutation_rate=0.1, pop_size=50):
        """Initializes an instance of a ga_solver for a given GAProblem

        Args:
            selection_rate (float, optional): Selection rate between 0 and 1.0. Defaults to 0.5.
            mutation_rate (float, optional): mutation_rate between 0 and 1.0. Defaults to 0.1.
        """
        self._pop_size = pop_size
        self._selection_rate = selection_rate
        self._mutation_rate = mutation_rate
        self._population = []

    def reset_population(self):
        """ Initialize the population with pop_size random Individuals """

        for i in range(self._pop_size):

            chromosome = MATCH.generate_random_guess()

            fitness = MATCH.rate_guess(chromosome) # evaluate a chromosome

            new_individual = Individual(chromosome, fitness) #create a new individual

            self._population.append(new_individual) # add new individuals to the _population list

        pass  # REPLACE WITH YOUR CODE

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
        # Sort the population by fitness in descending order
        self._population.sort(key=lambda x: x.fitness, reverse=True)

        # Selection: Keep only the top individuals based on the selection rate
        self._population = self._population[:int(len(self._population) * self._selection_rate)]
        
        # Generate all possible pairs of indices for reproduction
        nombres = range(0, len(self._population) - 1)
        combinaisons = list(itertools.combinations(nombres, 2))

        # Reproduce until the population size is restored
        while len(self._population) < self._pop_size:
        
            # Select a random pair of parents from the combinations
            index = random.choice(combinaisons)
            combinaisons.remove(index)
            
            parent1 = self._population[index[0]]
            parent2 = self._population[index[1]]

            # Perform single-point crossover to create a new chromosome
            x_point = random.randint(0, len(parent1.chromosome) - 1)
            new_chrom = parent1.chromosome[0:x_point] + parent2.chromosome[x_point:]

            # Mutation: With a probability defined by mutation_rate, mutate the chromosome
            number = random.random()
            if number < self._mutation_rate:
                valid_colors = mm.get_possible_colors()  # Get valid colors for mutation
                new_gene = random.choice(valid_colors)  # Choose a random new gene
                index = random.randint(0, len(new_chrom) - 1)  # Choose a random position
                new_chrom[index] = new_gene  # Replace the gene at the chosen position        

            # Create a new individual with the mutated chromosome and evaluate its fitness
            new_individual = Individual(new_chrom, MATCH.rate_guess(new_chrom))

            # Add the new individual to the population
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

MATCH = mm.MastermindMatch(secret_size=4)
solver = GASolver()
solver.reset_population()
solver.evolve_until(threshold_fitness=MATCH.max_score())

best = solver.get_best_individual()
print(MATCH._secret)
print(f"Best guess {best.chromosome}")
print(f"Score {best.fitness}")
print(f"Problem solved? {MATCH.is_correct(best.chromosome)}")


