import numpy as np

rollnumber = 2018101117
prob_x = 1 - (((rollnumber % 1000)%40 + 1) / 100)

discount = 0.5
values = "reward"

actions = np.array(["stay", "up", "down", "left", "right"])

observations = np.array(['o1', 'o2', 'o3', 'o4', 'o5', 'o6'])

# START PRINTING:

print("discount: {0}".format(discount))
print("values: {0}".format(values))

print("states: ", end="")
for x1 in range(0, 3):
    for y1 in range(0, 3):
        for x2 in range(0, 3):
            for y2 in range(0, 3):
                for z in range(0, 2):
                    print('s_' + str(x1)+'-'+str(y1)+'_'+str(x2)+'-'+str(y2)+'_'+str(z), end=" ")
print("")

print("actions: ", end="")
for action in actions:
    print(action, end=" ")
print("")

print("observations: ", end="")
for observation in observations:
    print(observation, end=" ")
print("")

# TRANSISTION MATRIX:

def is_out_of_bounds(pos):
    if pos[0] < 0 or pos[0] > 2 or pos[1] < 0 or pos[1] > 2:
        return True
    else:
        return False

def move_target(x, y):

    target_pos = list()
    target_prob = list()

    target_pos.append(str(x)+'-'+str(y))
    target_prob.append(0.4)

    possible = [ [x+1, y], [x-1, y], [x, y+1], [x, y-1] ]

    for pos in possible:
        if is_out_of_bounds(pos):
             target_prob[0] += 0.15
        else:
            target_pos.append(str(pos[0])+'-'+str(pos[1]))
            target_prob.append(0.15)

    # print(target_pos, target_prob)

    return target_pos, target_prob

def move_agent(x, y, action):

    agent_pos = list()
    agent_prob = list()

    if action == "stay":
        agent_pos.append(str(x)+'-'+str(y))
        agent_prob.append(1.0)

    elif action == "up" or action == "down":
        possible = [ [x+1, y], [x-1, y] ]

        i = 0
        for pos in possible:

            prob = (1-i)*prob_x + i*(1-prob_x)
            if action == "up":
                prob = i*prob_x + (1-i)*(1-prob_x)

            if is_out_of_bounds(pos):
                agent_pos.append(str(x)+'-'+str(y))
                agent_prob.append(prob)
            else:
                agent_pos.append(str(pos[0])+'-'+str(pos[1]))
                agent_prob.append(prob)

            i += 1

    elif action == "left" or action == "right":
        possible = [ [x, y+1], [x, y-1] ]

        i = 0
        for pos in possible:

            prob = (1-i)*prob_x + i*(1-prob_x)
            if action == "left":
                prob = i*prob_x + (1-i)*(1-prob_x)

            if is_out_of_bounds(pos):
                agent_pos.append(str(x)+'-'+str(y))
                agent_prob.append(prob)
            else:
                agent_pos.append(str(pos[0])+'-'+str(pos[1]))
                agent_prob.append(prob)

            i += 1

    return agent_pos, agent_prob

for action in actions:
    for x1 in range(0, 3):
        for y1 in range(0, 3):
            for x2 in range(0, 3):
                for y2 in range(0, 3):
                    for z in range(0, 2):
                        start_state = 's_' + str(x1)+'-'+str(y1)+'_'+str(x2)+'-'+str(y2)+'_'+str(z)

                        agent_pos, agent_prob = move_agent(x1, y1, action)

                        for i in range(len(agent_pos)):

                            for call in range(0, 2):
                                call_prob = 0.2 if z else 0.4
                                if(z == call):
                                    call_prob = 1 - call_prob
                                  
                                target_pos, target_prob = move_target(x2, y2)
                                for j in range(len(target_pos)):
                                      
                                    # print(agent_prob[i], target_prob[j], call_prob)
                                    prob = agent_prob[i] * target_prob[j] * call_prob
                                    end_state = 's_' + agent_pos[i] + '_' + target_pos[j] + '_' + str(call)

                                    print("T: {0} : {1} : {2} {3}".format(action, start_state, end_state, prob))

# OBSERVATION PROBABILITIES:

for x1 in range(0, 3):
    for y1 in range(0, 3):
        for x2 in range(0, 3):
            for y2 in range(0, 3):
                for z in range(0, 2):
                    
                    end_state = 's_' + str(x1)+'-'+str(y1)+'_'+str(x2)+'-'+str(y2)+'_'+str(z)

                    obs = "o6"
                    if x1==x2 and y1==y2:
                        obs = "o1"
                    elif x1==x2 and y1==y2-1:
                        obs = "o2"
                    elif x1==x2-1 and y1==y2:
                        obs = "o3"
                    elif x1==x2 and y1==y2+1:
                        obs = "o4"
                    elif x1==x2+1 and y1==y2:
                        obs = "o5"
    
                    print("O: * : {0} : {1} 1.0".format(end_state, obs))

# REWARD FUNCTION:

for action in actions:
    for x1 in range(0, 3):
        for y1 in range(0, 3):
            for x2 in range(0, 3):
                for y2 in range(0, 3):
                    for z in range(0, 2):
                        end_state = 's_' + str(x1)+'-'+str(y1)+'_'+str(x2)+'-'+str(y2)+'_'+str(z)

                        reward = 0
                        if x1==x2 and y1==y2 and z:
                            reward = rollnumber%100 + 10
                        
                        if action != "stay":
                            reward -= 1

                        print("R: {0} : * : {1} : * {2}".format(action, end_state, reward))
