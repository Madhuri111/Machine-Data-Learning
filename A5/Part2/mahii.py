import numpy as np
d = 0

def pprint(str):
    if(d):
        print(str)


rollnumber = int(input("Enter RollNumber:"))

x = 1-((rollnumber % 1000) % 40+1)/100
print(x)
outstr = ""  # contains the output string

outstr += "discount: 0.5\n"
outstr += "values: reward\n"

# STATES

# positions

# here we use (column,row) format while determining the location of agent/target

possible_locations = []
possible_locations_representation = []
for i in range(3):
    for j in range(3):
        possible_locations.append(tuple([i, j]))
        possible_locations_representation.append(str(i)+str(j))
pprint(possible_locations)
pprint(possible_locations_representation)

# states
states = []
states_representation = []
for agent_pos in range(9):
    for target_pos in range(9):
        for call in range(2):
            states.append(
                tuple([possible_locations[agent_pos], possible_locations[target_pos], call]))
            states_representation.append(
                'a' + possible_locations_representation[agent_pos] + 't' + possible_locations_representation[target_pos]+'c' + str(call))
print(states)
print(states_representation)

outstr += 'states: '
for i in states_representation:
    outstr += i+' '
outstr += '\n'

# actions
actions = ['Stay', 'up', 'Down', 'Left', 'Right']
outstr += 'actions: '
for i in actions:
    outstr += i+' '
outstr += '\n'

# observations
observations = ['o1', 'o2', 'o3', 'o4', 'o5', 'o6']
outstr += 'observations: '
for i in observations:
    outstr += i+' '
outstr += '\n'

# start
# this depends upon the case they are dealing with rn. start include
# If you know the target is in (1,1) cell and your observation is o6: agent not in 1 cell distance from target
# this means that the agent is at the corners of the page


start_positions_representation = []
target_pos_x = 1
target_pos_y = 1

for call in range(2):
    start_positions_representation.append('a00t11c' + str(call))
    start_positions_representation.append('a22t11c' + str(call))
    start_positions_representation.append('a02t11c' + str(call))
    start_positions_representation.append('a20t11c' + str(call))

outstr += 'start include: '
for i in start_positions_representation:
    outstr += i+' '
outstr += '\n'

# Resulting position after each action
# actions = ['Stay', 'up', 'Down', 'Left', 'Right']


def move(cpx, cpy, action):
    if(action == "Stay"):
        return (cpx, cpy)
    elif(action == 'Down'):
        return (cpx, max(cpy-1, 0))
    elif(action == 'up'):
        return (cpx, min(cpy+1, 2))
    elif(action == 'Left'):
        return (max(cpx-1, 0), cpy)
    elif(action == 'Right'):
        return (min(cpx+1, 2), cpy)

# makes the target  positions and the probability of reaching there list


def target_pos_prob_list(target_position):
    move_target_probabilities = []
    move_target_final_positions = []  # in tuple form
    for act in actions:
        final_target_pos = move(target_position[0], target_position[1], act)
        move_target_final_positions.append(
            possible_locations_representation[final_target_pos[0]*3+final_target_pos[1]])  # in representation form
        if(act == "Stay"):
            move_target_probabilities.append(0.4)
        else:
            move_target_probabilities.append(0.15)
    mt = dict()
    for i in range(5):
        if move_target_final_positions[i] in mt.keys():
            mt[move_target_final_positions[i]] += move_target_probabilities[i]
        else:
            mt[move_target_final_positions[i]] = move_target_probabilities[i]
    return mt


def opposite(action):
    if(action == "Stay"):
        return "Stay"
    elif(action == 'up'):
        return "Down"
    elif(action == 'Down'):
        return "up"
    elif(action == 'Left'):
        return "Right"
    elif(action == 'Right'):
        return "Left"

# makes a dictionary of all possible agent positions and corresponding probability


def agent_pos_prob_list(agent_position, act):
    move_agent_probabilities = []
    move_agent_final_positions = []  # in tuple form
    final_agent_pos_1 = move(agent_position[0], agent_position[1], act)
    final_agent_pos_2 = move(
        agent_position[0], agent_position[1], opposite(act))
    move_agent_final_positions.append(
        possible_locations_representation[final_agent_pos_1[0]*3+final_agent_pos_1[1]])
    move_agent_final_positions.append(
        possible_locations_representation[final_agent_pos_2[0]*3+final_agent_pos_2[1]])  # in representation form
    move_agent_probabilities.append(x)
    move_agent_probabilities.append(1-x)
    mt = dict()
    for i in range(2):
        if move_agent_final_positions[i] in mt.keys():
            mt[move_agent_final_positions[i]] += move_agent_probabilities[i]
        else:
            mt[move_agent_final_positions[i]] = move_agent_probabilities[i]
    # print(act,agent_position,mt)
    # input()
    return mt


# transition matrix
state_no = 0
for agent_action in actions:
    for agent_pos in range(9):
        for target_pos in range(9):
            # this represents each state
            agent_position = possible_locations[agent_pos]
            target_position = possible_locations[target_pos]
            # if the action is Stay,  then the agent position shall remain the same
            # in representation form
            att = agent_pos_prob_list(agent_position, agent_action)

            # the target position can vary. This is where the challenge lies
            # the target can go to 5 possible positions, let their probabilities be stored in a list of 4
            # [Stay,up,Down,Left,Right]
            #  now mt contains the list of all possible final positions and their corresponding probabilities
            mt = target_pos_prob_list(target_position)
            # now deal with the calls

            for kk in att.keys():
                for i in mt.keys():
                    ft = [{"0": 0.6, "1": 0.4}, {"0": 0.2, "1": 0.8}]
                    for initial_call in range(2):
                        for j in ft[initial_call].keys():
                            # kk,i fnal positions
                            if initial_call==1 and kk==i:
                                print("hi")
                                outstr += "T: "+agent_action+" : " + 'a'+possible_locations_representation[agent_pos]+'t'+possible_locations_representation[target_pos]+'c'+str(
                                initial_call)+' : '+'a'+kk+'t'+i+'c'+"0"+" "+str(mt[i]*att[kk]) + '\n'

                            else:
                                outstr += "T: "+agent_action+" : " + 'a'+possible_locations_representation[agent_pos]+'t'+possible_locations_representation[target_pos]+'c'+str(
                                initial_call)+' : '+'a'+kk+'t'+i+'c'+j+" "+str(mt[i]*ft[initial_call][j]*att[kk]) + '\n'


# OBSERVATIONS
# the action does not affect the endstate: use a *
for agx in range(3):
    for agy in range(3):
        for tx in range(3):
            for ty in range(3):
                for call in range(2):
                    obs = 'o'
                    if(agx == tx and agy == ty):
                        obs = 'o1'
                    elif(agx == tx-1 and agy == ty):
                        obs = 'o2'
                    elif(agx == tx and agy == ty+1):
                        obs = 'o3'
                    elif(agx == tx+1 and agy == ty):
                        obs = 'o4'
                    elif(agx == tx and agy == ty-1):
                        obs = 'o5'
                    else:
                        obs = 'o6'
                    outstr += 'O: * : '+'a' + \
                        str(agx)+str(agy)+'t'+str(tx)+str(ty) + \
                        'c'+str(call)+' : '+obs+' 1.0\n'

# REWARDS: assuming that Stay is also an action that needs to be penalised
for act in actions:
  for agx in range(3):
    for agy in range(3):
        for tx in range(3):
            for ty in range(3):
                for call in range(2):
                    if(act=='Stay'):obs=0
                    else:obs = -1
                    if(agx == tx and agy == ty and call == 1):
                        obs += rollnumber % 100+10
                    outstr += 'R: '+act+' : * : '+'a' + \
                        str(agx)+str(agy)+'t'+str(tx)+str(ty) + \
                        'c'+str(call)+' : * '+str(obs)+'\n'

open(str(rollnumber)+'.pomdp','w').write(outstr)