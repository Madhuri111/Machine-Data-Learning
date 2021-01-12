import pickle
import numpy as np
import operator
from operator import itemgetter
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures

infile1 = open("X_train.pkl",'rb')
new_trx = pickle.load(infile1)


infile2 = open("X_test.pkl",'rb')
new_tsx = pickle.load(infile2)


infile3 = open("Fx_test.pkl",'rb')
new_tsy = pickle.load(infile3)


infile4 = open("Y_train.pkl",'rb')
new_try = pickle.load(infile4)


final_bias=[]
final_var=[]
for i in range(1,10):
	temp=[]
	for j in range(1,20,1):
		my_sets=np.reshape(new_trx[j],(-1,1))
		your_sets=np.reshape(new_try[j],(-1,1))
		dy=np.reshape(new_tsy,(-1,1))
		dx=np.reshape(new_tsx,(-1,1))
		poly_here=PolynomialFeatures(degree=i)
		my_poly=poly_here.fit_transform(my_sets)
		madhuri=LinearRegression().fit(my_poly,your_sets)
		dx=poly_here.fit_transform(dx)
		huhu=madhuri.predict(dx)
		temp.append(huhu)

	arr_bias=[]
	arr_var=[]
	for k in range(0,80,1):
		calc=(list(map(itemgetter(k),temp)))
		only=abs(np.mean(calc)-new_tsy[k])
		only=only*only
		arr_bias.append(only)
		var1=(np.mean(calc))
		var2=np.mean(abs((calc-var1)*(calc-var1)))
		arr_var.append(var2)
	there=np.mean(arr_bias)
	their=np.mean(arr_var)
	final_bias.append(there)
	final_var.append(their)

arr=[]
for me in range(1,10):
	arr.append(me)

print("      Bias          ",'   ',"Variance     ")
for i in range(9):
	print(i+1,final_bias[i],'  ',final_var[i])

	poly_here=PolynomialFeatures(degree=j,interaction_only=True)
	plt.plot(arr, final_bias, color="b")
	plt.plot(arr, final_var, color="r")
	plt.title('Bias^2 vs Variance')
	plt.legend(('Bias Squared', 'Variance'), loc='best')
	plt.xlabel("Complexity")
	plt.ylabel("Error")
plt.show()
