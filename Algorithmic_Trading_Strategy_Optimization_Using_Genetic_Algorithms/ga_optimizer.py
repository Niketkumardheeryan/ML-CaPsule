"""
Genetic Algorithm Optimizer for Algorithmic Trading Strategy Optimization.

Implements diverse population initialization, parameter-based crossover (blend/uniform),
bounded Gaussian parameter mutation, tournament selection, elitism, and penalty-guided
fitness evaluation pipeline.
"""

import copy
import random
from typing import Any, Dict, List, Tuple
import numpy as np
import pandas as pd

from .backtest import run_backtest
from .strategy import (
    GENE_BOUNDS,
    generate_random_chromosome,
    sanitize_chromosome,
)


def evaluate_fitness(chromosome: Dict[str, Any], df: pd.DataFrame) -> float:
    """
    Calculate strategy fitness score using Sharpe ratio and trade volume / drawdown penalties.

    Parameters
    ----------
    chromosome : Dict[str, Any]
        Strategy chromosome.
    df : pd.DataFrame
        OHLCV market DataFrame.

    Returns
    -------
    float
        Fitness score (higher is better).
    """
    results = run_backtest(df, chromosome)

    sharpe = results["sharpe_ratio"]
    mdd_frac = results["max_drawdown_pct"] / 100.0
    num_trades = results["num_trades"]

    # Severe penalty for inactive strategies (0 trades)
    if num_trades == 0:
        return -5.0

    # Small penalty for very low trade count to encourage active strategies
    trade_penalty = 0.5 if num_trades < 3 else 0.0

    # Drawdown penalty if maximum drawdown exceeds 25% threshold
    dd_penalty = 3.0 * max(0.0, mdd_frac - 0.25)

    fitness = sharpe - dd_penalty - trade_penalty
    return float(max(-10.0, fitness))


def tournament_selection(
    population: List[Dict[str, Any]], fitness_scores: np.ndarray, k: int = 3
) -> Dict[str, Any]:
    """Select the individual with highest fitness from a random tournament subset of size k."""
    pop_size = len(population)
    selected_indices = random.sample(range(pop_size), k=min(k, pop_size))
    best_idx = selected_indices[int(np.argmax(fitness_scores[selected_indices]))]
    return copy.deepcopy(population[best_idx])


def crossover_chromosomes(
    parent1: Dict[str, Any], parent2: Dict[str, Any], crossover_rate: float = 0.8
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Perform uniform and blend crossover on parent strategy chromosomes.

    Returns
    -------
    Tuple[Dict[str, Any], Dict[str, Any]]
        (child1, child2)
    """
    if random.random() > crossover_rate:
        return copy.deepcopy(parent1), copy.deepcopy(parent2)

    child1 = {}
    child2 = {}

    for gene in GENE_BOUNDS:
        val1 = parent1[gene]
        val2 = parent2[gene]

        if random.random() < 0.5:
            # Swap gene values
            child1[gene] = val2
            child2[gene] = val1
        else:
            # Blend gene values with random alpha
            alpha = random.uniform(0.1, 0.9)
            if GENE_BOUNDS[gene][2]:  # Is Integer
                child1[gene] = int(round(alpha * val1 + (1.0 - alpha) * val2))
                child2[gene] = int(round((1.0 - alpha) * val1 + alpha * val2))
            else:
                child1[gene] = alpha * val1 + (1.0 - alpha) * val2
                child2[gene] = (1.0 - alpha) * val1 + alpha * val2

    return sanitize_chromosome(child1), sanitize_chromosome(child2)


def mutate_chromosome(
    chromosome: Dict[str, Any], mutation_rate: float = 0.2
) -> Dict[str, Any]:
    """
    Apply bounded Gaussian jitter mutation to chromosome parameters.

    Returns
    -------
    Dict[str, Any]
        Mutated valid strategy chromosome.
    """
    mutated = copy.deepcopy(chromosome)

    for gene, (min_val, max_val, is_int) in GENE_BOUNDS.items():
        if random.random() < mutation_rate:
            gene_range = max_val - min_val
            scale = gene_range * 0.15
            delta = random.gauss(0.0, scale)

            new_val = mutated[gene] + delta
            new_val = max(min_val, min(max_val, new_val))

            if is_int:
                mutated[gene] = int(round(new_val))
            else:
                mutated[gene] = float(new_val)

    return sanitize_chromosome(mutated)


class GeneticAlgorithmOptimizer:
    """
    Genetic Algorithm Engine for Strategy Parameter Evolution.
    """

    def __init__(
        self,
        population_size: int = 30,
        generations: int = 20,
        crossover_rate: float = 0.8,
        mutation_rate: float = 0.2,
        elitism_count: int = 2,
        tournament_k: int = 3,
        seed: int = 42,
    ):
        self.population_size = max(4, population_size)
        self.generations = max(1, generations)
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elitism_count = max(0, min(self.population_size // 2, elitism_count))
        self.tournament_k = tournament_k
        self.seed = seed

    def run(self, df: pd.DataFrame, verbose: bool = True) -> Dict[str, Any]:
        """
        Execute Genetic Algorithm optimization on training market dataset.

        Returns
        -------
        Dict[str, Any]
            Dict containing best_chromosome, best_fitness, history, and training statistics.
        """
        random.seed(self.seed)
        np.random.seed(self.seed)

        # 1. Initialize Diverse Population
        population = [generate_random_chromosome() for _ in range(self.population_size)]

        history = {
            "best_fitness": [],
            "mean_fitness": [],
            "best_chromosomes": [],
        }

        best_overall_chrom = None
        best_overall_fitness = -float("inf")

        for gen in range(self.generations):
            # 2. Evaluate Fitness for Population
            fitness_scores = np.array(
                [evaluate_fitness(ind, df) for ind in population], dtype=float
            )

            gen_best_idx = int(np.argmax(fitness_scores))
            gen_best_fit = float(fitness_scores[gen_best_idx])
            gen_mean_fit = float(np.mean(fitness_scores))

            history["best_fitness"].append(gen_best_fit)
            history["mean_fitness"].append(gen_mean_fit)
            history["best_chromosomes"].append(copy.deepcopy(population[gen_best_idx]))

            if gen_best_fit > best_overall_fitness:
                best_overall_fitness = gen_best_fit
                best_overall_chrom = copy.deepcopy(population[gen_best_idx])

            if verbose:
                print(
                    f"Generation {gen+1:2d}/{self.generations:2d} | "
                    f"Best Fitness (Sharpe): {gen_best_fit:+.4f} | "
                    f"Mean Fitness: {gen_mean_fit:+.4f}"
                )

            # 3. Create Next Generation with Elitism, Selection, Crossover, & Mutation
            sorted_indices = np.argsort(fitness_scores)[::-1]
            new_population = []

            # Elitism: preserve top performers directly
            for i in range(self.elitism_count):
                new_population.append(copy.deepcopy(population[sorted_indices[i]]))

            # Generate remaining offspring
            while len(new_population) < self.population_size:
                p1 = tournament_selection(population, fitness_scores, k=self.tournament_k)
                p2 = tournament_selection(population, fitness_scores, k=self.tournament_k)

                c1, c2 = crossover_chromosomes(p1, p2, self.crossover_rate)

                c1 = mutate_chromosome(c1, self.mutation_rate)
                c2 = mutate_chromosome(c2, self.mutation_rate)

                new_population.append(c1)
                if len(new_population) < self.population_size:
                    new_population.append(c2)

            population = new_population

        return {
            "best_chromosome": best_overall_chrom,
            "best_fitness": best_overall_fitness,
            "history": history,
        }
