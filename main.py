import random
import game
import environment
import agentMCTS

# main for playing tic tac toe games

# agent to play a random move
def agent_random(obs, config):
    moves = obs[3]
    return random.choice(moves)

game = game.NDgame(2,3)
env = environment.Environment(game)

print(env.run([agent_random, agent_random], display_end=True, print_moves=True))