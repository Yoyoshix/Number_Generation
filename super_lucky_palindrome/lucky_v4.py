import scipy.special

class lucky_v4():
    def __init__(self):
        self.query = 0
        self.seven = 0
        self.solution = ""
        
    def is_lucky(self, number): #detect if number is a lucky number
        if any(x in str(number) for x in "01235689"):
            return 0
        return 1
    
    def get_length_from_index(self, index): #create correct SLP length
        binary = "{0:b}".format(index+2)
        res = ""
        for idx, i in enumerate(binary[1:]):
            res += "4" if i == "0" else "7"
        return int(res)
    
    def get_palindrome_pair(self, length):
        pair = []
        is_odd = length % 2
        limit = length // 2
        total = 0
        for x in range(0, limit+1):
            if self.is_lucky(x*2+is_odd) == 1 or self.is_lucky(x*2) == 1 or \
            self.is_lucky(length-x*2-is_odd) == 1 or self.is_lucky(length-x*2) == 1:
                pair.append(x)
        return pair
    
    def get_possibilities(self, length, pair): #return the amount of possibilities
        total = 0
        for i in pair:
            total += scipy.special.comb(length, i, exact=True)
        return total
    
    def generate(self, query, pair_numbers, length):
        pair = pair_numbers
        space = length
        self.solution = ["4"] * length
        self.seven = 0 #we assume that the solution is filled by "4" where some of "4" will be replaced by "7"
        
        idx = space
        while query > 0:
            remove = query + 1
            while idx >= 0 and query < remove: #get the correct idx.
                remove = self.get_possibilities(idx, pair)
                idx -= 1
            self.solution[idx+1] = "7"
            self.seven += 1
            query -= remove #decrease the value of query by the amount of useless solutions
            space = idx
            for i in range(len(pair)): #update pair numbers
                pair[i] -= 1
            if pair[0] < 0: #delete because useless
                del pair[0]
        
        if query == 0: #here we put the rest of "7" that needs to be added
            for i in range(pair[0]):
                self.solution[i] = "7"
                self.seven += 1
                
        self.solution = "".join(self.solution)
        return self.solution
        
    def get_solution(self, query): #let's go
        self.query = query
        
        index = 0
        while self.query > 0: #we need to know the length of the solution
            length = self.get_length_from_index(index) #we first get the length of out current lucky number
            pair = self.get_palindrome_pair(length) #we determine the pair numbers of the length
            limit = length // 2
            total = self.get_possibilities(limit, pair) #we calculate how much possibilities exist
            self.query -= total
            index += 1
        self.query += total - 1       #go back one step to know what is the real query
        
        self.generate(self.query, pair, limit) #everything
        
        if length%2 == 0: #we create the whole number from one side of it
            self.solution = self.solution[::-1] + self.solution
        else:                                        #we determine what is the value of the middle digit
            if self.is_lucky(self.seven*2 + 1) == 1 or self.is_lucky((limit - self.seven)*2) == 1:
                self.solution = self.solution[::-1] + "7" + self.solution
            else:
                self.solution = self.solution[::-1] + "4" + self.solution
        
        return self.solution
