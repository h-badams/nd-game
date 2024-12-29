import random
import game
import environment
import agentMCTS

# main for playing tic tac toe games

# agent to play a random move
def agent_random(obs, config):
    moves = obs[3]
    return random.choice(moves)

def agent_player(obs, config):
    if config[0] != 2:
        raise Exception("visualization in 3d+ has not been implemented yet!")
    else:
        print(*obs[0])
    
    legal_moves = obs[2]
    while True:
        move = []
        for i in range(config[1]):
            component = int(input(f"component {i+1}:"))
            move.append(component)
        if tuple(move) in legal_moves:
            break
        else:
            print("illegal move, try again")
            
    return tuple(move)
            
game = game.NDgame(2,3)
env = environment.Environment(game)

a = agentMCTS.Agent()

env.run([a.agent_mcts, agent_random], display_end=True)
env.run([a.agent_mcts, agent_random], display_end=True)

env.run([a.agent_mcts, agent_random], display_end=True)

# print(env.run([agent_random, agent_random], display_end=True, print_moves=True))
# env.run([agent_player, agent_random])