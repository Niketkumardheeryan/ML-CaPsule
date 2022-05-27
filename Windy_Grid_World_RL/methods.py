# -*- coding: utf-8 -*-

import numpy as np
import random
from environment import *


def SARSA(grid, num_episodes, start_loc=None, max_episode_len=100, gamma=1.0, epsilon=1.0, alpha=0.1):

    # Init state-action function to zeros
    Q = np.zeros((grid.state_size, grid.action_size))

    for i in range(num_episodes):
        if start_loc == None:
        # Start at random location
            state_loc = random.choice(list(set(grid.locs) - set(grid.absorbing_locs)))
        else:
            state_loc = start_loc
        state_idx = grid.loc_to_state(state_loc, grid.locs)

        # Choose a' from s' using policy derived from Q (epsilon-greedy)
        action_idx = epsilon_greedy_action(Q, epsilon, state_idx)

        steps = 0
        while (steps <= max_episode_len) & (not grid.absorbing[0, state_idx]):

            steps += 1

            # Take a step : take action a', observe reward and s'
            _, _, reward, state_prime_idx = grid.state_action_step(state_idx, action_idx)

            # Choose a' from s' using policy derived from Q (epsilon-greedy)
            action_prime_idx = epsilon_greedy_action(Q, epsilon, state_prime_idx)

            # Update Q function
            Q[state_idx, action_idx] += alpha * \
                    (reward + gamma * Q[state_prime_idx, action_prime_idx] - Q[state_idx, action_idx])

            # Update state, action
            state_idx, action_idx = state_prime_idx, action_prime_idx

        # Encourage exploration at first episodes
        epsilon = max(epsilon * 0.99995, 0.05)

    policy = Q.argmax(1)

    return Q, policy

def Q_learning(grid, num_episodes, start_loc=None,  max_episode_len=100, gamma=1.0, epsilon=1.0, alpha=0.1):

    # Init state-action function to zeros
    Q = np.zeros((grid.state_size, grid.action_size))

    for i in range(num_episodes):
        if start_loc == None:
        # Start at random location
            state_loc = random.choice(list(set(grid.locs) - set(grid.absorbing_locs)))
        else:
            state_loc = start_loc
        state_idx = grid.loc_to_state(state_loc, grid.locs)

        steps = 0
        while (steps <= max_episode_len) & (not grid.absorbing[0, state_idx]):

            steps += 1

            # Choose a' from s' using policy derived from Q (epsilon-greedy)
            action_idx = epsilon_greedy_action(Q, epsilon, state_idx)

            # Take a step : take action a', observe reward and s'
            _, _, reward, state_prime_idx = grid.state_action_step(state_idx, action_idx)

            # Update Q function (choose greedy action from s')
            Q[state_idx, action_idx] += alpha * \
                    (reward + gamma * Q[state_prime_idx].max() - Q[state_idx, action_idx])

            # Update state
            state_idx = state_prime_idx

        # Encourage exploration at first episodes
        epsilon = max(epsilon * 0.99995, 0.05)

    policy = Q.argmax(1)

    return Q, policy

def epsilon_greedy_policy(Q, epsilon):
    policy = np.zeros(Q.shape)
    best_actions = np.argmax(Q, 1)
    policy[range(Q.shape[0]), best_actions] = 1 - epsilon + epsilon / Q.shape[1]
    other_actions = [[i for i in range(Q.shape[1]) if i!= j] for j in best_actions]
    other_actions = np.array(other_actions).T
    policy[range(Q.shape[0]), other_actions] = epsilon / Q.shape[1]
    return policy

def epsilon_greedy_action(Q, epsilon, state_idx):

    if np.random.rand() < 1 - epsilon:
        # p(a = a*|s) = 1 - epsilon + epsilon / |A(s)|
        action_idx = Q[state_idx].argmax()
    else:
        # p(a = a', a'!= a*|s) = epsilon / |A(s)|
        action_idx = np.random.choice(range(Q.shape[1]))
    return action_idx

