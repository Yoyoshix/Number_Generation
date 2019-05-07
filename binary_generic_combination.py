import copy
import scipy.special

def get_possibilities(length, pair): #determine how much possibility for a given length
    total = 0
    for i in pair:
        if i <= length:
            total += scipy.special.comb(length, i, exact=True) #exact=True return a int instead of a float
        else:
            break
    return total

def exponential_search(length, pair, query):
    idx = length-2 #start at end of array
    step = 1 #helps moving on the array 
    current = -1 #store current value
    best_idx = -1 #return idx
    best_val = 0 #return value
    over_it = False #once we've got over the target we will change the behavior of step

    while step > 0: #while we can move
        if over_it == True:
            step = step // 2 #need to reduce the steps to get precise

        current = get_possibilities(idx+1, pair)
        if current <= query:
            if over_it == False: #exception when breaking the point for the first time
                step = step // 4
                over_it = True #we know we crossed the line so we now need to get precise
                if idx == length-2: #another exception
                    step = 1
            best_val = current #saves the best values
            best_idx = idx
            idx += step
        else:
            idx -= step

        if over_it == False:
            step *= 2       #need to increase the step to go further and faster

    return best_idx+1, best_val

def generate(length, pair_numbers, query, digits=["0", "1"]):
    space = length
    pair = copy.copy(pair_numbers)
    solution = [digits[0]] * length
    
    idx = 0
    remove = 1
    while query > 0 and remove > 0:
        idx, remove = exponential_search(space, pair, query)
        if idx >= length:
            return None
        solution[idx] = digits[1]

        query -= remove
        space = idx
        for i in range(len(pair)): #update pair numbers
            pair[i] -= 1
        if pair[0] < 0: #delete because useless
            del pair[0]

    if query == 0:
        for i in range(pair[0]): #sometimes there is some remaining digits to put
            solution[i] = digits[1]
    space = 0

    return "".join(solution[::-1])
