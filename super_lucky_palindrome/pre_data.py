import scipy.special

def is_lucky(length):
    if any(x in str(length) for x in "01235689"):
        return 0
    return 1

def possibilities(length):
    pair = []
    limit = length//2    #palindrom middle
    is_odd = length%2
    total = 0
    for x in range(0, limit+1):
        #Need to *2 because we will process only one side of palindrome
        if is_lucky(x*2+is_odd) == 1 or is_lucky(x*2) == 1 or is_lucky(length-x*2-is_odd) == 1 or is_lucky(length-x*2) == 1:
            pair.append(x)
    for i in pair:
        total += scipy.special.binom(limit, i)
    print(length, pair, int(total))
    return total

for i in range(4,4445): #We hit the infinity barrier at 4444 number length 
    if is_lucky(i) == 1:
        possibilities(i)
