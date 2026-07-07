# Running this program solves the Deterministic Windy Gridworld with SARSA, then with Q-learning.
# Then it solves the Stochastic Windy Gridworld with King's Moves with SARSA, then with Q-learning.
# We could put SARSA and Q-learning into one method and could run certain lines depending on if a parameter tells us its SARSA or Q-learning
# we could also make the allowedActions method look nicer and be more efficient

import numpy as np
import random
import time
import matplotlib.pyplot as plt

class World:
    def __init__(self, kingBool): # if kingBool is True, the agent can use King's moves, else it can only move N, S, E, W
        self.gridWidth = 10
        self.gridHeight = 7
        self.startPos = (3,0)
        self.currentPos = self.startPos
        self.goalPos = (3,7)
        self.windVals = [0,0,0,1,1,1,2,2,1,0]
        self.king = kingBool

    def movePosition(self, action): # moves the agent to a new position based on the chosen action, and returns the new position and the reward
        newPos = np.add(list(self.currentPos), list(action))

        if(self.king): # if the agent is using King's Moves, the wind is stochastic
            windProbability = random.randint(1,3)
        else:
            windProbability = 1

        temp = newPos[0] - self.windVals[list(self.currentPos)[1]]

        if(windProbability == 2):
            temp -= 1
        elif(windProbability == 3):
            temp += 2

        # if it goes outisde the grid bc of the wind, make the new position be just inside where it would have gone off
        if(temp < 0):
            newPos[0] = 0
        elif(temp >= self.gridHeight):
            newPos[0] = self.gridHeight - 1

        if(newPos[0] == list(self.goalPos)[0] and newPos[1] == list(self.goalPos)[1]):
            reward = 1
        else:
            reward = -1

        return [(newPos[0], newPos[1]), reward]

    def allowedActionsFromPos(self, position): # not allowing agent to move off grid, unless because of wind
        allowedMoves = []
        if(position[0] != 0):
            allowedMoves.append((-1,0))
        if(position[0] != self.gridHeight - 1):
            allowedMoves.append((1,0))
        if(position[1] != self.gridWidth - 1):
            allowedMoves.append((0,1))
        if(position[1] != 0):
            allowedMoves.append((0,-1))
        if(self.king): # append the correct diagonal actions to the allowedMoves lsit
            allowedMoves.append((1,1))
            allowedMoves.append((-1,1))
            allowedMoves.append((1,-1))
            allowedMoves.append((-1,-1))
            if(position == (0,0)): # top left
                allowedMoves.remove((-1,-1))
                allowedMoves.remove((-1,1))
                allowedMoves.remove((1,-1))
            elif(position == (0, self.gridWidth - 1)): # top right (0,9)
                allowedMoves.remove((-1,-1))
                allowedMoves.remove((-1,1))
                allowedMoves.remove((1,1))
            elif(position == (self.gridHeight - 1, 0)): # bottom left (6,0)
                allowedMoves.remove((-1,-1))
                allowedMoves.remove((1, -1))
                allowedMoves.remove((1, 1))
            elif(position == (self.gridHeight - 1, self.gridWidth - 1)): # bottom right (6,9)
                allowedMoves.remove((1,-1))
                allowedMoves.remove((1,1))
                allowedMoves.remove((-1,1))
            else:
                if(position[1] == self.gridWidth - 1):
                    allowedMoves.remove((-1,1))
                    allowedMoves.remove((1,1))
                if(position[1] == 0):
                    allowedMoves.remove((-1,-1))
                    allowedMoves.remove((1,-1))
                if(position[0] == 0):
                    allowedMoves.remove((-1,1))
                    allowedMoves.remove((-1,-1))
                if(position[0] == self.gridHeight - 1):
                    allowedMoves.remove((1,1))
                    allowedMoves.remove((1,-1))

        return allowedMoves

class Agent:
    def __init__(self, a, e, world: World):
        self.alpha = a # learning rate
        self.epsilon = e # the percent you want to explore
        self.world = world
        self.gamma = 0.9
        self.Q_values = self.createQTable()
        self.numOfSteps = 0

    def createQTable(self):
        QTable = {} # dictionary where each key is a state that holds a differnt number of possible actions, each which has a q-value
        for x in range(self.world.gridHeight):
            for y in range(self.world.gridWidth):
                position = (x,y)
                QTable[position] = {}
                allowedActions = self.world.allowedActionsFromPos(position)
                for action in allowedActions:
                    QTable[position][action] = 0
        return QTable

    def getBestAction(self, position):
        maxVal = np.NINF
        maxAction = None
        for action, value in self.Q_values[position].items():
            if value > maxVal:
                maxVal = value
                bestAction = action
        return bestAction

    def chooseAction(self, position):
        allowedActions = list(self.Q_values[position].keys()) # go to the dictionary and get the actions allowed in this state
        possibleNextState = self.world.startPos # just to initialize it, we know it will go into loop
        action = None # initializing the return

        randomNum = np.random.rand()
        # this is the epsilon-greedy policy:
        if(randomNum < self.epsilon):
            subOptimalActionChoiceIndex = random.randint(0, len(allowedActions) - 1)
            action = allowedActions[subOptimalActionChoiceIndex]
        else:
            action = self.getBestAction(position)
        possibleNextState = np.add(list(position), list(action))
        temp = possibleNextState[0] - self.world.windVals[list(possibleNextState)[1]]

        if(temp >= 0):
            possibleNextState[0] = temp

        possibleNextState = (possibleNextState[0], possibleNextState[1])

        return action

    def SARSA(self):
        self.world.currentPos = self.world.startPos
        visited = [] # initalize
        actionsTaken = []
        visited.append(self.world.startPos) # put the first state into it to say we visited it
        chosenAction = self.chooseAction(self.world.currentPos) # choose a random action from (3,0)
        newPosAndReward = None # initialize
        converged = True

        while True: # loop for each step of the episode
            # Take action A, observe R and S'
            newPosAndReward = self.world.movePosition(chosenAction) # move the agent to a new position based on the chosen action
            newPosition = (newPosAndReward[0][0], newPosAndReward[0][1]) # get the reward and new position from that chosen action
            reward = newPosAndReward[1]
            visited.append(newPosition) # say we vsited that state
            actionsTaken.append(chosenAction)
            self.numOfSteps += 1
            # Choose A' from S' using epislon-greedy policy
            nextAction = self.chooseAction(newPosition) # choose an action that is possible from the new position based on the epislon greedy method

            oldQ = self.Q_values[self.world.currentPos][chosenAction]

            # Update the Q-value of the current position
            self.Q_values[self.world.currentPos][chosenAction] += self.alpha * (reward + self.gamma * self.Q_values[newPosition][nextAction] - self.Q_values[self.world.currentPos][chosenAction]) # perform the update

            if(abs(oldQ - self.Q_values[self.world.currentPos][chosenAction]) > self.epsilon):
                converged = False

            # advance to the next state and action
            self.world.currentPos = newPosition # make current position be the new position, and action be the chosen action that we executed
            chosenAction = nextAction

            if(self.world.currentPos == self.world.goalPos): # if the next state is the goal, break
                    break

        return converged, visited, actionsTaken

    def Qlearning(self):
        self.world.currentPos = self.world.startPos
        visited = []
        actionsTaken = []
        visited.append(self.world.startPos)
        newPosAndReward = None # initialize
        converged = True

        while True: # loop for each step of the episode
            # Choose A from S using the epislon-greedy policy
            chosenAction = self.chooseAction(self.world.currentPos)
            # Take A and observe R and S'
            newPosAndReward = self.world.movePosition(chosenAction)
            newPosition = newPosAndReward[0]
            reward = newPosAndReward[1]
            visited.append(newPosition) # say we vsited that state
            actionsTaken.append(chosenAction)
            self.numOfSteps += 1
            # find best action from S'
            bestAction = self.getBestAction(newPosition)

            oldQ = self.Q_values[self.world.currentPos][chosenAction]

            # update current state q-value
            self.Q_values[self.world.currentPos][chosenAction] += self.alpha * (reward + self.gamma * self.Q_values[newPosition][bestAction] - self.Q_values[self.world.currentPos][chosenAction]) # perform the update

            if(abs(oldQ - self.Q_values[self.world.currentPos][chosenAction]) > self.epsilon):
                converged = False

            # advance to the next state
            self.world.currentPos = newPosition

            if(self.world.currentPos == self.world.goalPos): # if the next state is the goal, break
                    break

        return converged, visited, actionsTaken

def main():
    # Runs regular SARSA
    testWorld = World(False)
    testAgent = Agent(0.9, 0.001, testWorld)
    timeSteps = [0]
    episodes = [0]
    convergedX = []
    convergedY = []
    alreadyConverged = False
    for x in range(170): # the max number of episodes
        result = testAgent.SARSA()
        timeSteps.append(testAgent.numOfSteps)
        episodes.append(x)
        if(result[0] and not alreadyConverged):
            print("Found the optimal policy using SARSA. The path is...")
            print(result[1])
            print("The actions taken on that path are...")
            print(result[2])
            convergedX.append(x)
            convergedY.append(testAgent.numOfSteps)
            alreadyConverged = True

    plt.plot(timeSteps, episodes, 'r--', convergedY, convergedX, 'bs')
    plt.suptitle("SARSA")
    plt.xlabel("Total Timesteps")
    plt.ylabel("Episodes")
    plt.show()

    #Runs regular Q-learning
    testWorld = World(False)
    testAgent = Agent(0.9, 0.01, testWorld)
    timeSteps = [0]
    episodes = [0]
    convergedX = []
    convergedY = []
    alreadyConverged = False
    for x in range(170): # the max number of episodes
        result = testAgent.Qlearning()
        timeSteps.append(testAgent.numOfSteps)
        episodes.append(x)
        if(result[0] and not alreadyConverged):
            print("Found the optimal policy using Q-learning. The path is...")
            print(result[1])
            print("The actions taken on that path are...")
            print(result[2])
            convergedX.append(x)
            convergedY.append(testAgent.numOfSteps)
            alreadyConverged = True

    plt.plot(timeSteps, episodes, 'r--', convergedY, convergedX, 'bs')
    plt.suptitle("Q-learning")
    plt.xlabel("Total Timesteps")
    plt.ylabel("Episodes")
    plt.show()

    # Runs SARSA with King's Moves
    testWorld = World(True)
    testAgent = Agent(0.9, 0.01, testWorld)
    timeSteps = [0]
    episodes = [0]
    convergedX = []
    convergedY = []
    alreadyConverged = False
    for x in range(170): # the max number of episodes
        result = testAgent.SARSA()
        timeSteps.append(testAgent.numOfSteps)
        episodes.append(x)
        if(result[0] and not alreadyConverged):
            print("Found the optimal policy using SARSA, King's Moves, and stochastic winds. The path is...")
            print(result[1])
            print("The actions taken on that path are...")
            print(result[2])
            convergedX.append(x)
            convergedY.append(testAgent.numOfSteps)
            alreadyConverged = True

    plt.plot(timeSteps, episodes, 'r--', convergedY, convergedX, 'bs')
    plt.suptitle("SARSA - King's Moves")
    plt.xlabel("Total Timesteps")
    plt.ylabel("Episodes")
    plt.show()

    # Runs Q-learning with King's Moves
    testWorld = World(True)
    testAgent = Agent(0.9, 0.01, testWorld)
    timeSteps = [0]
    episodes = [0]
    convergedX = []
    convergedY = []
    alreadyConverged = False
    for x in range(170): # the max number of episodes
        result = testAgent.Qlearning()
        timeSteps.append(testAgent.numOfSteps)
        episodes.append(x)
        if(result[0] and not alreadyConverged):
            print("Found the optimal policy using Q-learning, King's Moves, and stochastic winds. The path is...")
            print(result[1])
            print("The actions taken on that path are...")
            print(result[2])
            convergedX.append(x)
            convergedY.append(testAgent.numOfSteps)
            alreadyConverged = True

    plt.plot(timeSteps, episodes, 'r--', convergedY, convergedX, 'bs')
    plt.suptitle("Q-learning - King's Moves")
    plt.xlabel("Total Timesteps")
    plt.ylabel("Episodes")
    plt.show()

if __name__ == '__main__':
    main()