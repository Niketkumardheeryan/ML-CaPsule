# Financial Projects with Reinforcement Learning

1.Currency Arbitrage with Reinforcement Learning

##Currency Arbitrage with Reinforcement Learning

### Overview
This project involves developing a Reinforcement Learning (RL) model to perform currency arbitrage. The agent learns to make profitable trades between different currency pairs by observing historical exchange rate data.

### Dataset
The dataset contains historical exchange rates with the following columns:
- `Date`: The date of the observation.
- `USD_EUR`: Exchange rate from USD to EUR.
- `USD_GBP`: Exchange rate from USD to GBP.
- `EUR_GBP`: Exchange rate from EUR to GBP.

##Custom Environment
The custom environment is defined in currency_arbitrage_env.py. It handles the interactions between the agent and the market, including actions (Buy, Sell, Hold) and rewards.

## Training the Agent
The agent is trained using the DQN algorithm from stable-baselines3. The training process involves learning from the historical data to make profitable trades.

## requirements
Python 3.7+
pandas
numpy
gym
stable-baselines3


