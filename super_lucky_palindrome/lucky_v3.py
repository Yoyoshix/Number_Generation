import copy
import numpy as np
import scipy.special
import time

class lucky_v3():
    def __init__(self):
        #List of possible length   
        self.length_list = [4, 7, 44, 47, 74, 77, 444, 447, 474, 477, 744, 747, 774, 777]
        #Amount of solutions by length. To use this I do query-range_list, once query becomes <=0 I go out the loop and do query+range_list
        self.range_list = [2, 8, 464, 4096, 18728400854, 75422540336, 3949534246513022733692774166275217636196352, 27912724205136969367829202079257831965458432, 54901863838981370331031720163633347084419072, 408867219021824519558760381286789756865216512, 731060835093268059719935428380319894767978536241103340770302477220618973863638154274876419272070389261402112, 3028768728981208771138392332161427475712344495983372066026850069568299204087095837473068158977043396135223296, 383767495066681352637998366663200070705183074877734592607500475472627707939626649121930829298776144224727016144896, 1564887013153773591096691217957484965016329465244742414975904717557119142894155366820818937587853276546953480503296]
        #(this explanation is true for the first half of the number) List of the possible amount of 4's and 7's for each length.
        self.pair_list = [[0,2], [0,1,2,3], [0,2,20,22], [0,1,2,3,20,21,22,23], [0,2,15,22,35,37], [0,1,2,3,15,16,22,23,35,36,37,38], [0,2,22,37,185,200,220,222], [0,1,2,3,22,23,37,38,185,186,200,201,220,221,222,223], [0,2,15,22,37,200,215,222,235,237], [0,1,2,3,15,16,22,23,37,38,200,201,215,216,222,223,235,236,237,238], [0,2,22,37,135,150,222,237,335,350,370,372], [0,1,2,3,22,23,37,38,135,136,150,151,222,223,237,238,335,336,350,351,370,371,372,373], [0,2,15,22,37,150,165,222,237,350,365,372,385,387], [0,1,2,3,15,16,22,23,37,38,150,151,165,166,222,223,237,238,350,351,365,366,372,373,385,386,387,388]]
        
        self.limit = 0 #length//2, useful here and there
        self.seven_amount = 0 #the amount of seven needed to get the middle digit of odd length palindrom
        self.pair = [] #store self.pair_list[self.index]
        self.solution = "" #store solution
    
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
                    total += scipy.special.binom(pos, i)
            comb.append(total)
        return comb
    
    def get_solution(self, query):
        index = 0
        while query - self.range_list[index] > 0: #we access the right index to access to the right parameters
            query -= self.range_list[index]
            index += 1
        
        query -= 1 #offset of 1 because there is a difference between input value and the one used in the algorithm
        self.limit = self.length_list[index]//2 #get half the length because palindrom
        self.seven_amount = 0
        self.pair = copy.copy(self.pair_list[index]) #we copy this because algorithm will alter the array
        self.solution = ["4"] * self.limit
        
        self.slp_algorithm(query) #everything
        
        if self.length_list[index]%2 == 0:
            self.solution = self.solution[::-1] + self.solution
        else: #we do this because if number is odd we need to fill the middle of the palindrom
            if self.seven_amount*2+1 in self.length_list or (self.limit-self.seven_amount)*2 in self.length_list:
                self.solution = self.solution[::-1] + ["7"] + self.solution
            else:
                self.solution = self.solution[::-1] + ["4"] + self.solution
        
        return "".join(self.solution)
    
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
