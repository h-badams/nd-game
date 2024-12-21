import environment, nodeMCTS

# MCTS agent that stores tree information

'''
Want to try and make this as formal and abstract as possible
(so that this code works in a very general case)
The agent gets a game that has a current state - agent then
builds a tree w/ MCTS, picks the best move, and repeats
'''

class Agent:
    def __init__(self, current_tree=None, current_state=None):        
        # a node with the game state should be passed in
        self.current_tree = current_tree
        
        self.current_state = current_state
        
        self.explore_const = 1000
    
    def agent_mcts(self, obs, config):
        # if first time called, get the starting state and make a node
        if self.current_tree is None or obs[2] == 0 or obs[2] == 1:
            int_env = environment.Environment(config[0],config[1])
            int_env.board = obs[0]
            self.current_tree = nodeMCTS.Node(int_env, False, None, obs[1], True)
            self.current_state = obs[0]
        # if not, then figure out what the last move was and
        # prune your previous tree
        else:
            new_top = self.get_next_node(obs[0])
            
            if new_top is None:
                raise Exception(f"didn't find opponent's move in tree!")
            if not new_top.is_player_turn: # for testing purposed right now
                raise Exception("New node not player's turn - something is wrong")
            new_top.detach()
            self.current_tree = new_top
        
        for i in range(self.explore_const):
            self.current_tree.explore()
        
        next_top, next_move = self.current_tree.next()
        
        if not next_top.done: # wait, why do we need this check?
            next_top.detach()
            self.current_tree = next_top
        
        return next_move
    
    # chooses move opponent made in tree
    def get_next_node(self, current_board):
        for child in self.current_tree.children:
            if child.env.board == current_board:
                return child
