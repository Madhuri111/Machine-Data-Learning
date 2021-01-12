import numpy as np
d = 0


rollnumber = int(input("Enter RollNumber:"))
start_state_type=int(input("Enter Start State Type: \n\n0 for no start states\n1 for target in (1,1), o6 \n2 for agent in (0,1) and not o6 \n3 for agent at (0,1): 0.6 and (2,1): 0.4 and target at 4 corner cells uniformly\n\nCHOICE: "))

x = 1-((rollnumber % 1000) % 40+1)/100
print('x=', x)
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


outstr += 'states: '
for i in states_representation:
    outstr += i+' '
outstr += '\n'

# actions
actions = ['stay', 'up', 'down', 'left', 'right']
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

if(start_state_type==0):outstr+='start: uniform\n'
elif(start_state_type==1):outstr+='start include: a00t11c0 a22t11c0 a02t11c0 a20t11c0 a00t11c1 a22t11c1 a02t11c1 a20t11c1\n'
elif(start_state_type==2):outstr+='start include: a01t00c0 a01t11c0 a01t01c0 a01t02c0\n'
elif(start_state_type==3):
    outstr+='start: '
    agent_states={'01':0.6,'02':0.4}
    target_states={'00':0.25,'22':0.25,'02':0.25,'20':0.25}
    ln=dict()
    for i in agent_states.keys():
        for j in target_states.keys():
            for call in range(2):
                ln['a'+i+'t'+j+'c'+str(call)]=agent_states[i]*target_states[j]/2
    print(ln)
    state_no=0
    for i in states_representation:
       try: 
           if(ln[i]):outstr+=str(ln[i])+' '
       except: print(i);outstr+=' 0 '
    outstr+='\n'
# Resulting position after each action
# actions = ['stay', 'up', 'down', 'left', 'right']

outstr += "T: * : * : * 0\n"


def move(cpx, cpy, action):
    if(action == "stay"):
        return (cpx, cpy)
    elif(action == 'down'):
        return (cpx, max(cpy-1, 0))
    elif(action == 'up'):
        return (cpx, min(cpy+1, 2))
    elif(action == 'left'):
        return (max(cpx-1, 0), cpy)
    elif(action == 'right'):
        return (min(cpx+1, 2), cpy)

# makes the target  positions and the probability of reaching there list


def target_pos_prob_list(target_position):
    move_target_probabilities = []
    move_target_final_positions = []  # in tuple form
    for act in actions:
        final_target_pos = move(target_position[0], target_position[1], act)
        move_target_final_positions.append(
            possible_locations_representation[final_target_pos[0]*3+final_target_pos[1]])  # in representation form
        if(act == "stay"):
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
    if(action == "stay"):
        return "stay"
    elif(action == 'up'):
        return "down"
    elif(action == 'down'):
        return "up"
    elif(action == 'left'):
        return "right"
    elif(action == 'right'):
        return "left"

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
    return mt


# transition matrix
state_no = 0
for agent_action in actions:
    for agent_pos in range(9):
        for target_pos in range(9):
            # this represents each state
            agent_position = possible_locations[agent_pos]
            target_position = possible_locations[target_pos]
            # if the action is stay,  then the agent position shall remain the same
            # in representation form
            att = agent_pos_prob_list(agent_position, agent_action)

            # the target position can vary. This is where the challenge lies
            # the target can go to 5 possible positions, let their probabilities be stored in a list of 4
            # [stay,up,down,left,right]
            #  now mt contains the list of all possible final positions and their corresponding probabilities
            mt = target_pos_prob_list(target_position)
            # now deal with the calls
            for kk in att.keys():
                for i in mt.keys():
                    # check if it is a reward state
                    if(agent_pos == target_pos):
                        ft = [{"0": 0.6, "1": 0.4}, {"0": 1.0, "1": 0.0}]
                    else:
                        ft = [{"0": 0.6, "1": 0.4}, {"0": 0.2, "1": 0.8}]
                    for initial_call in range(2):
                        for j in ft[initial_call].keys():
                            outstr += "T: "+agent_action+" : " + 'a'+possible_locations_representation[agent_pos]+'t'+possible_locations_representation[target_pos]+'c'+str(
                                initial_call)+' : '+'a'+kk+'t'+i+'c'+j+" "+str(mt[i]*ft[initial_call][j]*att[kk]) + '\n'


# OBSERVATIONS
# the action does not affect the endstate: use a *
outstr += "O: * : * : * 0\n"
for agx in range(3):
    for agy in range(3):
        for tx in range(3):
            for ty in range(3):
                for call in range(2):
                    obs = 'o'
                    if(agx == tx and agy == ty):
                        obs = 'o1'
                    elif(agx == tx+1 and agy == ty):
                        obs = 'o4'
                    elif(agx == tx and agy == ty+1):
                        obs = 'o3'
                    elif(agx == tx-1 and agy == ty):
                        obs = 'o2'
                    elif(agx == tx and agy == ty-1):
                        obs = 'o5'
                    else:
                        obs = 'o6'
                    outstr += 'O: * : '+'a' + \
                        str(agx)+str(agy)+'t'+str(tx)+str(ty) + \
                        'c'+str(call)+' : '+obs+' 1.0\n'

# REWARDS: assuming that stay is also an action that needs to be penalised
outstr += "R: * : * : * : * 0\n"

for act in actions:
    for agx in range(3):
        for agy in range(3):
            for tx in range(3):
                for ty in range(3):
                    for call in range(2):
                        if(act == 'stay'):
                            obs = 0
                        else:
                            obs = -1
                        if(agx == tx and agy == ty and call == 1):
                            obs += rollnumber % 100+10
                        outstr += 'R: '+act+' : * : '+'a' + \
                            str(agx)+str(agy)+'t'+str(tx)+str(ty) + \
                            'c'+str(call)+' : * '+str(obs)+'\n'

open("newstuff/"+str(rollnumber)+'_'+str(start_state_type)+'.pomdp', 'w').write(outstr)
