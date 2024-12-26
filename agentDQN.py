import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import random
from collections import deque


class Agent():
    def __init__(self, game_config, state_space, action_space):
        self.batch_size = 100
        self.epsilon = 1.0 # TODO update this
        
        # in the tic tac toe case, the action space should be a
        # list of all tuples in the board
        self.action_space = action_space
        self.network = DQN(len(state_space), len(action_space))
        self.memory = deque([], maxlen=1000)
        
        self.optimizer = optim.Adam(self.network.parameters)
        
    def sample_memory(self):
        return random.sample(self.memory, self.batch_size)
    
    # epsilon-greedy action selection
    def get_action(self, state, action_subset):
        if np.random.random() < self.epsilon:
            return random.choice(action_subset)
        else:
            # have network make q values prediction
            prediction = self.network.forward(state)
            
            # set q vals for illegals to -infinity
            # this requres actions to be numbered?
            for i in range(len(self.action_space)):
                if self.action_space[i] not in action_subset:
                    prediction[i] = -1e7
            
            # return argmax of q values over the actions
            # aka argmax over the legal acitons
            index = 0
            max_q = prediction[index]
            
            for i in range(len(prediction)):
                if prediction[i] > max_q:
                    max_q = prediction[i]
                    index = i
                    
            # return the ith action
            
            return self.action_space[i]
                    
    
    
    def train(self):
        pass
        
 
class DQN(nn.Module):
    def __init__(self, in_size, out_size):
        super(DQN, self).__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            # trying one hot encoding the for board state, hence the 3
            nn.Linear(in_size, 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
            nn.Linear(32, out_size),
        )
        
        # TODO experiment with convolutional layers due to spatial nature of data
    
    def forward(self, x):
        x = self.flatten(x)
        output =  self.linear_relu_stack(x)
        
        # TODO now set all illegal moves to -inf
        
        return output
    
