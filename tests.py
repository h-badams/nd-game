import game

def test_enumerate_lines(game):
    n = game.width
    d = game.dim
    expected_num_lines = int(((n + 2)**d - (n)**d) / 2)
    print("correct number of lines:", expected_num_lines)
    print("actual number of lines:", len(game.winning_lines))
    
    print("lines:", game.winning_lines)

if __name__ == "__main__":
    game = game.NDgame(2,3)
    test_enumerate_lines(game)