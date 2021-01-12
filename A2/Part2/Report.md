the value iteration algorithm is used to obtain the optimal policy and the state reward values
corresponding to it.

FRom the following code we find the new utility by using the old utilities, gamma and step
reward by the Bellman Update equation.
Since we use Value Iteration algorithm, we check if the max difference of the utilities
between previous iteration and present iteration to be greater than delta.If not then the
algorithm ends and the result is stored in a file.
If the max difference is greater than delta, we update the utilities and continue the algorithm
by doing the action which gives the maximum reward and print it.So, we repeat this until the
maximum difference becomes less than delta. Since our Team number is 48
, our penalty is
-20


TASK 2
Here we take step cost as -2.5 as mentioned.
Part 1 ​ :
Also the step cost of shoot function is changed to -0.25
Here also we initialize the states, previous utilities and actions with some default values
appropriate to the algorithm and call the algorithm.
Here we can observe that parameters in the calling function had been changed as per the
new values.
Part 2 :
Here the gamma( γ ) value is changed to 0.1.So, we just need to change a little in the
implementation function
Here also we initialize the states, previous utilities and actions with some default values
appropriate to the algorithm and call the algorithm.
Here we can observe that parameters in the calling function had been changed as per the
new values.
Lero’s Weird Behaviour :
The no of iterations lero took to converge with γ = 0.99 is 103.
And with γ = 0.1 is 4.
This drastic reduction in no of iterations is due to consideration of low value of γ . Since in
the bellman Update we multiply the future reward with γ , the very low value of γ results in
geometrical reduction of utility of each state which makes it to converge faster.
Since the iterations performed are less for γ = 0.1 , the reward R(s,a) in bellman Update
equation will be added less no of times, utilities will be more than for γ = 0.99 .
Also, the no of cases of utilities for dodging and recharging being same are increased, lero
randomly picks one which shows a weird behaviour in policy



Part 3 :
Since this is continuation of part 2, gamma( γ ) is 0.1 and delta( δ) is now changed to 10 ^
−10
This also needs only a few changes in the implementation function
Here also we initialize the states, previous utilities and actions with some default values
appropriate to the algorithm and call the algorithm.
Here we can observe that parameters in the calling function had been changed as per the
new values.
Observation :
As seen in previous case, with γ = 0.1 and δ = 10 the no of iterations are 4,
now with −3 γ = 0.1 and δ = 10 we observe no of iterations go to 10.
This can be explained as since the δ value drastically reduced, the target for maximum
difference is drastically reduced.
So, it requires more iterations for reduction in utilities which in case reduces the maximum
difference between previous and present utilities until it reaches δ .
