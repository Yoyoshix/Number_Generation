class lucky_v4():
    def __init__(self):
        self.query = 0
        self.limit = 0 #length//2, useful here and there
        self.pair = [] #store the pair numbers
        self.seven_amount = 0 #the amount of seven needed to know if the middle digit of odd length palindrom is 4 or 7
        self.solution = "" #store solution
    
    def is_lucky(self, length):
        if any(x in str(length) for x in "01235689"):
            return 0
        return 1
    
    def get_pair(self, length):
        pair = []
        is_odd = length % 2
        limit = length // 2
        total = 0
        for x in range(0, limit+1):
            #Need to *2 because we will process only one side of palindrome
            if self.is_lucky(x*2+is_odd) == 1 or self.is_lucky(x*2) == 1 or \
            self.is_lucky(length-x*2-is_odd) == 1 or self.is_lucky(length-x*2) == 1:
                pair.append(x)
        return pair
    
    def fact(self, n):
        if n == 0:
            return 1
        res = 1
        while n > 1:
            res *= n
            n -= 1
        return res

    def binomial(self, n, k):
        return self.fact(n) // (self.fact(k) * self.fact(n-k))
    
    def get_lucky_from_index(self, index):
        binary = "{0:b}".format(index+2)
        res = 0
        for idx, i in enumerate(binary[1:]):
            res += (4 if i == "0" else 7) * 10**(len(binary)-idx-2)
        return res
        
    def get_solution(self, query):
        index = 0
        while query > 0:
            total = 0
            length = self.get_lucky_from_index(index)
            self.limit = length // 2                  #get half the length because palindrom
            self.pair = self.get_pair(length)
            for i in self.pair:
                total += self.binomial(self.limit, i)
            query -= total
            index += 1
        
        query += total
        query -= 1 #offset of 1 because there is a difference between input value and the one used in the algorithm
        self.seven_amount = 0
        self.solution = ["4"] * self.limit
        
        self.slp_algorithm(query) #everything
        
        if length%2 == 0:
            self.solution = self.solution[::-1] + self.solution
        else: #we do this because if number is odd we need to fill the middle of the palindrom
            if self.is_lucky(self.seven_amount*2+1) == 1 or self.is_lucky((self.limit-self.seven_amount)*2) == 1:
                self.solution = self.solution[::-1] + ["7"] + self.solution
            else:
                self.solution = self.solution[::-1] + ["4"] + self.solution
        
        return "".join(self.solution)

    def get_comb(self, length, offset=0):
        """ return the combination array depending of length and self.pair
        offset is used to decrease the value in pair array to create a better generic function
        
        combination (or comb) array works like this :
        for each index inside length we calculate the amount of possible combination that exists
        we simply use the binomial coeficient to get the values
        if parameters are wrong it stores 0 at current index
        
        Exemple : if length = 4 and pair = [2,3,4]
        The possibilities are : 0011, 0101, 0110, 0111, 1001, 1010, 1011, 1100, 1101, 1110, 1111 (11 possibilities)
        The comb array will return : [0,1,4,11]
        
        Why ? Let's explain step by step
        "0" in the current comb array means that there is no possibility to place our 1's within a length of 1
            "length of 1" is determine by the index of the value +1 ("0" is at index 0, so we add +1)
            
        "1" means that within a length of 2 we can have one possibility to place the 1's
            possibility is : 11 (we then add 0s at the start because we need to return a string of 4 digits)
            
        "4" means that there is 4 possibilities within a length of 3
            possibilities are : 011, 101, 110, 111
        
        "11" (the last value in array) gives the amount of all possibilites with the length of 4
        """
        comb = []
        for pos in range(1, length+1):
            total = 0
            for i in self.pair:
                i -= offset
                if i <= pos:
                    total += self.binomial(pos, i)
            comb.append(total)
        return comb
    
    def slp_algorithm(self, cursor, pos=0, depth=0): #See top of file to better understand the algorithm
        if self.pair[0] - depth < 0: #update if the amount of seven is higher than the least pair value
            del self.pair[0]
        if cursor < 0: #a simple exception (it happens when all 7s are everywhere)
            return
        if cursor == 0: #if we're here, all remaining 7s to put will be placed at the beginning of the string
            for i in range(self.pair[0] - depth):
                self.solution[i] = "7"
                self.seven_amount += 1
            return
        
        comb = self.get_comb(self.limit - pos, depth) #get the comb array
        idx = 0
        while idx < self.limit - depth and cursor >= comb[idx]: #self.limit - pos = len(comb), so it's FASTER
            idx += 1
        self.solution[idx] = "7" #place the 7 at current index
        self.seven_amount += 1
        cursor -= comb[idx-1] #we update the value of cursor
        self.slp_algorithm(cursor, self.limit - idx, depth + 1)
