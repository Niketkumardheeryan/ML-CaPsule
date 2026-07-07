# Sentiment Analysis Driven Trading Strategy Optimization

This project aims to optimize a trading strategy based on stock prices and sentiment data using a genetic algorithm. The goal is to find the best buy and sell thresholds that maximize the portfolio value over a given period.

## Dataset

The dataset used in this project is `sentiment_trading_data.csv`, which contains the following columns:
- `Date`: The date of the observation.
- `Stock_Price`: The stock price on the given date.
- `Sentiment`: The sentiment score for the given date, ranging from -1 to 1.

## Genetic Algorithm Implementation

### Step 1: Load the Data

First, load the `sentiment_trading_data.csv` dataset.

```python
import pandas as pd
import numpy as np

# Load data
data_sentiment = pd.read_csv('sentiment_trading_data.csv')
print(data_sentiment.head())

# Convert to NumPy array (excluding the 'Date' column)
data_sentiment = data_sentiment.drop(columns=['Date']).to_numpy()

# Step 2: Define the Fitness Function
The fitness function evaluates how well a given trading strategy (individual) performs based on stock prices and sentiment.

# step 3: Initialize the Population
Generate an initial population of random trading strategies.

# Step 4: Selection
Select the best-performing individuals to be parents for the next generation.

# Step 5: Crossover
Create offspring by combining parts of two parents.

# Step 6: Mutation
Randomly mutate some individuals to maintain genetic diversity.

#Step 7: Run the Genetic Algorithm
Execute the genetic algorithm with the defined functions.

#Results
The genetic algorithm was run for 50 generations with a population size of 100. The best trading strategy found is:

Buy Threshold: -0.7733929905450716
Sell Threshold: -0.9756864570452264

#Contributor
Ashish Kumar Patel
