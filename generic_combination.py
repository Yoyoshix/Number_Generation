import scipy.special
import copy

def get_comb(length, pair, offset=0):
    for i in range(len(pair)):
        pair[i] -= offset
    comb = []
    for pos in range(1, length+1):
        total = 0
        for i in pair:
            if i <= pos:
                total += scipy.special.binom(pos, i)
        comb.append(total)
    return comb

def recurs(res, cursor, pos, pair, depth):
    if cursor < 0:
        return "".join(res[::-1])
    if cursor == 0:
        idx = 0
        while pair[idx] < depth:
            idx += 1
        min_pair = pair[idx] - depth
        for i in range(min_pair):
            res[i] = "1"
        return "".join(res[::-1])
    length = len(res) - pos
    comb = get_comb(length, copy.copy(pair), depth)
    idx = 0
    while idx < len(comb) and cursor >= comb[idx]:
        idx += 1
    res[idx] = "1"
    cursor -= comb[idx-1]
    return recurs(res, cursor, len(res) - idx, pair, depth + 1)
