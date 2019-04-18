"""
I fixed the line 36 after I detected there was a mistake working with float numbers because they were not precise enough
the original code I worked with was wrong but I fixed it for github
"""

import scipy.special

#return 1 if number is a lucky number
def is_lucky(length):
    if any(x in str(length) for x in "01235689"):
        return 0
    return 1

#return the pair numbers that follows the rules of a lucky palindrome number
def get_pair(length):
    pair = []
    limit = length // 2    #palindrom middle
    is_odd = length % 2
    
    #to optimize the algorithm, we need to work with only one side of the palindrom (because palindrome are mirrors)
    #the for loop will simulate the process of the algorithm
    #we check for every amount of 4 and 7 within only one part of the palindrome if they are a lucky number
    #so we need to *2 to get the real total amount of 4 and 7 and one of these two values need to be a lucky number
    #we also need to adapt this formula for odd length lucky numbers
    #because the middle digit can be either a 4 or a 7, we need to check both possibility, which implies 4 differents check of is_lucky()
    for amount_4 in range(0, limit+1):
        if is_lucky(amount_4*2+is_odd) == 1 or is_lucky(amount_4*2) == 1 or \
        is_lucky(length-amount_4*2-is_odd) == 1 or is_lucky(length-amount_4*2) == 1:
            pair.append(amount_4)
    return pair

#total amount of posibilities depending of length of the number and pair numbers
def get_possibilities(length, pair):
    total = 0
    for i in pair:
        total += scipy.special.comb(length, i, exact=True)
    return total

for i in range(4,445): #We stop at index 10^18 because that's the problem's statement, 444 length reach that index
    if is_lucky(i) == 1:
        pair = get_pair(i)
        print(i, pair, get_possibilities(i//2, pair))
