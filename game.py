import random
from collections import defaultdict
# Class representing a tic tac toe board of arbitrary width and dimension

class NDgame():
    
    def __init__(self, dim, width):
        self.dim = dim
        self.width = width
        self.board = self.create_board(dim, width)
        self.winning_lines = self.enumerate_lines(dim, width)
        self.squares = width ** dim
        
        self.points = self.enumerate_points(dim, width)
        # caching saves time when playing 100s of games in higher dimensions
        self.points_to_lines = {}
        for p in self.points:
            for line in self.winning_lines:
                if p in line:
                    if p not in self.points_to_lines:
                        self.points_to_lines[p] = []
                    self.points_to_lines[p].append(line)
                    
        self.moves_played = 0
        self.move_list = []
    
    # creates a 'dim' dimensional array of length 'width'
    def create_board(self, dim, width):
        if dim < 1:
            raise Exception("Illegal Argument: dim should be positive")
        if dim == 1:
            return [0 for i in range(width)]
        else:
            return [self.create_board(dim - 1, width) for i in range(width)]
        
    def enumerate_points(self, dim, width):
        coords = []
        curr = [0 for i in range(dim)]
        for i in range(width ** dim):
            coords.append(tuple(i for i in curr))
            if i != (width ** dim) - 1:
                pointer = 0
                while curr[pointer] == width - 1:
                    curr[pointer] = 0
                    pointer += 1
                curr[pointer] += 1
        return coords
    
    # returns the value of a square on the board
    def get_square_val(self, coord):
        current = self.board
        for i in range(self.dim):
            if i < len(coord) and coord[i] < self.width:
                current = current[coord[i]]
            else:
                raise Exception("invalid coordinate")
        return current
    
    # sets a value on the board - either 1 for X or 2 for O
    def set_square_val(self, coord, value):
        current = self.board
        for i in range(self.dim-1):
            if i < len(coord) and coord[i] < self.width:
                current = current[coord[i]]
            else:
                raise Exception("invalid coordinate")
        current[coord[-1]] = value
    
    # returns the lines that pass through a given coordinate
    def lines_through_coord(self, coord):
        if len(coord) != self.dim:
            raise Exception("coord is the wrong length")
        '''lines = []
        for line in self.winning_lines:
            if coord in line:
                lines.append(line)
        return lines'''
        
        return self.points_to_lines[coord]
    
    # enumerates all winning lines - that is, all lines of length 'dim'
    def enumerate_lines(self, dim, width):
        winning_lines = []
        coordinate_choices = [i for i in range(width)]
        coordinate_choices.append(width) # ascending
        coordinate_choices.append(width + 1) # descending
        
        pointer = 0
        
        current_choices = [0 for i in range(dim)]
        
        while pointer < len(current_choices):
            # enumerate a line
            line = []
            
            if width in current_choices or width + 1 in current_choices:
                if width in current_choices and (
                    width + 1 not in current_choices or (
                        current_choices.index(width) < current_choices.index(width + 1))):
                    for j in range(width):
                        x = tuple(coord if coord < width else (j if coord == width else width - 1 - j) for coord in current_choices)
                        line.append(x)
                    winning_lines.append(tuple(line))
            
            # increment pointer
            while pointer < len(current_choices) and current_choices[pointer] == width + 1:
                current_choices[pointer] = 0
                pointer += 1
            
            if pointer < len(current_choices):
                current_choices[pointer] += 1
                pointer = 0
                
        return winning_lines
       
    # returns true if any of a collection of lines contains all of one mark (either X or O)
    def win_through_lines(self, lines, coord):
        
        for line in lines:
            mark = self.get_square_val(line[0])
            is_win = True
            for x in line:
                if self.get_square_val(x) == 0 or self.get_square_val(x) != mark:
                    is_win = False
            if is_win:
                return True
        return False

    # returns true for an empty square's coordinates, false otherwise
    def is_legal(self, coord):
        if self.get_square_val(coord) == 0:
            return True
        return False
    
    # plays a move on the board
    def play_move(self, coord, mark):
        if self.is_legal(coord):
            self.set_square_val(coord, mark)
            self.moves_played += 1
        else:
            raise Exception("can't play - illegal move!")
    
    # returns a list of legal moves
    def get_legal_moves(self):
        moves = []
        coord = [0 for i in range(self.dim)]
        
        for i in range(self.squares):
            pointer = 0
            if self.is_legal(coord):
                moves.append(tuple(coord))
                
            # incrememt coordinate
            if i != self.squares - 1:
                while coord[pointer] == self.width - 1:
                    coord[pointer] = 0
                    pointer += 1
                coord[pointer] += 1
                
        if not moves:
            raise Exception("no legal moves!")
        return moves
    
    # returns a random legal move
    def get_random_move(self):
        moves = self.get_legal_moves()
        return random.choice(moves)
        
    # returns true if a player has just made 'dim' in a row, false otherwise
    def is_win(self, coord):
        if self.moves_played < 2 * self.width - 1:
            return False
        lines = self.lines_through_coord(coord)
        return self.win_through_lines(lines, coord)
    
    # returns -1 if game is ongoing, 1 for X win, 0 for O win, 0.5 for tie
    def game_result(self, coord, mark):
        if self.is_win(coord):
            if mark == 1:
                return 1
            if mark == 2:
                return 0
            else:
                raise Exception("invalid mark!")
        elif self.moves_played == self.squares:
            return 0.5
        return -1
    
    # resets the game
    def reset(self):
        self.board = self.create_board(self.dim, self.width)
        self.moves_played = 0
        self.move_list = []
        self.win_dict = {line : [0,0] for line in self.winning_lines}

    # returns the board in string representation 
    def __str__(self):
        return str(self.board)   
    
if __name__ == "__main__":
    game = NDgame(2,3)
    
    lines = game.lines_through_coord((1,1))
    
    game.play_move((1,1), 1)
    game.play_move((1,0), 1)
    game.play_move((1,2), 1)
    
    print(game.win_dict)

    
    print(game.win_through_lines(lines, (1,1)))
    
    '''print(len(game.lines_through_coord((0,0,0))))
    print(game.get_square_val((0,1,2)))
    game.set_square_val((0,1,2),1)
    print(game.get_square_val((0,1,2)))
    print(game.get_random_move())'''
    '''game.play_move((1,1), 1)
    game.play_move((0,1), 1)
    game.play_move((2,1), 1)
    print(game)
    print(game.win_through_lines(game.lines_through_coord((1,1))))'''