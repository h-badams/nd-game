# environment for a two player game

class Environment():
    def __init__(self, game):
        self.game = game
        self.turn = game.moves_played
        
    # runs a game between two agents, and returns the result - 1, 0, or 0.5 for the first player
    def run(self, agent_list, display_end=False, print_moves=False, return_move_num=False, reset_before=False):
        
        if reset_before:
            self.reset()
        
        # TODO change this to be safer
        while True:
            move = agent_list[self.turn % 2](
                (self.game.board, turn_to_mark(self.turn), self.turn, self.game.get_legal_moves()), (
                self.game.dim, self.game.width))
            if self.game.is_legal(move):
                self.play_move(move)
                if print_moves:
                    print(move)
            else:
                raise Exception(f"illegal move by player {turn_to_mark(self.turn)}")

            if self.game.game_result(move) != -1:
                if display_end:
                    print("final game state: ", self.game)
                if not return_move_num:
                    return self.game.game_result(move)
                else:
                    return self.game.game_result(move), self.game.moves_played
        
    # useful to call this instead of the game version    
    def play_move(self, coord):
        mark = turn_to_mark(self.turn) 
        self.game.play_move(coord, mark)
        self.turn += 1
        
    def reset(self):
        self.game.reset()
        self.turn = 0

def turn_to_mark(turn):
    if turn % 2 == 0:
        return 1
    else:
        return 2         