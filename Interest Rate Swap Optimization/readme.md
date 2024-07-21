## Interest Rate Swap Optimization Using Genetic Algorithm

# Overview
This project applies a genetic algorithm to optimize interest rate swap strategies. The goal is to determine the best allocation between fixed and floating rates that maximizes the portfolio value over a given period.

# Dataset
The dataset, interest_rate_swap_data.csv, contains synthetic data for interest rate swap optimization. It includes daily data from January 1, 2020, to December 31, 2023, with the following columns:

Date: The date of the observation.
Fixed_Rate: The fixed interest rate.
Floating_Rate: The floating interest rate.

# Genetic Algorithm
Steps
**Load Data:** Load the dataset and prepare it for processing.
**Define Fitness** Function: Evaluate the performance of an interest rate swap strategy based on fixed and floating rates.
**Initialize Population:** Create an initial population of strategies.
**Selection:** Select the best-performing strategies as parents.
**Crossover:** Combine parts of two parent strategies to create offspring.
**Mutation:** Randomly alter some strategies to maintain genetic diversity.
**Run the Genetic Algorithm:** Execute the genetic algorithm to find the optimal strategy.

## Contributor
Ashish Kumar Patel