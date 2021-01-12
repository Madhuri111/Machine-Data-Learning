import numpy as np
import os
directory = "outputs"
if not os.path.exists(directory):
    os.mkdir(directory)
files=["task_1_trace.txt","task_2_part_1_trace.txt","task_2_part_2_trace.txt","task_2_part_3_trace.txt"]
r=[-20,-2.5,-2.5,-2.5]
sh=[-20,-0.25,-2.5,-2.5]
gamma=[0.99,0.99,0.1,0.1]
delta=[0.001,0.001,0.001,0.0000000001]
glo=0
while(glo<4):
    t="outputs/"+files[glo]
    f = open(t, "a+")
    actions=['shoot','dodge','recharge']
    x=48
    y=-20
    aa=[]
    bb=[]
    cc=[]
    act1=np.zeros((60,60),dtype=float)     #created 60*60 matrix for transiiton probability function
    act3=np.zeros((60,60),dtype=float)
    act2=np.zeros((60,60),dtype=float)
    def shoot_transition():
        h=5
        a=4
        s=3
        for i in range(h):
            for j in range(a):
                for k in range(s):
                    me=(i,j,k)
                    calc=np.asarray(me)
                    aa.append(calc)
        #aa=aa.reshape(1,60)
        #for i in range(60):
        #print(np.shape(aa))  #totally have 60 rows in which , each row has array with three elements
        #print(np.shape(me))   #printing it's dimensions
        for ii in range(12,60,1):
            for jj in range(60):
                #below statement is for printing and checking values in 60*60 matrix if they are having correct comparision
                #print(aa[ii][0],aa[ii][1],aa[ii][2],aa[jj][0],aa[jj][1],aa[jj][2])
                #condition when arrows or stamina or health increases which can actuallly never happen , so zero
                #if((aa[ii][2]-aa[jj][2])==1 or (aa[ii][1]-aa[jj][1])==1 or aa[ii][0]<aa[jj][0]):
                #act1[ii][jj]=0
                #condition when health got reduced and even arrow which means hit MD with arrow with probabitlity 0.5
                if((aa[ii][0]-aa[jj][0])==1 and (aa[ii][1]-aa[jj][1])==1 and (aa[ii][2]-aa[jj][2])==1):
                    act1[ii][jj]=0.5
                #condition when hit with arrow but didn't touch
                if((aa[ii][0]-aa[jj][0])==0 and (aa[ii][1]-aa[jj][1])==1 and (aa[ii][2]-aa[jj][2])==1):
                   act1[ii][jj]=0.5
                if(aa[ii][1]==0 or aa[ii][2]==0):
                    act1[ii][ii]=1
       


    #recharge 100
    def recharge_transition():
        h=5
        a=4
        s=3
        for i in range(h):
            for j in range(a):
                for k in range(s):
                    me=(i,j,k)
                    calc=np.asarray(me)
                    bb.append(calc)
        #print(np.shape(bb))
        for l in range(12,60,1):
            for m in range(60):
                if(bb[l][2]==2):
                    act3[l][l]=1
                #below condition checks if stamina is increased by 50 points which means 1 , so it is with probability 0.8 as given
                elif((bb[m][2]-bb[l][2])==1):
                    if(bb[l][1]==bb[m][1] and bb[l][0]==bb[m][0]):
                        act3[l][m]=0.8
                #below condition checks if stamina is not increased by 50 points which means 1 , so it is with probability 0.2 as given
                elif((bb[m][2]-bb[l][2])==0):
                    if(bb[l][1]==bb[m][1] and bb[l][0]==bb[m][0]):
                        act3[l][m]=0.2

        count=0
        for i in range(12,60,1):
            for j in range(0,60,1):
                if(act3[i][j]!=0):
                    count=count+1
        #print(count,"recharge")            


    #dodge 100 # rrecharge 80
    def dodge_transition():
        h=5
        a=4
        s=3
        man=0
        for i in range(h):
            for j in range(a):
                for k in range(s):
                    me=(i,j,k)
                    calc=np.asarray(me)
                    cc.append(calc)


        for u in range(12,60):
            for v in range(60):
                if(cc[u][2]==2 and cc[u][0]==cc[v][0]):    
                    if(cc[v][2]==1):  #from 100 to 50
                        if(cc[u][1]==3 and cc[v][1]==3):
                                act2[u][v]=0.8
                        elif(cc[v][1]-cc[u][1]==1):
                            act2[u][v]=0.64
                        elif(cc[v][1]==cc[u][1]):
                            act2[u][v]=0.16
                    elif(cc[v][2]==0):      #from 100 to 100
                        if(cc[u][1]==3 and cc[v][1]==3):
                                act2[u][v]=0.2
                        elif(cc[v][1]-cc[u][1]==1):
                            act2[u][v]=0.16
                        elif(cc[v][1]==cc[u][1]):
                            act2[u][v]=0.04
             

                elif(cc[u][2]==1 and cc[u][0]==cc[v][0]):  
                    if(cc[v][2]==0):   #from 50 to 0 
                        if(cc[u][1]==3 and cc[v][1]==3):
                                act2[u][v]=1
                        elif(cc[v][1]-cc[u][1]==1):
                            act2[u][v]=0.8
                        if(cc[v][1]==cc[u][1]):
                            act2[u][v]=0.2
                elif(cc[u][2]==0):
                    act2[u][u]=1


    '''
        coun=0
        for i in range(0,60,1):
            for j in range(0,60,1):
                if(act2[i][j]!=0):
                    print(i,"-->",j,act2[i][j])
                    coun=coun+1
        print(coun,"dodge")  
    '''
    def maximum(a, b, c): 
       
        if (a >= b) and (a >= b): 
            largest = a 
      
        elif (b >= a) and (b >= a): 
            largest = b 
        else: 
            largest = c 
              
        return largest 





    cou=0

    #creating utility function , for every state so 60*1 matrix
    current_util=np.zeros([60,1],dtype=float)

    #creating previous utility function, for every state so 60*1 matrix
    prev_util=np.zeros([60,1],dtype=float)
    for mad in range(0,12):
            prev_util[mad]=0
    for me in range(0,12):
        current_util[me]=0

    while(1):
        print("iteration",cou)
        shoot_transition()
        dodge_transition()
        recharge_transition()

        
        #print(prev_util)

        for mana in range(0,12,1):
            f=current_util[mana]
            res=cc[mana],":","-1","=","0.000"
            print(res,file=f)

        flag=0
        for i in range(12,60,1):
            #storing current actions with shoot , dodge, recharge
            current_action=np.zeros((3,1))
            #print(current_action)
            #print(np.shape(current_action))
            a=0
            b=0
            c=0
            for j in range(60):
                #print(current_action)
                #modifying action values according to transition functions
                a=a++gamma[glo]*act1[i][j]*prev_util[j]  #for shoot action

                b=b++gamma[glo]*act2[i][j]*prev_util[j]  #for dodge action

                c=c++gamma[glo]*act3[i][j]*prev_util[j]  #for recharge action

            a=a+sh[glo]
            b=b+r[glo]
            c=c+r[glo]
            maxh=max(a,b,c)
            #print(cc[i]) it gives you values of state there suppose cc[2] = (0,0,2) so health 0 , arrows 0 , stamina 2
            take=cc[i]   #now x has all three values suppose cc[12]=(100) then x[0]=1,x[1]=0,x[2]=0
            choose="" #declared a string for choosing which action to have

            if(a==b and b==c and c==a):

                
                if(take[1]!=0 and take[2]!=0):
                    choose="SHOOT"
                    maxh=a
                    if(take[1]>take[2]):
                        choose="SHOOT"
                        maxh=a
                elif(take[2]!=0):
                    choose="DODGE"
                    maxh=b
                else:
                    choose="RECHARGE"
                    maxh=c
                '''
                if(take[2]==0):
                    choose="RECHARGE"
                    maxh=c
                elif(take[1]!=0):
                    choose="SHOOT"
                    maxh=a
                else:
                    choose="DODGE"
                    maxh=b
                '''
                
            else:
                #case 1 if any two of them are equal , total 3 kind of these cases will come
                if(a==b and a==maxh): #shoot or dodge
                    if(take[2]!=0):
                        if(take[1]!=0):
                            choose="SHOOT"
                            maxh=a
                        else:
                            choose="DODGE"
                            maxh=b
                    else:
                        choose="RECHARGE"
                        maxh=c
                if(b==c and b==maxh):  #dodge or recharge
                    if(take[2]!=0):
                        choose="DODGE"
                        maxh=b
                    else:
                        choose="RECHARGE"
                        maxh=c
                if(c==a and c==maxh): #shoot or recharge
                    if(take[2]!=0):
                        if(take[1]!=0):
                            choose="SHOOT"
                            maxh=a
                        else:
                            choose="RECHARGE"
                            maxh=c
                    else:
                        choose="RECHARGE"
                        maxh=c
                #4th test case
                elif(a!=b and b!=c and c!=a):
                    if(maxh==a):
                        if(take[2]!=0): 
                            if(take[1]!=0):
                                choose="SHOOT"
                                maxh=a 
                            else:
                                second=max(b,c)
                                if(second==b):
                                    choose="DODGE"
                                    maxh=b
                                elif(second==c):
                                    choose="RECHARGE"
                                    maxh=c
                        else:
                            choose="RECHARGE"
                            maxh=c
                        #choose next max here and give it                        
                    elif(maxh==b):
                        if(take[2]!=0):
                            choose="DODGE"
                            maxh=b
                            #choose next max here and give it
                        else:
                            choose="RECHARGE"
                            maxh=c

                    elif(maxh==c):
                        choose="RECHARGE"
                        maxh=c

                #6th testcase
                else:
                    store=maxh
                    if(maxh==a):
                        if(take[2]!=0):
                            if(take[1]!=0):
                                choose="SHOOT"
                                maxh=a 
                            else:
                                if(b==c):
                                    choose="RECHARGE"
                                    maxh=c
                                else:
                                    second=max(b,c)
                                    if(second==b):
                                        choose="DODGE"
                                        maxh=b
                                    elif(second==c):
                                        choose="RECHARGE"
                                        maxh=c
                    elif(maxh==b):
                        if(take[2]!=0):
                            choose="DODGE"
                            maxh=b
                        else:
                            maxh=c
                            choose="RECHARGE"
                    elif(maxh==c):
                        choose="RECHARGE"
                        maxh=c



            current_util[i]=maxh
            #print(a,b,c,"Values")
            res="(",take[0],take[1],take[2],")",":",choose,"=",current_util[i]
            print(res,file=f)
            print()
            print()
        print(file=f)
		print(file=f)

        #checking is crossed given delta value if yes our function is over
        store=0
        for iy in range(60):
            if(abs(current_util[iy]-prev_util[iy])>store):
                store=abs(current_util[iy]-prev_util[iy])
        md=0
        if(store<0.001):
            break
        for kk in range(60):
            prev_util[kk]=current_util[kk]

        if(md<delta[glo]):
            break

        #current_util[i]=0
        for ll in range(0,12):
            current_util[ll]=0
        for mm in range(12,60):
            current_util[mm]=0
        cou+=1

    f.close()
    glo=glo+1