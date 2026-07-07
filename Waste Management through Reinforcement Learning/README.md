# Project Overview
Epsilon Explorer is a reinforcement learning project designed to explore and analyze the performance of an agent using an epsilon-greedy strategy. The primary objective of this project is to investigate how the agent learns over multiple episodes by balancing exploration (trying new actions) and exploitation (choosing the best-known actions). This project provides valuable insights into the agent's learning dynamics, highlighting the effects of epsilon decay on performance and score improvement.

# Key Concepts
Reinforcement Learning
Reinforcement learning (RL) is a type of machine learning where an agent learns to make decisions by interacting with an environment. The agent receives feedback in the form of rewards or penalties based on its actions, allowing it to learn optimal strategies for maximizing cumulative rewards.

# Epsilon-Greedy Strategy
The epsilon-greedy strategy is a popular approach used in reinforcement learning to balance exploration and exploitation. The strategy employs a parameter, epsilon (ε), which determines the probability of choosing a random action (exploration) versus the best-known action (exploitation). As training progresses, epsilon typically decays, allowing the agent to rely more on learned knowledge and less on exploration.

# Score Tracking
Tracking the scores achieved by the agent during training provides valuable insights into its performance. By analyzing these scores, we can evaluate the effectiveness of different learning strategies and make informed decisions about tuning hyperparameters.


![ep_RL2](https://github.com/user-attachments/assets/4b369c79-64ff-4600-b329-30df9552ad18)
![epsilon_RL1](https://github.com/user-attachments/assets/8b577058-7e29-4776-9cb3-e9f8eaad2016)

Further an real life application of this concept is implemented through the use of a Daily AI Waste Management technique 
--------------------------------------------------------------------------------------------------------------------------

## Project Documentation: Waste Management Reinforcement Learning

Project Overview:
------------------

The project aims to develop a reinforcement learning (RL) agent to optimize waste collection in a simulated environment, minimizing overflow events and improving efficiency.
1) Environment and State Representation:

The state is represented by four features:
Waste Level: Current waste level (0 to 1)
Time of Day: A random value representing the time (0 to 24 hours)
Weather Condition: A random value (0 to 1) indicating the weather
Distance to Collection Point: A random value (0 to 10) representing the distance to the waste collection point.

2) Action Space:

The agent can choose between two actions:
Wait (0): Do not collect waste.
Collect Waste (1): Proceed with waste collection.

3) Reward Structure:

The reward system is designed to encourage efficient waste collection:
+10 for timely collection when the waste level exceeds the threshold.
-5 for premature collection when the waste level is below the threshold.
-1 for each time step to penalize waiting.

4) Training Process:

The agent is trained over 100 episodes, where each episode simulates a series of time steps (up to 20) where the agent makes decisions based on the current state.
The agent learns from experience using a replay memory and updates its policy through Q-learning.

5) Evaluation Metrics:

Performance is evaluated using:
Average Reward per Episode: Measures the effectiveness of the agent's actions.
Epsilon Decay: Tracks the exploration rate, indicating how the agent balances exploration vs. exploitation.
Overflow Events: Counts occurrences when the waste level exceeds the maximum capacity as per previous updation.

6) Visualization:

The results are visualized using Matplotlib to plot:
Average rewards per episode, showing the agent's learning progression and rewards gained on successfull execution and implementation of a specified condition
Epsilon decay over episodes, illustrating the shift from exploration to exploitation.
Overflow events per episode, highlighting improvements in waste management techniques 

Further the results have been visualized with the help of graphs:
![use_case_Waste_management_RL1](https://github.com/user-attachments/assets/4d8724d1-c9d3-4d96-adf0-12b977398edd)
![use_case_waste_managent_2](https://github.com/user-attachments/assets/7153c560-52fb-46c3-b3c0-62fcacb35247)
![use_case_waste_management3](https://github.com/user-attachments/assets/1a8a7109-1c40-4286-bd05-c6cde101f355)

