# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 11:24:15 2022

@author: agademer & tdrumond

Template for exercise 1
(genetic algorithm module specification)
"""

import random
import numpy as np
import itertools
import cities
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

        # Initialize the population with random individuals
        for i in range(self._pop_size):
            # Generate a default road (sequence of cities)
            chromosome = cities.default_road(city_dict)

            # Shuffle the chromosome to create a random individual
            random.shuffle(chromosome)

            # Calculate the fitness of the individual (negative road length)
            fitness = - cities.road_length(city_dict, chromosome)

            # Create a new Individual with the chromosome and fitness
            new_individual = Individual(chromosome, fitness)

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

        # Get the default road (sequence of cities)
        possible_cities = cities.default_road(city_dict)

        # Sort the population in descending order based on fitness
        self._population.sort(key=lambda x: x.fitness, reverse=True)

        # Selection: Keep only the top x% of the population
        self._population = self._population[:int(len(self._population) * self._selection_rate)]
        
        # Generate all possible combinations of parent indices for reproduction
        nombres = range(0, len(self._population) - 1)
        combinaisons = list(itertools.combinations(nombres, 2))

        # Reproduce until the population size reaches the desired size
        while len(self._population) < self._pop_size:
        
            # Select a random pair of parents from the combinations
            index = random.choice(combinaisons)
            combinaisons.remove(index)
            
            parent1 = self._population[index[0]]
            parent2 = self._population[index[1]]

            # Perform crossover at a random point
            x_point = random.randint(1, len(parent1.chromosome) - 1) if len(parent1.chromosome) > 1 else 1

            # Step 1: Get cities in the first segment of parent1
            segment1 = parent1.chromosome[:x_point]

            # Step 2: Get cities from parent2 in order, excluding those already in segment1
            segment2 = [city for city in parent2.chromosome if city not in segment1]

            # Step 3: Merge the two parts to create a new chromosome
            new_chrom = segment1 + segment2

            # Mutation: Swap two cities in the chromosome with a certain probability
            number = random.random()
            if number < self._mutation_rate:
                index1, index2 = np.random.randint(0, len(new_chrom), 2)
                new_chrom[index1], new_chrom[index2] = new_chrom[index2], new_chrom[index1]

            # Calculate the fitness of the new individual
            new_fitness = - cities.road_length(city_dict, new_chrom)

            # Create a new individual and add it to the population
            new_individual = Individual(new_chrom, new_fitness)
            self._population.append(new_individual)

    def show_generation_summary(self):
        """ Print some debug information on the current state of the population """
        pass  # REPLACE WITH YOUR CODE

    def get_best_individual(self):
        """ Return the best Individual of the population """
        self._population.sort(key=lambda x: x.fitness, reverse=True)

        return self._population[0]


    def evolve_until(self, max_nb_of_generations=1000, threshold_fitness=None):
        """ Launch the evolve_for_one_generation function until one of the two condition is achieved : 
            - Max nb of generation is achieved
            - The fitness of the best Individual is greater than or equal to
              threshold_fitness
        """
        pbar = tqdm(total=max_nb_of_generations)
        while max_nb_of_generations > 0 and - self.get_best_individual().fitness < threshold_fitness:

            self.evolve_for_one_generation()

            pbar.update(1)
            max_nb_of_generations += -1

city_dict = cities.load_cities("genetic_part2\cities.txt")
solver = GASolver()
solver.reset_population()
solver.evolve_until(threshold_fitness=10000)

best = solver.get_best_individual()
cities.draw_cities(city_dict, best.chromosome)


