import numpy as np
import random
import copy

# Node in the Monte Carlo Tree
# An overview of the algorithm used can be found at:
# https://en.wikipedia.org/wiki/Monte_Carlo_tree_search

class Node():
    def __init__(self, player_mark, env, done, is_player_turn, parent=None, action_played=None, result=None):
        self.children = None
        self.player_mark = player_mark
        self.N = 0
        self.T = 0
        self.env = env
        self.done = done
        self.parent = parent
        self.is_player_turn = is_player_turn
        self.action_played = action_played
        self.result = result # stores the 'objective result' - i.e. it stores 1 iff X wins
                
        # exploration const - experiment with this
        self.c = 1.41
    
    # TODO method comment
    
    def uct_score(self):
        sign = 1
        if not self.is_player_turn:
            sign *= -1
        
        if self.N == 0:
            return 1e6
        
        top_node = self
        if self.parent:
            top_node = top_node.parent
        
        # flipping the sign of the UCT score on opponent nodes is
        # equivalent to minmaxing when traversing the game tree
        return sign * (self.T / self.N) + (
            self.c * np.sqrt(np.log(top_node.N) / self.N))
    
    # TODO write test for this method
    
    # return 1 if the current node winds the rollout,
    # 0 for loss, 0.5 for tie
    def rollout(self):
        new_env = copy.deepcopy(self.env)
        result = new_env.run([agent_random, agent_random])
        if self.turn_to_mark() == 1:
            return result
        if self.turn_to_mark() == 2:
            return 1 - result
    
    # TODO method comment
    def create_children(self):
        if self.done:
            raise Exception("can't create children at a finished game node")
        
        actions = self.env.game.get_legal_moves()
        children = []
        
        if not actions:
            raise Exception("actions shouldn't be empty!")
        
        for action in actions:
            
            if not action:
                raise Exception("there shouldn't be a null action!")
            
            new_env = copy.deepcopy(self.env)
            new_env.play_move(action)
            
            new_done = False
            new_result = None
            result = new_env.game.game_result(action)
            if result != -1:
                new_done = True
                new_result = result
                
            child_node = Node(self.player_mark, new_env, new_done,
                              not self.is_player_turn, parent=self,
                              action_played=action, result=new_result)
            children.append(child_node)
            
        self.children = children
    
    # Explores the game tree, either creating new leaf nodes
    # or conducting a rollout at an unvisited leaf node
    def explore(self):
        
        # traverse tree until a leaf is reached
        
        current = self
        while current.children:
            children = current.children
            max_score = max(c.uct_score() for c in children)
            candidate_nodes = [c for c in children if c.uct_score() == max_score]
            
            if not candidate_nodes:
                print(max_score)
                print([c.uct_score() for c in children])
                raise Exception("no legal moves!")
            
            new_child = random.choice(candidate_nodes)
            current = new_child
        
        # either rollout or expand node
        
        reward = 0
        
        if current.done:
            reward = current.calculate_done_reward()
        elif current.N < 1:
            reward = current.rollout()
        else:
            current.create_children()
            current = random.choice(current.children)
            
            if current.done:
                reward = current.calculate_done_reward()
            else:
                reward = current.rollout()
            
        parent = current
        do_compliment = False
        
        while parent:
            parent.N += 1
            if do_compliment:
                parent.T += 1 - reward
            else:
                parent.T += reward
            parent = parent.parent
            do_compliment = not do_compliment

    # TODO method comment
    def calculate_done_reward(self):
        if not self.action_played:
                raise Exception("null action at a finished game state!")
        if self.result is not None:
            result = self.result
        else:
            result = self.env.game.game_result(self.action_played)
            raise Exception("this shouldn't happen")
        if self.turn_to_mark() == 1:
            return result
        elif self.turn_to_mark() == 2:
            return 1 - result
    
    # TODO method comment
    def turn_to_mark(self):
        if self.is_player_turn:
            return self.player_mark
        else:
            if self.player_mark == 1:
                return 2
            elif self.player_mark == 2:
                return 1           
 
    # TODO method comment
    def next(self):
        if not self.children:
            self.env.game.print_board()
            raise Exception("no legal moves or no children!")
        if self.done:
            raise Exception("game is done!")
        
        max_visits = max(c.N for c in self.children)
        max_children = [c for c in self.children if c.N == max_visits]
        choice = random.choice(max_children)
        
        return choice, choice.action_played
    
    # TODO method comment
    def detach(self):
        del self.parent
        self.parent = None
    
    def __str__(self):
        return f"(N: {self.N}, T: {self.T}, board: {self.env.game.board}, action played: {self.action_played}, turn: {self.env.game.moves_played}, result: {self.result})"
    
# useful for cleanly writing rollout code
def agent_random(obs, config):
    moves = obs[3]
    return random.choice(moves)