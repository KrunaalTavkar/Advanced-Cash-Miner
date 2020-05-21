#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 22:19:37 2019

@author: krunaaltavkar
"""

import time

all_turns = {}
action = ['U', 'D', 'L', 'R']
actions = {'U':((-1,0), (-1, -1), (-1, 1)), 'D':((1,0), (1, -1), (1, 1)), 'L':((0, -1), (-1, -1), (1, -1)), 'R':((0, 1), (-1, 1), (1 ,1))}

def policy_eval(grid_ans, utility):
    for m in range(0, 3):
        for i in reach:
            for j in reach:
                state = (i, j)
                if state not in rewards and state not in walls:
                    utility[i][j] = r_p + gamma * utility_values(grid_ans[(i, j)], state, utility, all_turns)
    return utility

def get_best_move(values):
    best_move = values.index(max(values))
    return best_move

def utility_values(action, state, utitlity, all_turns):
    value = sum(probability * utility[x][y] for ((x, y), probability) in all_turns[state, action])
    return value

def all_moves():
    for state in grid_pos:
        for i in action:
            if i == 'R':
                x1 = (state[0], state[1] + 1)
                x2 = (state[0] - 1, state[1] + 1)
                x3 = (state[0] + 1, state[1] + 1)
            elif i == 'L':
                x1 = (state[0], state[1] - 1)
                x2 = (state[0] - 1, state[1] - 1)
                x3 = (state[0] + 1, state[1] - 1)
            elif i == 'U':
                x1 = (state[0] - 1, state[1])
                x2 = (state[0] - 1, state[1] - 1)
                x3 = (state[0] - 1, state[1] + 1)
            elif i == 'D':
                x1 = (state[0] + 1, state[1])
                x2 = (state[0] + 1, state[1] - 1)
                x3 = (state[0] + 1, state[1] + 1)
            
            if x1 in valid_moves:
                s1 = (x1, p_value)
            else:
                s1 = (state, p_value)
            
            if x2 in valid_moves:
                s2 = (x2, p_displacement)
            else:
                s2 = (state, p_displacement)
                
            if x3 in valid_moves:
                s3 = (x3, p_displacement)
            else:
                s3 = (state, p_displacement)
            
            all_turns[(state, i)] = s1,s2,s3
            
    return 0

if __name__ == '__main__':
    #start = time.time()
    
    walls = []
    rewards = {}
    utility = []
    line_count = 1
    program_input = open("input.txt", 'r')
    program_input_data = program_input.readlines()
    grid_size = int(program_input_data[0])
    wall_size = int(program_input_data[1])
    
    for i in range(2, wall_size+2):
        z = program_input_data[i].strip().split(',')
        walls.append((int(z[0]) - 1, int(z[1]) - 1))
        
    line_count += i
    reward_size = int(program_input_data[line_count])
    
    for i in range(line_count + 1, reward_size + line_count + 1):
        z = program_input_data[i].strip().split(',')
        coordinates = (int(z[0]) - 1, int(z[1]) - 1)
        reward_value = float(z[2])
        rewards[coordinates] = reward_value
        
    line_count = i + 1
    p_value = float(program_input_data[line_count])
    line_count += 1
    r_p = float(program_input_data[line_count])
    line_count += 1
    gamma = float(program_input_data[line_count])
    p_displacement = (1 - p_value)/2
    reach = range(0, grid_size)
    
    grid_pos = []
    for i in reach:
        for j in reach:
            grid_pos.append((i,j))
    utility = [[r_p] * grid_size for x in range(grid_size)]
    for i in reach:
        for j in reach:
            state = (i, j)
            if state in walls:
                utility[i][j] = None
            elif state in rewards:
                utility[i][j] = rewards[state]
        
    grid_ans = {}
    for i in reach:
        for j in reach:
            state = (i, j)
            if state not in rewards and state not in walls:
                grid_ans[(i, j)] = 'U'
            elif state in rewards:
                grid_ans[state] = 'E'
            elif state in walls:
                grid_ans[state] = 'N'
                
    valid_moves = {(i, j) for i in reach for j in reach} - set(walls)
            
    all_moves()
    
    while True:
        utility = policy_eval(grid_ans, utility)
        no_change = True
        for state in valid_moves:
            if state not in rewards:
                best_move = action[get_best_move([utility_values(a, state, utility, all_turns) for a in action])]
                if best_move != grid_ans[state]:
                    grid_ans[state] = best_move
                    no_change = False
        if no_change:
            break
            
    output = open("output.txt", "w")
    for i in reach:
        temp_val = []
        for j in reach:
            temp_val.append(grid_ans[(i, j)])
        k = ','.join(temp_val)
        output.write(str(k) + "\n")
    output.close()
    
    #print time.time() - start
