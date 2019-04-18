import scipy.special

def get_comb(length, pair, offset=0):
    comb = []
    for pos in range(1, length+1):
        total = 0
        for i in pair:
            i -= offset
            if i <= pos:
                total += scipy.special.comb(pos, i, exact=True)
        comb.append(total)
    return comb

def solve(length, pair, cursor):
    if cursor >= get_comb(length, pair)[-1] or cursor < 0:
        return None
    
    res = ["0"] * length
    pos = 0
    amount = 0
    
    while cursor > 0:
        comb = get_comb(length, pair, amount)
        idx = 0
        while idx < len(comb) and cursor >= comb[idx]:
            idx += 1
        res[idx] = "1"
        
        if idx > 0:
            cursor -= comb[idx-1]
        else:
            break
        length = idx
        amount += 1
    
    if cursor == 0:
        idx = 0
        while pair[idx] < amount:
            idx += 1
        for i in range(pair[idx] - amount):
            res[i] = "1"
    
    return "".join(res[::-1])


length = 4
pair = [2,3,4]
for cursor in range(get_comb(length, pair)[-1]):
    print(solve(length, pair, cursor), cursor)
