# Class representing a tic tac toe board of arbitrary width and dimension

class NDgame():
    
    def __init__(self, dim, width):
        self.dim = dim
        self.width = width
        self.board = self.create_board(dim, width)
        self.winning_lines = self.enumerate_lines(dim, width)
        
        self.moves_played = 0
        self.squares = width ** dim
    
    # creates a 'dim' dimensional array of length 'width'
    def create_board(self, dim, width):
        if dim < 1:
            raise Exception("Illegal Argument: dim should be positive")
        if dim == 1:
            return [0 for i in range(width)]
        else:
            return [self.create_board(dim - 1, width) for i in range(width)]
    
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
        lines = []
        for line in self.winning_lines:
            if coord in line:
                lines.append(line)
        return lines
    
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
                    width + 1 not in current_choices or current_choices.index(width) < current_choices.index(width + 1)):
                    for j in range(width):
                        x = tuple(coord if coord < width else 
                                (j if coord == width else len(current_choices) - 1 - j) for coord in current_choices)
                        line.append(x)
                    winning_lines.append(line)
            
            # increment pointer
            while pointer < len(current_choices) and current_choices[pointer] == width + 1:
                current_choices[pointer] = 0
                pointer += 1
            
            if pointer < len(current_choices):
                current_choices[pointer] += 1
                pointer = 0
                
        return winning_lines
       
    # returns true if any of a collection of lines contains all of one mark (either X or O)
    def win_through_lines(self, lines):
        for line in lines:
            mark = line[0]
            is_win = True
            for x in line:
                if x == 0 or x != mark:
                    is_win = False
                    break
            if is_win:
                return True
        return False

    # returns true if a player has just made 'dim' in a row, false otherwise
    def is_win(self, coord):
        lines = self.lines_through_coord(coord)
        return self.win_through_lines(lines)
    
    # returns -1 if game is ongoing, 1 for X win, 0 for O win, 0.5 for tie
    def game_result(self, coord):
        if self.is_win(coord):
            pass
        elif self.moves_played == self.squares:
            return 0.5
        return -1
    
    # returns the board in string representation 
    def __str__(self):
        return str(self.board)   
    
game = NDgame(3,3)
print(len(game.winning_lines))
print(len(game.lines_through_coord((0,0,0))))
'''print(game.get_square_val((0,1,2)))
game.set_square_val((0,1,2),1)
print(game.get_square_val((0,1,2)))'''

    
            