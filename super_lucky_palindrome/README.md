The original problem : https://www.spoj.com/problems/CTPLUCKY/

Here you'll find 3 versions (I'm planning for a forth one)

v1 : Naive solution \
Not optimized at all. Just do its job. \
Here is some timing on my pc : \
val = 100 in 0.021 sec \
val = 1000 in 0.052 sec \
val = 10000 in 1.882 sec \
val = 100000 in 8.231 sec \
val = 1000000 in 39.543 sec \
val = 10000000 in 231.087 sec \
 \
v2 : Naive solution optimized \
The idea is to detect early during the recursive function if the amount of seven to put will be incrorrect depending of the current position. \
Here is some timing : \
val = 100 in 0.001 sec \
val = 1000 in 0.004 sec \
val = 10000 in 0.087 sec \
val = 100000 in 1.165 sec \
val = 1000000 in 10.743 sec \
val = 10000000 in 98.939 sec \
 \
v3 : Mathematical approach using combination formulas \
Well. You can check the explanation dedicated to this algorithm to better understand its working \
Here are some shocking timing : \
val = 100 in 0 sec \
val = 1000 in 0 sec \
val = 10000 in 0 sec \
val = 100000 in 0.001 sec \
val = 1000000 in 0 sec \
val = 10000000 in 0.001 sec \
val = 100000000 in 0.0 sec \
val = 1000000000 in 0.001 sec \
val = 10000000000 in 0.001 sec \
val = 100000000000 in 0.003 sec \
val = 1000000000000 in 0.003 sec \
val = 10000000000000 in 0.003 sec \
val = 100000000000000 in 0.002 sec \
val = 1000000000000000 in 0.003 sec \
val = 10000000000000000 in 0.003 sec \
val = 100000000000000000 in 0.004 sec \
val = 1000000000000000000 in 0.004 sec (10^18, yeah) \
 \
Because the v3 is not calculating every existing solutions I can not be sure that the algorithm is working perfectly. \
BUT \
I checked until some high number and everything was ok until a certain point. \
The problem is that when number are too big, float numbers that I get from the binomial formula are not precise enough and create a wrong result. \
 \
This is the reason I'll try to work on a v4 that will store digits in array and process calculus from there. \
That way I'll remain exact on my results to the cost of some longer executions.

22h45 : 17 March 2019 \
v4 is done \
Algorithm is done \
Everything is done and complete \
I never expected the algorithm to be this fast. It's really incredible. Thanks python to have no limits of digits with your integers \
