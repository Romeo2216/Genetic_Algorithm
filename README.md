# Genetic Algorithm Project

This repository contains implementations of Genetic Algorithms (GA) for solving various optimization problems. The project is divided into three main parts:

## Folder Structure

### `genetic_part1`
This folder contains the foundational implementation of a Genetic Algorithm. It includes:
- Basic GA components such as population initialization, selection, crossover, and mutation.
- Simple examples to demonstrate the working of a GA.

### `genetic_part2`
This folder builds upon `genetic_part1` by introducing:
- Advanced selection methods (e.g., tournament selection, roulette wheel).
- Enhanced mutation and crossover strategies.
- Performance optimizations for larger problem spaces.

### `genetic_part3`
This folder provides a more detailed and modular implementation of the Genetic Algorithm. It is designed to be flexible and reusable for solving various optimization problems. Key features include:
- A generic GA solver that can be adapted to different problems.
- Example implementations for specific problems like the Traveling Salesman Problem (`tsp_problem`) and the Mastermind Problem (`mastermind_problem`).

## Implementing the GA Solver for Any Problem

To use the GA solver for a specific problem, follow these steps:

1. **Define the Problem**:
   - Create a class or function that represents the problem.
   - Define the fitness function to evaluate the quality of a solution.
   - Specify the representation of a solution (e.g., a list of cities for TSP or a sequence of colors for Mastermind).

2. **Configure the GA Solver**:
   - Set parameters such as population size, mutation rate, crossover rate, and the number of generations.
   - Choose appropriate selection, crossover, and mutation strategies.

3. **Integrate the Problem with the GA Solver**:
   - Pass the problem-specific fitness function and solution representation to the GA solver.
   - Ensure the solver can generate and evaluate solutions for the problem.

4. **Run the Solver**:
   - Execute the GA solver and monitor its progress.
   - Analyze the best solution found by the algorithm.

### Example: Solving `tsp_problem`
- Define the cities and distances as input.
- Implement a fitness function that minimizes the total travel distance.
- Use the GA solver to find the optimal route.

### Example: Solving `mastermind_problem`
- Define the secret code and rules for feedback.
- Implement a fitness function that evaluates guesses based on feedback.
- Use the GA solver to deduce the secret code.

For detailed examples, refer to the implementations in the `genetic_part3` folder.

## Conclusion
This project demonstrates the versatility of Genetic Algorithms in solving diverse optimization problems. By following the modular approach in `genetic_part3`, you can adapt the GA solver to tackle new challenges efficiently.
