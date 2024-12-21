import game
import environment
import matplotlib.pyplot as plt
import numpy as np
import random
import time

# histogram for win rates in higher dimensions when both players play randomly
# warning: this takes a long time

start_time = time.time()

def agent_random(obs, config):
    moves = obs[3]
    return random.choice(moves)

if __name__ == "__main__":
    # Fixing random state for reproducibility
    
    d = [2,3,4,5]
    n = [2,3,4,5]
    
    heights = [[1 for i in d] for j in n]
    
    trials = 100
    
    for i in d:
        for j in n:
            g = game.NDgame(i,j)
            env = environment.Environment(g)
            average_length = 0
            for k in range(trials):
                result, turns = env.run([agent_random, agent_random], return_move_num=True)
                average_length += turns / 100.0
                if result == 1:
                    heights[j-2][i-2] += 1
                if k == trials - 1:
                    print(f"finished n={j}, d={i}, average length = {average_length}")
        
    print("--- %s seconds ---" % (time.time() - start_time))
    
    heights = np.array(heights)
    
    nx, ny = heights.shape

    # Generate x and y coordinates
    x, y = np.meshgrid(np.arange(nx), np.arange(ny), indexing='ij')

    # Flatten arrays to 1D for bar3d
    x = x.flatten()
    y = y.flatten()
    z = np.zeros_like(x)  # Base of the bars
    dx = dy = np.ones_like(x)  # Width of the bars
    dz = heights.flatten()  # Heights of the bars

    # Plotting
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Create 3D histogram
    ax.bar3d(x, y, z, dx, dy, dz, shade=True)
    
    ax.set_xticks(np.arange(nx))  # Ticks at 0, 1, 2
    ax.set_yticks(np.arange(ny))  # Ticks at 0, 1, 2

    # Custom labels
    ax.set_xticklabels(np.arange(2, 2 + nx))
    ax.set_yticklabels(np.arange(2, 2 + ny))

    # Labels and title
    ax.set_xlabel('Width')
    ax.set_ylabel('Dimension')
    ax.set_zlabel('Win %')
    ax.set_title('3D Histogram')

    plt.show()