import random
import game
import environment
import agentMCTS
import numpy as np
import matplotlib.pyplot as plt

def agent_random(obs, config):
    moves = obs[3]
    return random.choice(moves)

game = game.NDgame(2,4)
env = environment.Environment(game)
a = agentMCTS.Agent()

num_games = 10

explore_step_size = 3
max_explores = 30
histogram_data = []

for i in range(1, max_explores, explore_step_size):
    agent_mcts_wins = 0
    for j in range(0, num_games, 1):
        result = env.run([a.agent_mcts, agent_random])
        if result == 1:
            agent_mcts_wins += 1
            histogram_data.append(i)
        '''result = env.run([agent_random, a.agent_mcts])
        if result == 0:
            agent_mcts_wins += 1
            histogram_data.append(i)'''
            
print(np.array(histogram_data))
plt.hist(np.array(histogram_data))
plt.show()
