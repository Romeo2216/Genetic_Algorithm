# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 11:24:15 2022

@author: agademer & tdrumond

Template for exercise 1
(genetic algorithm module specification)
"""

import cities
import random


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
        for n in range(self._pop_size):

            chromosome = cities.default_road("cities.txt") #creation of a random chormosome
            random.shuffle(chromosome) #shuffle the chromosome
            fitness = - cities.road_length(city_dict, chromosome) #evaluation of the fitness of the chromosome
            new_individual = Individual(chromosome, fitness) #creation of a new individual
            self._population.append(new_individual) #add the new individual to the population

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
        #sort the population in descending order, based on the fitness of the individuals
        self._population.sort(key=lambda x: x.fitness, reverse=True) 

        #selection: remove the less adapted individuals
        selection_size = int(len(self._population) * self._selection_rate)
        self._population = self._population[:selection_size]

        #reproduction: recreate the same quantity by crossing the surviving ones
        #set to store the unique pairs of parents
        unique_pairs = set() 
        #while the population is not full
        while len(self._population) < self._pop_size: 
            #select two parents randomly
            parent1 = self._population[random.randrange(0, selection_size)]
            parent2 = self._population[random.randrange(0, selection_size)]
            #if the parents are different and the pair is unique
            if parent1 != parent2 and (parent1, parent2) not in unique_pairs:
                #add the pair to the set of unique pairs
                unique_pairs.add((parent1, parent2))
                #generate a random crossing point
                crossing_point = random.randrange(0, len(parent1.chromosome))
                #create a new chromosome by crossing the parents at the crossing point
                new_chromosome = parent1.chromosome[:crossing_point] + (parent2.chromosome not in parent1.chromosome)
                
                #mutation: for each new individual, mutate with probability mutation_rate
                if random.random() < self._mutation_rate:
                    #generate a random mutation point
                    point1, point2 = random.randrange(0, len(new_chromosome),2)
                    value1, value2 = new_chromosome[point1], new_chromosome[point2]
                    #swap the values at the mutation points
                    new_chromosome[point1], new_chromosome[point2] = value2, value1
                #evaluate the fitness of the new chromosome                    
                new_fitness = - cities.road_length(city_dict, new_chromosome)
                #create a new individual with the new chromosome and the new fitness
                new_individual = Individual(new_chromosome, new_fitness)
                #add the new individual to the population
                self._population.append(new_individual)


    def show_generation_summary(self):
        """ Print some debug information on the current state of the population """
        pass  # REPLACE WITH YOUR CODE

    def get_best_individual(self):
        """ Return the best Individual of the population """
        #sort the population in descending order, based on the fitness of the individuals
        self._population.sort(key=lambda x: x.fitness, reverse=True) 
        #return the first individual of the population (which will have the highest fitness value)
        return self._population[0]

    def evolve_until(self, max_nb_of_generations=500, threshold_fitness=None):
        """ Launch the evolve_for_one_generation function until one of the two condition is achieved : 
            - Max nb of generation is achieved
            - The fitness of the best Individual is greater than or equal to
              threshold_fitness
        """
        #while the maximum number of generations is not reached and the fitness of the best individual is less than the threshold fitness
        while max_nb_of_generations > 0 and self.get_best_individual().fitness < threshold_fitness:
            #evolve for one generation
            self.evolve_for_one_generation()
            #decrement the maximum number of generations
            max_nb_of_generations -= 1

city_dict = cities.load_cities("cities.txt")

solver = GASolver()
solver.reset_population()
solver.evolve_until()

best = solver.get_best_individual()
cities.draw_cities(city_dict, best.chromosome)