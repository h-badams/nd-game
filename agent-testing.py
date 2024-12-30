import random
import game
import environment
import agentMCTS
import numpy as np
import matplotlib.pyplot as plt

def agent_random(obs, config):
    moves = obs[3]
    return random.choice(moves)

g = game.NDgame(3,3)
env = environment.Environment(g)
a = agentMCTS.Agent()

num_games = 20

explore_step_size = 10
max_explores = 101
explores_to_score = {}

for i in range(10, max_explores, explore_step_size):
    a = agentMCTS.Agent(explore_const=i)
    explores_to_score[i] = -10
    for j in range(0, num_games, 2):
        
        result = env.run([a.agent_mcts, agent_random], reset_before=True)
        explores_to_score[i] += result
        
        result = env.run([agent_random, a.agent_mcts], reset_before=True)
        explores_to_score[i] += 1 - result
        
    print(f"completed {i} explores")
    
plt.bar(explores_to_score.keys(), explores_to_score.values())
plt.xlabel('Explores')
plt.ylabel('# Excess Wins (Out of 10)')
plt.title('Excess Wins vs. Explores, 3x3x3 TicTacToe')

plt.show()
