import sys
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

def eval_fxn(s,f):
    return eval(s)

def read_input(filename):
    lines=[]
    with open(filename) as f:
        lines=f.readlines()
    f.close()
    dataset_num=int(lines[0])
    rules=[]
    for line in lines[1:]:
        line=line.split(',')
        if(len(line)==2):
            line[0]=line[0].strip()
            line[1]=line[1].strip()
            rules.append(line)
    return dataset_num,rules

def read_dataset(filename):
    lines=[]
    with open(filename) as f:
        lines=f.readlines()[1:]
    f.close()
    l=len(lines)
    train_data=[]
    test_data=[]
    for i in range(l):
        if i<0.8*l:
            temp=[]
            for j in lines[i].strip().split(','):
                try:
                    temp.append(float(j))
                except:
                    temp.append(j.strip())
            train_data.append(temp)
        else:
            temp=[]
            for j in lines[i].strip().split(','):
                try:
                    temp.append(float(j))
                except:
                    temp.append(j.strip())
            test_data.append(temp)
    return train_data,test_data

def get_tree_nodes(dataset_num,roll_num):
    fptr=open(str(roll_num)+'.tree','w')
    train_data,test_data=read_dataset('./dataset/dataset'+str(dataset_num)+'.csv')
    data=np.array(train_data+test_data)
    r,c=data.shape

    for i in range(c):
        try:
            data[:,i].astype('float')
        except:
            from sklearn import preprocessing
            le = preprocessing.LabelEncoder()
            le.fit(data[:,i])
            data[:,i]=le.transform(data[:,i])

    estimator = DecisionTreeClassifier(criterion='entropy')
    estimator.fit(data[:,:c-1],data[:,c-1])

    # The decision estimator has an attribute called tree_  which stores the entire
    # tree structure and allows access to low level attributes. The binary tree
    # tree_ is represented as a number of parallel arrays. The i-th element of each
    # array holds information about the node `i`. Node 0 is the tree's root. NOTE:
    # Some of the arrays only apply to either leaves or split nodes, resp. In this
    # case the values of nodes of the other type are arbitrary!
    #
    # Among those arrays, we have:
    #   - left_child, id of the left child of the node
    #   - right_child, id of the right child of the node
    #   - feature, feature used for splitting the node
    #   - threshold, threshold value at the node
    #

    # Using those arrays, we can parse the tree structure:

    n_nodes = estimator.tree_.node_count
    children_left = estimator.tree_.children_left
    children_right = estimator.tree_.children_right
    feature = estimator.tree_.feature
    threshold = estimator.tree_.threshold


    # The tree structure can be traversed to compute various properties such
    # as the depth of each node and whether or not it is a leaf.
    node_depth = np.zeros(shape=n_nodes, dtype=np.int32)
    is_leaves = np.zeros(shape=n_nodes, dtype=bool)
    stack = [(0, -1)]  # seed is the root node id and its parent depth
    while len(stack) > 0:
        node_id, parent_depth = stack.pop()
        node_depth[node_id] = parent_depth + 1

        # If we have a test node
        if (children_left[node_id] != children_right[node_id]):
            stack.append((children_left[node_id], parent_depth + 1))
            stack.append((children_right[node_id], parent_depth + 1))
        else:
            is_leaves[node_id] = True
    for i in range(n_nodes):
        if is_leaves[i]:
            fptr.write("%snode=%s leaf node.\n" % ("\t"*node_depth[i], i))
        else:
            fptr.write("%snode=%s test node: go to node %s if X[:, %s] <= %s else to "
                  "node %s.\n"
                  % (node_depth[i] * "\t",
                     i,
                     children_left[i],
                     feature[i],
                     threshold[i],
                     children_right[i],
                     ))
    fptr.close()
    # print(estimator.score(train_data[:,:c-1], train_data[:,c-1]),estimator.score(test_data[:,:c-1], test_data[:,c-1]))
    return np.sum(is_leaves)

def main(inp_file):
    dataset_num,rules=read_input(inp_file)
    roll_num=inp_file.split('.')[-2].split('/')[-1]
    max_tree_nodes=2*get_tree_nodes(dataset_num,roll_num)
    try:
        roll_int=int(roll_num)
    except:
        print(inp_file,"FILE_NAME_ERROR")
    d_num=roll_int%10+1
    if d_num!=int(dataset_num):
        print(roll_num,"WRONG DATASET")
    lst_digit=roll_int%10
    second_last_digit=(roll_int%100)//10
#    print(dataset_num,rules)
    train_data,test_data=read_dataset('dataset/dataset'+str(dataset_num)+'.csv')
#    print(train_data,test_data)
    total_entries=len(train_data)+len(test_data)
    swp1=(lst_digit+second_last_digit)%total_entries
    swp2=second_last_digit%total_entries
    if swp1==swp2:
        swp1=(second_last_digit+1)%total_entries

    train_score=0
    test_score=0

    lst_col=[]
    for i in train_data:
        lst_col.append(i[-1])
    lst_col=list(set(lst_col))
    
    opp_label={}
    opp_label[lst_col[0]]=lst_col[1]
    opp_label[lst_col[1]]=lst_col[0]

    l_t=len(train_data)
    if swp1<l_t:
        train_data[swp1][-1]=opp_label[train_data[swp1][-1]]
    else:
        test_data[swp1-l_t][-1]=opp_label[test_data[swp1-l_t][-1]]

    if swp2<l_t:
        train_data[swp2][-1]=opp_label[train_data[swp2][-1]]
    else:
        test_data[swp2-l_t][-1]=opp_label[test_data[swp2-l_t][-1]]
    for i in train_data:
        cnt=0
        for j in rules:
            if eval_fxn(j[0],i[:-1]):
                cnt+=1
#                print(i[-1],j[1])
                if i[-1]==j[1]:
                    cnt+=1
        if cnt==2:
            train_score+=1
#        else:
#           print(cnt,i)

    for i in test_data:
        cnt=0
        for j in rules:
            if j[1] not in lst_col:
                print(roll_num,"LABEL DOESN'T MATCH COLUMN ENTRY")
                exit()
            if eval_fxn(j[0],i[:-1]):
                cnt+=1
                if i[-1]==j[1]:
                    cnt+=1
        if cnt==2:
            test_score+=1
#        else:
#           print(cnt)
    if(train_score==0 and test_score==0):
        print(roll_num,"POSSIBLY ERROR / 0 SCORE")
    if(len(rules)>max_tree_nodes*(1+0.5*int(d_num>=8))):
        train_score*=0.8
        test_score*=0.8
    print(roll_num+','+str(train_score/len(train_data)*50+test_score/len(test_data)*50)+'\n')

if __name__=='__main__':
	try:
		import sys
		inp_file=sys.argv[1]
		main(inp_file)
	except:
		import sys
		roll_num=sys.argv[1].split('.')[-2].split('/')[-1]
		print(roll_num,"ERROR WHILE PARSING FILE")
