import copy

class lucky_v1():
    def __init__(self): 
        self.length_list = [4, 7, 44, 47, 74, 77, 444]
        self.range_list = [2, 8, 464, 4096, 18728400854, 75422540336, 3949534246514075237194788708873582383079842]
        self.pair_list = [[0,2], [0,1,2,3], [0,2,20,22], [0,1,2,3,20,21,22,23], [0,2,15,22,35,37], [0,1,2,3,15,16,22,23,35,36,37,38]]
        
        self.index = 0       #select the index of _list
        self.query = 0       #the real query
        self.limit = 0       #length // 2
        self.cursor = 1      #the amount of possibilities found. If equal to self.query then solution has been found
        self.solution = ""   #store solution
    
    def put(self, res, pos):
        res[pos] = "7"
        return res
    
    def generate(self, res, pos=0, num4=0, num7=0):
        if self.cursor > self.query: #once solution has been found we can end the recursive function
            return 
        if pos == self.limit: #we placed all possible '4' and '7'
            if num4 in self.pair_list[self.index] or num7 in self.pair_list[self.index]: #need to check if it's a SLP
                self.cursor += 1
                if self.cursor == self.query: #we hit the solution we're looking for
                    if self.length_list[self.index]%2 == 0: #if length is odd
                        self.solution = res + res[::-1]
                    else: #else we need to find what is the value of the middle digit
                        if num4*2 + 1 in self.length_list or num7*2 in self.length_list:
                            self.solution = res + ['4'] + res[::-1]
                        else:
                            self.solution = res + ['7'] + res[::-1]
        else:
            self.generate(res, pos + 1, num4 + 1, num7) #we simulate a placement of a "4"
            self.generate(self.put(copy.copy(res), pos), pos + 1, num4, num7 + 1) #we put a "7"
            
    def get_solution(self, query):
        self.query = query
        
        self.index = 0
        while self.query - self.range_list[self.index] > 0: #need to find what is the index of _list arrays
            self.query -= self.range_list[self.index]
            self.index += 1
        
        self.limit = self.length_list[self.index]//2
        self.cursor = 0
        
        self.generate(["4"]*self.limit) #generate() will create the solution inside the function
        
        return "".join(self.solution)
