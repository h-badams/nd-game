import NDgame

# environment for a two player game

class Environment():
    def __init__(self, game):
        self.game = game
    
    def run(self, agent_list, display_end=False, print_moves=False):
        turn = 0
        i = 0
        
        while True:
            move = agent_list[i]((self.game.board, i+1, turn), (self.width, self.winLength))
            if self.game.is_legal(move):
                self.game.play_move(move, i+1)
                self.game.move_list.append(move)
                if print_moves:
                    print(move)
            else:
                raise Exception("illegal move by player {i}")
            if self.game.game_result(move, i+1) != -1:
                if display_end:
                    print(self.game)
                return self.game.game_result(move, i+1)
            
            i += 1
            i %= 2
            turn += 1
            