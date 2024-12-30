import game
import environment
import nodeMCTS

# MCTS agent that stores tree information

class Agent():
    def __init__(self, explore_const=5):
        self.tree = None
        self.explore_const = explore_const
    
    def agent_mcts(self, obs, config):
        current_board = obs[0]
        agent_mark = obs[1]
        current_turn = obs[2]
        
        dim, width = config
        
        # if starting a new game, make a new game tree with the current position
        if current_turn <= 1:
            g = game.NDgame(dim, width)
            int_env = environment.Environment(g)
            our_turn = True
            if current_turn == 1:
                our_turn = False
            self.tree = nodeMCTS.Node(agent_mark, int_env, done=False, is_player_turn=our_turn, parent=None)
        
        # determine the opponent's move with respect to previous game tree
        self.update_tree_from_opponent_move(current_board)
        
        if self.tree.is_player_turn == False:
            raise Exception("it isn't our turn")
        
        # do some number of explores
        for _ in range(self.explore_const):
            self.tree.explore()
            
        # pick the most visited node, and make that one the top node by deleting its parent
        next_top, next_move = self.tree.next()
            
        next_top.detach()
        self.tree = next_top
        
        return next_move
    
    # TODO method comment
    def update_tree_from_opponent_move(self, current_board):
        if self.tree.done:
            raise Exception("don't call this method on a finished game state")
        
        if self.tree.env.game.board == current_board:
            return
        
        if not self.tree.children:
            self.tree.create_children()
            
        found_child = False
        for child in self.tree.children:
            if child.env.game.board == current_board:
                self.tree = child
                del self.tree.parent
                self.tree.parent = None
                found_child = True
                break
        
        if not found_child:
            raise Exception("current board was not the child of previous game state")
            