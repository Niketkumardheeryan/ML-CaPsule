import math
import random

def norm_cdf(x):
    # Approximation of the cumulative distribution function for normal distribution
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

def black_scholes_call(S, K, T, r, sigma):
    if sigma <= 0 or T <= 0:
        return max(0.0, S - K)
        
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    call_price = S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)
    return call_price

def optimize_implied_volatility():
    # Target options market parameters
    market_price = 12.50
    S = 100.0  # Spot price
    K = 95.0   # Strike price
    T = 1.0    # Time to maturity
    r = 0.05   # Risk-free rate
    
    def fitness(sigma):
        model_price = black_scholes_call(S, K, T, r, sigma)
        mse = (model_price - market_price) ** 2
        return -mse  # Maximize the negative error
        
    pop_size = 50
    generations = 50
    
    # Initialize random volatilities
    population = []
    for _ in range(pop_size):
        population.append(random.uniform(0.01, 1.0))
        
    for gen in range(generations):
        fitness_scores = []
        for i in range(len(population)):
            fitness_scores.append((population[i], fitness(population[i])))
            
        # Sort descending
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Keep top 50%
        parents = []
        for i in range(pop_size // 2):
            parents.append(fitness_scores[i][0])
            
        next_gen = parents.copy()
        
        while len(next_gen) < pop_size:
            p1 = random.choice(parents)
            p2 = random.choice(parents)
            
            # Crossover
            child = (p1 + p2) / 2.0
            
            # Mutation
            if random.random() < 0.1:
                child += random.uniform(-0.05, 0.05)
                child = max(0.01, child)
                
            next_gen.append(child)
            
        population = next_gen
        
    final_fitness = []
    for i in range(len(population)):
        final_fitness.append((population[i], fitness(population[i])))
    final_fitness.sort(key=lambda x: x[1], reverse=True)
    
    best_sigma = final_fitness[0][0]
    best_price = black_scholes_call(S, K, T, r, best_sigma)
    
    print(f"Target Market Price: {market_price}")
    print(f"Optimal Implied Volatility Found: {best_sigma:.4f}")
    print(f"Model Calculated Price: {best_price:.4f}")

if __name__ == "__main__":
    optimize_implied_volatility()