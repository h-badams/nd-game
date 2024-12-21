# Node in the Monte Carlo Tree

from numpy import sqrt, log
import copy
import random

class Node:
    
    def __init__(self, env, done, parent, player_mark, is_player_turn, action_played=None):
        
        # child nodes - should end up as a list
        self.children = None
        
        # if the node is "for" player 1 or 2
        self.player_mark = player_mark
        
        # times visited / total reward
        self.N = 0
        self.T = 0
        
        # possibly bad design - stores game state
        self.env = env
        
        # if game is over - boolean
        self.done = done
        
        # parent node
        self.parent = parent
        
        self.is_player_turn = is_player_turn
        
        self.action_played = action_played
        
        # self.c = sqrt(2) # In practice this is suboptimal for tictactoe, I think
        self.c = 0.6
        
    def uct_score(self):
        
        if self.N == 0:
            #return float('inf')
            return 1000000
        
        top_node = self
        # if node is not top, go up one node
        if top_node.parent:
            top_node = top_node.parent
        
        # adding the exploitation/exploration terms
        return (self.T / self.N) + (self.c * sqrt(log(top_node.N) / self.N))
    
    def turn_to_mark(self):
        if self.is_player_turn:
            return self.player_mark
        else:
            if self.player_mark == 1:
                return 2
            elif self.player_mark == 2:
                return 1
                
    def create_children(self):
        if self.done:
            return
    
        actions = self.env.get_legal_moves()
        children = []
        
        for i in range(len(actions)):
            # TODO change self.done to what it should be
            # TODO currently I believe all the moves are being played as one mark or the other - this needs to be fixed
            new_env = copy.deepcopy(self.env)
            new_env.play_move(actions[i], self.turn_to_mark())
            
            if actions is None or actions[i] is None:
                raise Exception("actions i should never be none")
            
            new_done = False
            if new_env.is_winner(actions[i]) or new_env.is_tie():
                new_done = True
        
            children.append(Node(new_env, new_done, self, self.player_mark, not self.is_player_turn, action_played=actions[i]))
        
        self.children = children
        
    def explore(self):
        
        # go down tree, choosing max uct
        
        current = self
        
        while current.children:
            children = current.children
            max_score = max(c.uct_score() for c in children)
            candidate_nodes = [c for c in children if c.uct_score() == max_score]
            new_child = random.choice(candidate_nodes)
            current = new_child
            
        # either rollout or create children / expand
        
        if current.done:
            result = current.env.get_winner(current.action_played)
            if result == self.player_mark:
                current.T += 1
            elif result == 0:
                current.T += 0.5
        elif current.N < 1:
            current.T += current.rollout()
        else:
            current.create_children()
            current = random.choice(current.children)
            
            # pasting the same code block but I'll figure out
            # a better solution later
            if current.done:
                result = current.env.get_winner(current.action_played)
                if result == self.player_mark:
                    current.T += 1
                elif result == 0:
                    current.T += 0.5
            else:
                current.T += current.rollout()
            
        current.N += 1

        # update stats / backprop
        
        parent = current 
        
        # TODO pretty sure this section is incorrect - should be updating every other node
        
        while parent.parent:
            parent = parent.parent
            parent.N += 1
            parent.T += current.T # current isn't updated in the loop, so it will always be 0/1
            
    def rollout(self):
        # idea: playout in env with random agents
        new_env = copy.deepcopy(self.env)
        result = new_env.run([agent_random, agent_random])
        if result == 0:
            return 0.5
        if result == self.player_mark:
            return 1
        return 0
    
    # returns the node and the associated action
    def next(self):
        # error if no child nodes or if game is over
        if self.children is None or self.done:
            raise Exception("illegal state for next method")
        
        max_N = max(c.N for c in self.children)
        max_children = [c for c in self.children if c.N == max_N]
        choice = random.choice(max_children)
        return choice, choice.action_played
    
    # removes everything above the node
    def detach(self):
        del self.parent
        self.parent = None

    # returns a string with the node's move, visit & win counts
    def __str__(self):
        return f"(N: {self.N}, T: {self.T}, {self.action_index})"
    
# this "agent" is really useful for concisely writing rollout code
def agent_random(obs, config):
    legal_moves = []
    board = obs[0]
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 0:
                legal_moves.append((row,col))
    return random.choice(legal_moves)
