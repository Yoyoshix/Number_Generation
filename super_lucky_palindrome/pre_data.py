import scipy.special

def is_lucky(number): #this return 1 if the number is a lucky number
    if any(x in str(number) for x in "01235689"):
        return 0
    return 1

def get_pair(length): #return pair numbers
    pair = []
    limit = length // 2
    is_odd = length % 2
    
    #About the big condition, it simulates every possible cases.
    #length-amount_4 is the amount of "7" and I always multiply by 2 to represent the full length of the final result
    #and +is_odd simulates the middle digit being a "4" or a "7"
    for amount_4 in range(0, limit+1): #I do +1 because there can be a "4" everywhere
        if is_lucky(amount_4*2) == 1 or is_lucky(length-amount_4*2) == 1 or \
        is_lucky(amount_4*2+is_odd) == 1 or is_lucky(length-amount_4*2-is_odd) == 1:
            pair.append(amount_4)
    return pair

def get_possibilities(length, pair): #return the amount of possibilities
    total = 0
    for i in pair:
        total += scipy.special.comb(length, i, exact=True) #get all possibilities. Exact=True return an integer
    return total
