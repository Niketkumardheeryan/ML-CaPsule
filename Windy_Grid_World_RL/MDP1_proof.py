import numpy as np


class gridworld:

    def __init__(self, dim1, dim2):
        # add dim1 and dim2 to self for future use
        self.dim1 = dim1
        self.dim2 = dim2

        # dimensions of the environment
        self.dim = [dim1, dim2]

        # Define starting position
        self.start = [0, 0]
        self.s = self.start[:]
        self.reward = 0
        self.n = 0

        # N/North, S/South, E/East, W/West
        self.action_space = ["N", "S", "E", "W"]
        self.action_prob = [0.25, 0.25, 0.25, 0.25]

    def special_states(self, a_pos_x, a_pos_y, a_reward, a_trans_x, a_trans_y, b_pos_x, b_pos_y, b_reward, b_trans_x,
                       b_trans_y):
        # index starts at 0
        self.pos_A = [a_pos_x, a_pos_y]
        self.rew_A = a_reward
        self.trans_A = [a_trans_x, a_trans_y]

        self.pos_B = [b_pos_x, b_pos_y]
        self.rew_B = b_reward
        self.trans_B = [b_trans_x, b_trans_y]

    # evaluate actions and rewards
    def action(self, a):
        if a not in self.action_space:
            return "Error: Invalid action"

        # Special transition states
        if self.s == self.pos_A:
            self.s = self.trans_A[:]
            self.reward = self.rew_A
        elif self.s == self.pos_B:
            self.s = self.trans_B[:]
            self.reward = self.rew_B

        # Move North
        elif a == "N" and self.s[0] > 0:
            self.s[0] -= 1
            self.reward = 0

        # Move West
        elif a == "W" and self.s[1] > 0:
            self.s[1] -= 1
            self.reward = 0

        # Move South
        elif a == "S" and self.s[0] < self.dim[0] - 1:
            self.s[0] += 1
            self.reward = 0

        # Move East
        elif a == "E" and self.s[1] < self.dim[1] - 1:
            self.s[1] += 1
            self.reward = 0
        else:
            self.reward = -1
        self.n += 1
        return self.s, self.reward

    def reset(self):
        self.s = self.start
        self.reward = 0
        self.n = 0

    # state value matrix
    # takes instance specific discount factor (gamma)
    def sv_table(self, gamma):
        v = np.zeros(self.dim)
        delta = 1e-5
        delta_t = 1

        while delta_t > delta:
            # create new empty matrix
            v_new = np.zeros(self.dim)
            for m in range(self.dim[0]):
                for n in range(self.dim[1]):
                    for action in self.action_space:
                        # coordinates on grid
                        self.s = [m, n]
                        s, r = self.action(action)
                        prob = self.action_prob[self.action_space.index(action)]
                        v_new[m, n] += prob * (r + gamma * v[s[0], s[1]])
                        # checks if the results of the latest calculation are significantly different
            delta_t = np.sum(np.abs(v - v_new))
            v = v_new.copy()

        return v


def main():
    # 5by5
    dim1 = 5
    dim2 = 5
    # A (1,2), it moves to cell A’ (5,2) and receives a reward +10
    a_pos_x = 0
    a_pos_y = 1
    a_reward = 10
    a_trans_x = 4
    a_trans_y = 1
    # B (1,4) it moves to cell B’ (3,4) and receives a reward +5
    b_pos_x = 0
    b_pos_y = 3
    b_reward = 5
    b_trans_x = 2
    b_trans_y = 3
    # discount rate 85
    gamma = 0.85

    grid = gridworld(
        dim1=dim1,
        dim2=dim2
    )
    grid.special_states(
        a_pos_x=a_pos_x,
        a_pos_y=a_pos_y,
        a_reward=a_reward,
        a_trans_x=a_trans_x,
        a_trans_y=a_trans_y,
        b_pos_x=b_pos_x,
        b_pos_y=b_pos_y,
        b_reward=b_reward,
        b_trans_x=b_trans_x,
        b_trans_y=b_trans_y
    )

    condition1 = grid.sv_table(gamma=gamma).round(1)
    print("The 5x5 matrix with a discount rate of 85:")
    print(condition1)

    # 5by5
    dim1 = 5
    dim2 = 5
    # A (1,2), it moves to cell A’ (5,2) and receives a reward +10
    a_pos_x = 0
    a_pos_y = 1
    a_reward = 10
    a_trans_x = 4
    a_trans_y = 1
    # B (1,4) it moves to cell B’ (3,4) and receives a reward +5
    b_pos_x = 0
    b_pos_y = 3
    b_reward = 5
    b_trans_x = 2
    b_trans_y = 3
    # discount rate 75
    gamma = 0.75

    grid = gridworld(
        dim1=dim1,
        dim2=dim2
    )
    grid.special_states(
        a_pos_x=a_pos_x,
        a_pos_y=a_pos_y,
        a_reward=a_reward,
        a_trans_x=a_trans_x,
        a_trans_y=a_trans_y,
        b_pos_x=b_pos_x,
        b_pos_y=b_pos_y,
        b_reward=b_reward,
        b_trans_x=b_trans_x,
        b_trans_y=b_trans_y
    )

    condition2 = grid.sv_table(gamma=gamma).round(1)
    print("The 5x5 matrix with a discount rate of 75:")
    print(condition2)

    # 7by7
    dim1 = 7
    dim2 = 7
    # A is located in (3,2), A’ in (7,2)) and receives a reward +10
    a_pos_x = 2
    a_pos_y = 1
    a_reward = 10
    a_trans_x = 6
    a_trans_y = 1
    #  B in (1,6) and B’ in (4,6)) and receives a reward +5
    b_pos_x = 0
    b_pos_y = 5
    b_reward = 5
    b_trans_x = 3
    b_trans_y = 5
    # discount rate 85
    gamma = 0.85

    grid = gridworld(
        dim1=dim1,
        dim2=dim2
    )
    grid.special_states(
        a_pos_x=a_pos_x,
        a_pos_y=a_pos_y,
        a_reward=a_reward,
        a_trans_x=a_trans_x,
        a_trans_y=a_trans_y,
        b_pos_x=b_pos_x,
        b_pos_y=b_pos_y,
        b_reward=b_reward,
        b_trans_x=b_trans_x,
        b_trans_y=b_trans_y
    )

    condition3 = grid.sv_table(gamma=gamma).round(1)
    print("The 7x7 matrix with a discount rate of 85:")
    print(condition3)

    # 7by7
    dim1 = 7
    dim2 = 7
    # A is located in (3,2), A’ in (7,2)) and receives a reward +10
    a_pos_x = 2
    a_pos_y = 1
    a_reward = 10
    a_trans_x = 6
    a_trans_y = 1
    #  B in (1,6) and B’ in (4,6)) and receives a reward +5
    b_pos_x = 0
    b_pos_y = 5
    b_reward = 5
    b_trans_x = 3
    b_trans_y = 5
    # discount rate 75
    gamma = 0.75

    grid = gridworld(
        dim1=dim1,
        dim2=dim2
    )
    grid.special_states(
        a_pos_x=a_pos_x,
        a_pos_y=a_pos_y,
        a_reward=a_reward,
        a_trans_x=a_trans_x,
        a_trans_y=a_trans_y,
        b_pos_x=b_pos_x,
        b_pos_y=b_pos_y,
        b_reward=b_reward,
        b_trans_x=b_trans_x,
        b_trans_y=b_trans_y
    )

    condition4 = grid.sv_table(gamma=gamma).round(1)
    print("The 7x7 matrix with a discount rate of 75:")
    print(condition4)


if __name__ == "__main__":
    main()