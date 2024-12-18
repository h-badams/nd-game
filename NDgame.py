# Class representing a tic tac toe board of arbitrary width and dimension

class NDgame():
    
    def __init__(self, dim, width):
        self.dim = dim
        self.width = width
        self.board = self.create_board(dim, width)
        self.winning_lines = self.enumerate_lines(dim, width)
    
    def create_board(self, dim, width):
        if dim < 1:
            raise Exception("Illegal Argument: dim should be positive")
        if dim == 1:
            return [0 for i in range(width)]
        else:
            return [self.create_board(dim - 1, width) for i in range(width)]
    
    def square_val(self, coord):
        pass
    
    def lines_through_coord(self, coord):
        if len(coord) != self.dim:
            raise Exception("coord is the wrong length")
        lines = []
        for line in self.winning_lines:
            if coord in line:
                lines.append(line)
        return lines
    
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
        
    def __str__(self):
        return str(self.board)   
    
game = NDgame(3,3)
print(len(game.winning_lines))
print(game.winning_lines)
print(game.lines_through_coord((1,1,1)))
    
            