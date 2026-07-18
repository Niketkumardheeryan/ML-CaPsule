# Q-Learning-From-Scratch
Implements Q-learning a form of Reinforcement Learning on a simulation on OpenAI Gymnasium from scratch!!

## What is Q-learning?

**Q-learning** is a model-free, off-policy reinforcement learning (RL) algorithm that learns the **optimal action-value function** $Q^*(s,a)$ for a Markov Decision Process (MDP). By iteratively updating estimates of how good it is to take an action $a$ in state $s$, it converges (under mild conditions) to the optimal policy that maximizes long-term expected reward.

---

## When should I use it?

Use Q-learning when:

* The state and action spaces are **small/discrete** (so a table fits in memory), or you can discretize reasonably.
* You **don’t** have (or don’t want) a dynamics model (transition probabilities).
* You want a **simple**, proven method to get a baseline or solve gridworld-like tasks, tabular control, or MDP toys.

If your problem has large/continuous spaces, prefer **function approximation** (e.g., DQN) or **policy-gradient** families.

---

## Key RL concepts (brief)

* **MDP:** Defined by states $\mathcal{S}$, actions $\mathcal{A}$, transition dynamics $P(s'\mid s,a)$, reward $R(s,a)$, and discount $\gamma \in [0,1)$.
* **Policy ($\pi$)**: A mapping from states to actions (deterministic or stochastic).
* **Optimal Q:** The greedy policy that maximizes returns.
* **Exploration vs. Exploitation:** Trade off trying new actions (explore) versus taking the best-known action (exploit). A common strategy is **$\epsilon$-greedy**.

---

## The Q-learning update (Bellman optimality)

After observing a transition $(s_t, a_t, r_{t+1}, s_{t+1})$, Q-learning performs:

$$
Q(s_t, a_t) \leftarrow Q(s_t, a_t) + \alpha \Big( r_{t+1} + \gamma \max_{a'} Q(s_{t+1}, a') - Q(s_t, a_t) \Big)
$$

Where:

* $\alpha$ is the learning rate (e.g., 0.1).
* $\gamma$ is the discount factor (e.g., 0.95).
* The target uses **$\max$** over next-state actions → **off-policy** (target is the greedy action regardless of the behavior policy).

  NOTE:- In the given code too the same formula has been used just the current-state's Q-value has been clubbed together 

---

## Algorithm ($\epsilon$-greedy tabular)

1. Initialize Q(s,a) arbitrarily (often zeros) for all states and actions.
2. **For each episode:**

   * Initialize state s.
   * **Loop** (until terminal):

     * With probability $\epsilon$, pick a random action; otherwise $\arg\max_a Q(s,a)$.
     * Execute action, observe reward r and next state $s'$.
     * Update Q using the formula above.
     * Set $s \leftarrow s'$.
3. Optionally **anneal** $\epsilon$ from high to low for exploration early, exploitation later.

---



**Notes:**

* The reward shaping (small step cost, big goal reward) encourages shorter paths.
* Annealing $\epsilon$ helps the agent explore early, then exploit later.


## Variants & relatives

* **SARSA (on-policy):** Update uses the *action actually taken next*: $r + \gamma Q(s',a')$. Safer near risky states (less overestimation), but may be more conservative.
* **Expected SARSA:** Uses expectation over next actions: $r + \gamma \mathbb{E}_{a'\sim\pi}[Q(s',a')]$.
* **Double Q-learning:** Reduces overestimation bias via two Q-tables.
* **DQN (Deep Q-Network):** Replaces the table with a neural network; adds target networks and experience replay.

---

## Common pitfalls

* **Insufficient exploration:** Agent gets stuck exploiting suboptimal early values.
* **Non-stationary rewards/dynamics:** Tabular Q-learning assumes stationary MDP.
* **Huge/continuous spaces:** The table explodes; use function approximation.
* **Learning rate too high/low:** Too high → oscillations; too low → slow learning.
* **Bootstrapping from terminal states:** Don’t include $\max_{a'} Q(s', a')$ if $s'$ is terminal.


## Overview Of the `CarMountain` Program:-

The program trains an agent using **Q-learning** to solve the **MountainCar-v0** environment from [Gymnasium](https://gymnasium.farama.org/). In this problem,a car is stuck between two hills and must build enough momentum to reach the flag on top of the right hill.
Since the environment has a **continuous state space** (position and velocity), the program discretizes it into a grid and applies tabular Q-learning.

---

## Step-by-step procedure

### 1. **Environment setup**

```python
env = gym.make('MountainCar-v0')
```

The agent interacts with the MountainCar environment. The observation space has two values (position, velocity) and the action space has three values (push left, no push, push right).

---

### 2. **Discretizing the state space**

The environment states are continuous, so they are mapped into discrete bins:

```python
table_size = (20, 20)
window_size = (env.observation_space.high - env.observation_space.low) / table_size
```

* The continuous space is split into a **20x20 grid**.
* `get_discrete_state(state, window_size)` converts a continuous state into an integer index for the Q-table.

---

### 3. **Initialize Q-table**

```python
q_table = np.random.uniform(low=0, high=1, size=(20, 20, env.action_space.n))
```

* Q-table dimensions = `(position_bins, velocity_bins, actions)`.
* Initially filled with random values in \[0,1].

---

### 4. **Training parameters**

* **Learning rate (α):** 0.1 → how much new info overrides old.
* **Discount factor (γ):** 0.95 → importance of future rewards.
* **Exploration rate (ε):** starts at 1.0 → decays gradually to 0.01.
* **Episodes:** 60,000 → each one is an attempt to solve the task.
* **Step limit per episode:** 120.

---

### 5. **Episode loop**

For each episode:

1. Reset environment → get initial state.
2. Discretize the state.
3. Loop until **done** (goal reached or max steps):

   * Choose an action:

     * With probability ε → random action (**exploration**).
     * Otherwise → greedy action (**exploitation**) based on Q-table.
   * Perform action → observe `(new_state, reward, done)`.
   * Discretize the new state.
   * Update Q-table using the Q-learning rule:

     ```python
     new_q = (1 - α) * current_q + α * (reward + γ * max_future_q)
     ```
   * If the goal is reached, set Q-value to 0 and mark episode done.
   * Accumulate reward and continue.
4. After each episode, **decay ε** to reduce exploration over time.

---

### 6. **Reward tracking**

```python
reward_list.append(total_reward)
sn.lineplot(reward_list)
```

* Stores the total reward per episode.
* Plots a reward curve to visualize learning progress.

---

### 7. **Evaluation (post-training)**

```python
eval_env = gym.make('MountainCar-v0', render_mode='rgb-space')
```

* A fresh environment is created with rendering enabled.
* The agent **always takes the greedy action** (no exploration).
* The car should reliably reach the goal after training.

---

## Workflow summary

1. Discretize continuous state space.
2. Initialize Q-table.
3. Train agent for many episodes:

   * Explore early, exploit later.
   * Update Q-values after each step.
4. Plot reward curve.
5. Run a final evaluation with the trained policy.

---

## Output

* **Console messages:** When the goal is reached during training (episode and step count).
* **Reward curve plot:** Shows improvement over episodes.
* **Rendered environment:** After training, the car reaches the goal in the visualization window.

---

## Overview Of the `CliffWalking` Program:-
## Key details of the environment

* **State space:** 48 discrete states (a 4x12 grid).
* **Action space:** 4 discrete actions (up, down, left, right).
* **Start:** bottom-left corner.
* **Goal:** bottom-right corner (state 37 in this implementation).
* **Cliff region:** cells between start and goal on the bottom row. Stepping here yields large negative reward and episode termination.

---

## Q-table initialization

```python
q_table = np.random.uniform(low=0, high=1, size=(48, 4))
```

* One row per state (48).
* One column per action (4).
* Initialized with random values.

---

## Training loop

For **10,000 episodes**, the agent learns by trial and error:

1. Reset the environment to get the starting state.
2. While the episode is not finished (or step < 50):

   * Select action:

     * With probability ε → random action (exploration).
     * Otherwise → action with highest Q-value for that state (exploitation).
   * Perform the action → observe `(new_state, reward, done)`.
   * Update Q-table using the Q-learning rule.
   * If the goal (state 37) is reached → set Q-value to 0 and mark episode as done.
3. Accumulate rewards and decay ε to encourage exploitation over time.

---

## Reward tracking

After each episode, the total reward is stored. At the end:

```python
sn.lineplot(reward_list)
plt.title('Reward per episode')
```

A curve of rewards per episode is plotted to visualize learning progress.

---

## Evaluation

A fresh environment with rendering is created:

```python
eval_env = gym.make('CliffWalking-v1', render_mode='rgb-space')
```

* The agent acts greedily using the trained Q-table.
* The agent should learn to avoid the cliff and reach the goal.
* The process is displayed in the render window.

---

## Output

* **Console logs:** Messages when the agent successfully reaches the goal.
* **Plot:** Reward per episode curve.
* **GIF Output:** Visualization of the final policy navigating the gridworld.

---

---

## Screenshots
<img width="616" height="476" alt="reward_episodes" src="https://github.com/user-attachments/assets/85c773da-50ab-4ed2-b3f6-8ecf72ba3d4d" />
<img width="608" height="411" alt="car_mountain_result" src="https://github.com/user-attachments/assets/1628ef5c-2df2-47f2-adda-85af6946f66b" />
<img width="734" height="248" alt="cliff_walking_output" src="https://github.com/user-attachments/assets/189fcaee-0c51-4952-9e50-a228ae4e13bd" />



---


## Notes

* Unlike MountainCar, **CliffWalking already has discrete states**, so no discretization is needed.
* The main challenge is balancing exploration so the agent doesn’t keep falling into the cliff.



## Notes

* These programs use **tabular Q-learning with discretization** — simple but effective for MountainCar and CliffWalking.
* More advanced approaches (e.g., **Deep Q-Networks**) can handle continuous spaces without manual discretization.

## Credits and Resources (Would really recommend sentdex's channel for beginners as he covers topics from depth and has a hands-on approach):-
* <a href="https://www.youtube.com/@sentdex"> sentdex's Youtube Channel</a>
* <a href="https://youtube.com/playlist?list=PLQVvvaa0QuDezJFIOU5wDdfy4e9vdnx-7&si=wTjdTWFRgLiwK_nV"> sentdex's Reinforcement Learning Playlist </a>


