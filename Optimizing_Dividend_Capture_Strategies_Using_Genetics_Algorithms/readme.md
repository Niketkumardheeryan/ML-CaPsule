# Optimizing Dividend Capture Strategies Using Genetic Algorithms

This project focuses on optimizing dividend capture strategies through the use of genetic algorithms. Dividend capture strategy involves buying a stock just before its ex-dividend date and selling it after the dividend is paid out. The objective is to maximize the returns by optimizing the entry and exit points and other parameters using genetic algorithms.

## Table of Contents

- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Dataset](#dataset)
- [Methodology](#methodology)
- [Results](#results)

## Introduction

Dividend capture strategy aims to exploit the predictable drop in stock prices after the dividend is paid out. By using genetic algorithms, we can optimize the parameters involved in this strategy to maximize returns. Genetic algorithms simulate the process of natural selection by generating a population of potential solutions and evolving them over multiple generations.

## Requirements

- Python 3.8+
- pandas
- numpy
- matplotlib
- deap (Distributed Evolutionary Algorithms in Python)

Methodology
Initialization: Generate an initial population of potential solutions.
Evaluation: Evaluate the fitness of each solution based on the returns of the dividend capture strategy.
Selection: Select the best-performing solutions to form a new population.
Crossover: Combine pairs of solutions to create offspring with mixed characteristics.
Mutation: Introduce random changes to some solutions to maintain diversity.
Iteration: Repeat the evaluation, selection, crossover, and mutation steps for multiple generations.