# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from environment import GridWorld
from methods import SARSA, Q_learning

grid = GridWorld(False)


# =============================================================================
# SARSA
# =============================================================================

num_episodes = 500
starting_loc = (4, 2)
max_episode_len = 1500 
gamma = 0.9 
epsilon = 0.99 
alpha = 0.1

Q_sarsa, p_sarsa = SARSA(grid, num_episodes, starting_loc, max_episode_len, gamma, epsilon, alpha)

trace = []
state_idx = grid.loc_to_state(starting_loc, grid.locs)

# grid.draw_deterministic_policy(p_sarsa)
# plt.savefig('det_pol_sarsa.png')
e = 0
while not grid.absorbing[0, state_idx] and e <= 20:
    action_idx = p_sarsa[state_idx]
    trace.append(grid.state_to_loc(state_idx))
    _, action_idx, _, state_idx = grid.state_action_step(state_idx, action_idx)
    e += 1
trace.append(grid.state_to_loc(state_idx))

grid.plot_trace(trace, title='SARSA')

plt.savefig('trace_sarsa.png')

# =============================================================================
# Q-learning
# =============================================================================

num_episodes = 500
starting_loc = (4, 2)
max_episode_len = 2000 
gamma = 0.9 
epsilon = 0.99 
alpha = 0.2

Q_qlearn, p_qlearn = Q_learning(grid, num_episodes, starting_loc, max_episode_len, gamma, epsilon, alpha)

trace = []
state_idx = grid.loc_to_state(starting_loc, grid.locs)

# grid.draw_deterministic_policy(p_qlearn)
# plt.savefig('det_pol_qlearning.png')
e = 0
while not grid.absorbing[0, state_idx] and e <= 20:
    action_idx = p_qlearn[state_idx]
    trace.append(grid.state_to_loc(state_idx))
    _, action_idx, _, state_idx = grid.state_action_step(state_idx, action_idx)
    e += 1
trace.append(grid.state_to_loc(state_idx))

grid.plot_trace(trace, title='Q-learning')

plt.savefig('trace_qlearning.png')