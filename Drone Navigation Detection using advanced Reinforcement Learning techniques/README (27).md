# Drone Pathfinding and Navigation with Reinforcement Learning
This project visualizes a drone's pathfinding journey in a grid environment, using both classical A* search and Reinforcement Learning (RL) techniques to achieve optimal navigation. The drone aims to reach a target location while avoiding obstacles and optimizing path cost. This file provides a comprehensive overview of the project’s structure, setup instructions, and available visualizations.

# Table of Contents
-> Features 
-> Project Blocks 
-> Setup Instructions 
-> Usage 
-> Visualizations

    1. Basic Environment Setup
    2. Static Path Visualization
    3. Heatmap of Pathfinding Costs
    4. Dynamic Movement Visualization
    5. 3D Surface Plot of Pathfinding Costs
-> Reinforcement Learning (RL) Model 
-> Contributing 
-> License

# Features
Pathfinding with A Algorithm*: Finds an optimal, shortest path from the starting position to the target using the A* heuristic. Reinforcement Learning Navigation: A reinforcement learning model trains to achieve the navigation goal while avoiding obstacles, rewarding efficient paths. Dynamic Obstacles: Specify obstacle positions to simulate real-world barriers and allow pathfinding adaptations. Comprehensive Visualizations: Includes static, dynamic, and 3D visualizations of the environment, path costs, and drone’s decision-making process. Real-time Animation: Watch the drone’s actions in a step-by-step movement toward the target.

# Project Structure
pathfinding block: Contains the A* algorithm and helper functions for calculating paths.
reinforcement_learning block: Implements the reinforcement learning environment using OpenAI Gym, where the drone learns an optimal policy for navigation.
visualizations block: Defines visualization functions, including static, dynamic, and heatmap visualizations.

# Setup Instructions
Clone the repository:

git clone https://github.com/Panchadip-128/Drone-Navigation_Detection_using_RL.git cd Drone-Navigation_Detection_using_RL

# Install required dependencies:
    pip install -r requirements.txt

Run the script: Drone-Navigation_Detection_using_RL.ipynb

# Usage:
Specify Start, Target, and Obstacle Positions: Set coordinates for the drone’s starting position, the target, and obstacles. Choose Navigation Algorithm: Run either the A* pathfinding method or the reinforcement learning model to observe different navigation approaches.

Select Visualization Type: View different visualizations of the environment, path, costs, and drone movements.

# Visualizations
The project includes several visualizations to illustrate pathfinding and navigation strategies in the environment.

- Basic Environment Setup Sets up a grid environment, marking the drone’s starting position, the target, and obstacles.

      def visualize_environment(drone_pos, target_pos, obstacles, grid_size=(10, 10))

  ![env graph](https://github.com/user-attachments/assets/a6868ac3-d936-4b03-a72d-1d20801c6aac)


- Static Path Visualization Displays a static view of the calculated A* path from start to target.

      def visualize_path(drone_pos, target_pos, obstacles, path)
  
  ![a star graph](https://github.com/user-attachments/assets/d70ec385-9cc2-40d6-adf6-5b22f12723d9)

- Heatmap of Pathfinding Costs Shows a heatmap for traversal costs to each grid cell, providing insight into pathfinding challenges.

      def visualize_cost_heatmap(start, goal, obstacles, grid_width, grid_height)

  ![pathfinding_heat-map](https://github.com/user-attachments/assets/320baa43-f83b-4567-8d99-131bfb4dd3b7)

- Dynamic Movement Visualization Animates the drone’s movement toward the target, step-by-step, showing real-time path adjustments.

  ![Navigation Graph](https://github.com/user-attachments/assets/acc92014-bbff-40de-b964-dc649d00a2d7)



- 3D Surface Plot of Pathfinding Costs Visualizes the cost distribution across the grid in 3D, highlighting areas with high or low pathfinding costs.
  
  ![3D Path Finding Cost Suraface schematic](https://github.com/user-attachments/assets/f243d58c-1948-462a-a50b-cfd763807bf9)

- Navigation Graph:

![Drone Navigation Graph](https://github.com/user-attachments/assets/bc69c957-acac-48ce-ad2d-cef3399f3c39)


Reinforcement Learning (RL) Model Overview In addition to the A* algorithm, this project includes a reinforcement learning approach to allow the drone to learn optimal navigation strategies through interaction with the environment. The RL agent is implemented using OpenAI Gym and trained with the Proximal Policy Optimization (PPO) algorithm from stable-baselines3.

RL Environment The RL environment for the drone is defined in DroneEnv, an OpenAI Gym environment that:

Defines the drone’s possible actions: Up, Down, Left, Right, and diagonal moves. Contains a custom reward function: Positive Reward: Awarded for reaching the target. Penalty: Applied when the drone hits an obstacle or moves away from the target. Exploration vs. Exploitation: Introduces a small exploration rate (epsilon) to encourage the drone to explore initially before converging on optimal paths.

# Training the RL Model
    from stable_baselines3 import PPO
    
    env = DroneEnv()
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10000)  # Training the model with adjustable timesteps
    
# Evaluation
After training, the RL model navigates the drone autonomously, continuously adjusting its path based on learned policies. This approach enhances the drone’s flexibility, enabling it to adapt even with changing obstacles or targets.

# Visualizing RL Navigation
The RL model’s path can be dynamically visualized, showing how it navigates step-by-step toward the target:

    obs = env.reset()
    for _ in range(20):
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        env.render()
        if done:
            obs = env.reset()
            
# Contributing
Contributions are welcome! Please fork the repository and create a pull request with improvements or feature addition or contact @Github:Panchadip-128 or @mail: panchadip125@gmail.com.

# License
This project is licensed under MIT License policies.
