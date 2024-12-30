import random
import game
import environment
import agentMCTS
import numpy as np
import matplotlib.pyplot as plt

def agent_random(obs, config):
    moves = obs[3]
    return random.choice(moves)

g = game.NDgame(2,3)
env = environment.Environment(g)
a = agentMCTS.Agent()

# Idea: can also change loop in env.run to just run width**dim times,
# then call it a draw afterwards

num_games = 10

explore_step_size = 10
max_explores = 300
explores_to_score = {}

for i in range(1, max_explores, explore_step_size):
    explores_to_score[i] = 0
    for j in range(0, num_games, 1):
        result = env.run([a.agent_mcts, agent_random], reset_before=True)
        explores_to_score[i] += result
        
        result = env.run([agent_random, a.agent_mcts], reset_before=True)
        explores_to_score[i] += 1 - result
    
plt.bar(explores_to_score.keys(), explores_to_score.values())
plt.show()
