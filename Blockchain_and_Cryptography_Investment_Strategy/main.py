import numpy as np
import pandas as pd
import yfinance as yf
import random

def get_data():
    assets = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'SOL-USD']
    # Download 1 year of historical market data
    data = yf.download(assets, start='2023-01-01', end='2024-01-01')['Adj Close']
    returns = data.pct_change().dropna()
    return returns, assets

def calculate_fitness(weights, returns):
    annual_return = np.sum(returns.mean() * weights) * 252
    cov_matrix = returns.cov() * 252
    annual_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    if annual_volatility == 0:
        return 0
    return annual_return / annual_volatility

def create_individual(num_assets):
    weights = np.random.random(num_assets)
    return weights / np.sum(weights)

def run_genetic_algorithm():
    returns, assets = get_data()
    num_assets = len(assets)
    
    pop_size = 50
    generations = 100
    mutation_rate = 0.1
    
    # Initialize Population
    population = []
    for _ in range(pop_size):
        population.append(create_individual(num_assets))
        
    for gen in range(generations):
        fitness_scores = []
        for i in range(len(population)):
            fitness_scores.append((population[i], calculate_fitness(population[i], returns)))
            
        # Sort descending to find the fittest individuals
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Selection: Top 50%
        parents = []
        for i in range(pop_size // 2):
            parents.append(fitness_scores[i][0])
            
        next_gen = parents.copy()
        
        # Crossover & Mutation
        while len(next_gen) < pop_size:
            p1 = random.choice(parents)
            p2 = random.choice(parents)
            
            # Uniform crossover
            child = np.zeros(num_assets)
            for i in range(num_assets):
                if random.random() < 0.5:
                    child[i] = p1[i]
                else:
                    child[i] = p2[i]
                    
            # Random mutation
            if random.random() < mutation_rate:
                mutate_idx = random.randint(0, num_assets - 1)
                child[mutate_idx] += np.random.normal(0, 0.1)
                child = np.abs(child)
                
            # Normalize weights back to 1.0
            if np.sum(child) > 0:
                child = child / np.sum(child)
            else:
                child = create_individual(num_assets)
                
            next_gen.append(child)
            
        population = next_gen
        
    final_fitness = []
    for i in range(len(population)):
        final_fitness.append((population[i], calculate_fitness(population[i], returns)))
    final_fitness.sort(key=lambda x: x[1], reverse=True)
    
    best_weights = final_fitness[0][0]
    best_sharpe = final_fitness[0][1]
    
    print("Optimal Crypto Portfolio Weights:")
    for i in range(num_assets):
        print(f"{assets[i]}: {best_weights[i]:.4f}")
    print(f"Expected Sharpe Ratio: {best_sharpe:.4f}")

if __name__ == "__main__":
    run_genetic_algorithm()