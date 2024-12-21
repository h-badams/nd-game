import game
import environment
import matplotlib.pyplot as plt
import numpy as np
import random

# histogram for win rates in higher dimensions when both players play randomly
# warning: this takes a long time

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
            for k in range(trials):
                result = env.run([agent_random, agent_random])
                if result == 1:
                    heights[j-2][i-2] += 1
                if k == trials - 1:
                    print(f"finished n={j}, d={i}")
        
    
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