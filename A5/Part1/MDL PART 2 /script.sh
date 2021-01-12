# Put all the following files in the same directory
# make_pomdp_file.py
# pomdpsol
# pomdpeval

mkdir newstuff

python3 make_pomdp_file.py
# here enter your roll number and question number 0,1,2,3 respectively


# after the above step, copy paste all these files
./pomdpsol --output newstuff/2018101042_0.policy  newstuff/2018101042_0.pomdp > newstuff/2018101042_0.out
./pomdpsol --output newstuff/2018101042_1.policy  newstuff/2018101042_1.pomdp > newstuff/2018101042_1.out
./pomdpsol --output newstuff/2018101042_2.policy  newstuff/2018101042_2.pomdp > newstuff/2018101042_2.out
./pomdpsol --output newstuff/2018101042_3.policy  newstuff/2018101042_3.pomdp > newstuff/2018101042_3.out
./pomdpeval --simLen 100 --simNum 1000 --policy-file newstuff/2018101042_0.policy newstuff/2018101042_0.pomdp > newstuff/2018101042_0.eval 
./pomdpeval --simLen 100 --simNum 1000 --policy-file newstuff/2018101042_1.policy newstuff/2018101042_1.pomdp > newstuff/2018101042_1.eval 
./pomdpeval --simLen 100 --simNum 1000 --policy-file newstuff/2018101042_2.policy newstuff/2018101042_2.pomdp > newstuff/2018101042_2.eval 
./pomdpeval --simLen 100 --simNum 1000 --policy-file newstuff/2018101042_3.policy newstuff/2018101042_3.pomdp > newstuff/2018101042_3.eval 
