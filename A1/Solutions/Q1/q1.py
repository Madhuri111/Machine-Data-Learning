import pickle
import numpy as np
import operator
from operator import itemgetter
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
import pandas as pd

infile = open("data.pkl",'rb')
new_dict = pickle.load(infile)


X_train, X_test = train_test_split(new_dict, train_size=0.9,test_size=0.1, random_state=1)

y_train=(list(map(itemgetter(1),X_train)))
y_test=(list(map(itemgetter(1),X_test)))
X_train=list(map(itemgetter(0),X_train))
X_test=list(map(itemgetter(0),X_test))


final_bias=[]
final_var=[]
final_norm=[]

my_sets=np.array_split(X_train,10)
your_sets=np.array_split(y_train,10)

for degree in range(1,10):
    temp=[]
    arr_bias=[]
    arr_var=[]
    arr_norm=[]
    for ds in range(10):
        xtr = np.array([my_sets[ds]]).T
        ytr = np.reshape(your_sets[ds],(-1,1))
        yts=np.reshape(y_test,(-1,1))
        xts=np.reshape(X_test,(-1,1))
        poly_here=PolynomialFeatures(degree=degree)
        my_poly=poly_here.fit_transform(xtr)
        madhuri=LinearRegression().fit(my_poly,ytr)
        xts=poly_here.fit_transform(xts)
        pred=madhuri.predict(xts)
        temp.append(pred)

    calc=0
    only=0
    var2=0
    var1=0
    i=0

#print(temp[0].T[0])
# temp[i].T[0] => i+1th degree, all predictions
    preds = []
    for i in range(9):
        preds.append(temp[i].T[0])
    temp = np.array(preds)

#temp[i] => numpy array of predictions of ith polynomial
#print(temp)
    tot_bias = 0
    tot_var=0
    for k in range(500):
        tot_bias += np.mean(((temp.T[k]-y_test[k])**2))
        tot_var += (np.mean(np.var(preds,axis=0)))
    tot_bias/=500
    tot_var/=500
    final_bias.append(tot_bias)
    final_var.append((tot_var))


arr=[]
for me in range(1,10):
    arr.append(me)

print("        Bias          ",'       ',"Variance     ")
for i in range(9):
    print(i+1,'   ',final_bias[i],'    ',final_var[i])
    poly_here=PolynomialFeatures(degree=i,interaction_only=True)
    plt.plot(arr, final_bias, color="b")
    plt.plot(arr, final_var, color="r")
    plt.title('Bias^2 vs Variance')
    plt.legend(('Bias Squared', 'Variance'), loc='best')
    plt.xlabel("Complexity")
    plt.ylabel("Error")
plt.show()
