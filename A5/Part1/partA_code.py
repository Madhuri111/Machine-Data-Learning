import json
import numpy as np
rollno=int(input("Enter roll no:"))
x = 1- ((rollno%1000)%40 +1)/100
y=(rollno%100)%3
print("Values of x and y are:",x,y)

actions = {0: "Left", 1: "Right"}
colors = {0: "Red", 1: "Green"}
states = {1: "Red", 2: "Red", 3: "Green", 4: "Green", 5: "Red"}

# pt[i][j] : probability of going to actually do j action, given a command i
pt = [[x, 1-x], [1-x, x]]

# transition probability table
t = np.zeros((2, 5, 5))
# t = [[[0.000]*5]*5]*2  # t[0] represents action: left t[1]: right

for i in range(5):
    t[0][i][max(i-1, 0)] = x  # left
    t[0][i][min(4, i+1)] = 1-x
    t[1][i][min(4, i+1)] = x  # right
    t[1][i][max(0, i-1)] = 1-x
print(t)
beliefs=[]
#
# print(t[0])
# print(t[1])
# obs[i][j]: observation table observe i given j is state
if(y==0):
    obs = [[0.9, 0.1], [0.85, 0.15]]
    observation = [[0.9, 0.1], [0.9, 0.1], [0.15, 0.85], [0.15, 0.85], [0.9, 0.1]]
elif(y==1):
    obs = [[0.8, 0.2], [0.95, 0.05]]
    observation = [[0.8, 0.2], [0.8, 0.2], [0.05, 0.95], [0.05, 0.95], [0.8, 0.2]]
elif(y==2):
    obs = [[0.85, 0.15], [0.9, 0.1]]
    observation = [[0.85, 0.15], [0.85, 0.15], [0.1, 0.9], [0.1, 0.9], [0.85, 0.15]]
# print(np.array(observation))

# current belief state should be stored in input.json
b = [1/3,1/3,0,0,1/3]
for ld in range (3):
    print("\n\n")
    print("Action ",ld,"\n")
    nb = [0]*5
    print("Previous Belief state: ", b)
    if(ld==0):
        a,o = 1,0
    else:
        a,o=0,1
    print("Action:",actions[a])
    print("Observation:",colors[o])
    for i in range(5):
        l = 0
        print("\n\nSTATE S"+str(i+1))
        print()
        print("Sum = ", end="")
        for s in range(5):
            l += t[a][s][i]*b[s]
        #  print(a,s,i, t[a][s][i], 6)
            print(round(t[a][s][i], 6), "×", round(b[s], 6), end=" + ")
        print("\n = ", end="")
        for s in range(5):
            print(round(t[a][s][i] * b[s], 6), end=" + ")
        print("\n = ", round(l, 6))
        print()
        print("New belief state = ", round(
            observation[i][o], 6), "×", round(l, 6), '=', round(observation[i][o]*l, 6))
        nb[i] = (observation[i][o]*l)
    print()
    print("Before normalising, ",[round(i,6) for i in nb])
    print("dividing by ",round(sum(nb),6))
    ss=sum(nb)
    for i in range(5):
        nb[i] /= ss
    print("After normalising, ",[round(i,6) for i in nb])
    print("Sum: ", sum(nb))
    b=nb
    beliefs.append(b)

print("Beliefs after each action: ",[[round(i,6) for i in nb]for nb in beliefs])
