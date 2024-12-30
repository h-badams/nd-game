import game
import environment
import nodeMCTS

'''
Tests to implement:
- Check that the tree expands correctly, i.e. that each child node has
    the proper number of moves, board state, etc
- TODO add more tests
'''

def print_tree(top_node):
    curr = top_node
    q = []
    q.append(curr)
    num_nodes = 1
    # do a bfs
    while q:
        to_print = q.pop(0) 
        print(to_print)
        children = to_print.children
        if children:
            for child in children:
                q.append(child)
                num_nodes += 1
                
    print(num_nodes)

g = game.NDgame(3, 3)
env = environment.Environment(g)
env.game.play_move((1,1,1), 1)

test_node = nodeMCTS.Node(2, env, done=False, is_player_turn=True, 
                          parent=None, action_played=None)

for i in range(50):
    test_node.explore()

print_tree(test_node)


        