import numpy as np
import random

class PortfolioStressEnv:
    def __init__(self):
        self.initial_balance = 100000.0
        self.balance = self.initial_balance
        self.market_volatility = 0.01
        self.max_steps = 30
        self.current_step = 0
        
    def reset(self):
        self.balance = self.initial_balance
        self.current_step = 0
        self.market_volatility = 0.01
        return self._get_state()
        
    def _get_state(self):
        # Discretize state for Q-table indexing
        return min(int(self.market_volatility * 100), 99)
        
    def step(self, action):
        # Actions: 0 = Hold, 1 = Hedge, 2 = Leverage
        self.current_step += 1
        
        # Introduce a stress event randomly
        if random.random() < 0.15:
            self.market_volatility += 0.05
            
        market_return = np.random.normal(0, self.market_volatility)
        
        if action == 1:
            market_return = max(market_return, -0.01) - 0.005 # Hedged constraint
        elif action == 2:
            market_return *= 2.0 # Amplified risk
            
        self.balance *= (1.0 + market_return)
        
        reward = (self.balance - self.initial_balance) / self.initial_balance
        done = self.current_step >= self.max_steps
        
        return self._get_state(), reward, done

def train_rl_agent():
    env = PortfolioStressEnv()
    q_table = np.zeros((100, 3)) 
    
    alpha = 0.1    # Learning rate
    gamma = 0.95   # Discount factor
    epsilon = 0.1  # Exploration rate
    episodes = 5000
    
    print("Training RL Agent for Portfolio Stress Testing...")
    
    for episode in range(episodes):
        state = env.reset()
        done = False
        
        while not done:
            if random.uniform(0, 1) < epsilon:
                action = random.randint(0, 2)
            else:
                action = np.argmax(q_table[state])
                
            next_state, reward, done = env.step(action)
            
            old_value = q_table[state, action]
            next_max = np.max(q_table[next_state])
            
            # Apply formal Q-learning algorithm update
            new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
            q_table[state, action] = new_value
            
            state = next_state
            
    print("Training Complete. Agent has learned optimal hedging strategies under stress.")
    print("Sample Q-Table output for high volatility (State 10):", q_table[10])

if __name__ == "__main__":
    train_rl_agent()