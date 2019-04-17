import copy
import scipy.special

class lucky():
    def __init__(self, query=0):
        #List of possible length   
        self.length_list = [4,7,44,47,74,77,444,447,474,477,744,747,774,777]
        #Amount of solutions by length. To use this I do query-range_list, once query becomes <=0 I go out the loop and do query+range_list
        self.range_list = [2, 8, 464, 4096, 18728400854, 75422540336, 3949534246513022733692774166275217636196352, 27912724205136969367829202079257831965458432, 54901863838981370331031720163633347084419072, 408867219021824519558760381286789756865216512, 731060835093268059719935428380319894767978536241103340770302477220618973863638154274876419272070389261402112, 3028768728981208771138392332161427475712344495983372066026850069568299204087095837473068158977043396135223296, 383767495066681352637998366663200070705183074877734592607500475472627707939626649121930829298776144224727016144896, 1564887013153773591096691217957484965016329465244742414975904717557119142894155366820818937587853276546953480503296]
        #(this explanation is true for the first half of the number) List of amount of 4's and 7's for each length. pair_list works like this : pair_list[length_index][amount_of_4]. If you know the length and the amount of 4 you can find the amount of 7 with length-amount_of_4. Very useful   
        self.pair_4list = [[0,2], [0,1,2,3], [ 0, 2,20,22], [ 0, 1, 2, 3,20,21,22,23], [ 0, 2,15,22,35,37], [ 0, 1, 2, 3,15,16,22,23,35,36,37,38], [  0,  2, 22, 37,185,200,220,222], [  0,  1,  2,  3, 22, 23, 37, 38,185,186,200,201,220,221,222,223], [  0,  2, 15, 22, 37,200,215,222,235,237], [  0,  1,  2,  3, 15, 16, 22, 23, 37, 38,200,201,215,216,222,223,235,236,237,238], [  0,  2, 22, 37,135,150,222,237,335,350,370,372], [  0,  1,  2,  3, 22, 23, 37, 38,135,136,150,151,222,223,237,238,335,336,350,351,370,371,372,373], [  0,  2, 15, 22, 37,150,165,222,237,350,365,372,385,387], [  0,  1,  2,  3, 15, 16, 22, 23, 37, 38,150,151,165,166,222,223,237,238,350,351,365,366,372,373,385,386,387,388]]
        self.pair_7list = [[2,0], [3,2,1,0], [22,20, 2, 0], [23,22,21,20, 3, 2, 1, 0], [37,35,22,15, 2, 0], [38,37,36,35,23,22,16,15, 3, 2, 1, 0], [222,220,200,185, 37, 22,  2,  0], [223,222,221,220,201,200,186,185, 38, 37, 23, 22,  3,  2,  1,  0], [237,235,222,215,200, 37, 22, 15,  2,  0], [238,237,236,235,223,222,216,215,201,200, 38, 37, 23, 22, 16, 15,  3,  2,  1,  0], [372,370,350,335,237,222,150,135, 37, 22,  2,  0], [373,372,371,370,351,350,336,335,238,237,223,222,151,150,136,135, 38, 37, 23, 22,  3,  2,  1,  0], [387,385,372,365,350,237,222,165,150, 37, 22, 15,  2,  0], [388,387,386,385,373,372,366,365,351,350,238,237,223,222,166,165,151,150, 38, 37, 23, 22, 16, 15,  3,  2,  1,  0]]
        
        self.query = query
        self.solution = "" #store solutions
        self.cursor = 1 #store current solution index
        self.index = 0 #store current index of *_list variable
        self.target = 0
        self.limit = 0
        
    def get_solution(self, target):
        if target <= 0:
            print("lol k")
            return None
        if target > self.range_list[-1]:
            print("Number too big")
            return None
        
        self.index = 0
        while target-self.range_list[self.index] > 0:
            target -= self.range_list[self.index]
            self.index += 1
        
        reverse = 0
        if target-self.range_list[self.index]//2 > 0:
            target = self.range_list[self.index] - target + 1
            reverse = 1
        
        if target == 1:
            if reverse == 0:
                return "4"*self.length_list[self.index]
            if reverse == 1:
                return "7"*self.length_list[self.index]
        
        self.cursor = 1
        self.target = target
        self.solution = ""
        self.limit = self.length_list[self.index]//2
        res = [""]*self.limit
        self.generate(res, 0, 0, 0)
        
        if reverse == 0:
            return "".join(self.solution)
        res = []
        for i in self.solution:
            if i == "4":
                res += "7"
            else:
                res += "4"
        return "".join(res)
        
    def put(self, res, pos, val):
        res[pos] = val
        return res
    
    def generate(self, res, pos, num4, num7):
        if self.cursor > self.target:
            return
        if pos == self.limit:
            if self.length_list[self.index]%2 == 0:
                if num4*2 in self.length_list or num7*2 in self.length_list:
                    if self.cursor == self.target:
                        self.solution = res + res[::-1]
                    self.cursor += 1
            else:
                if num4*2 + 1 in self.length_list or num7*2 in self.length_list:
                    if self.cursor == self.target:
                        self.solution = res + ['4'] + res[::-1]
                    self.cursor += 1
                if num4*2 in self.length_list or num7*2 + 1 in self.length_list:
                    if self.cursor == self.target:
                        self.solution = res + ['7'] + res[::-1]
                    self.cursor += 1
        else:
            self.generate(self.put(copy.copy(res), pos, "4"), pos + 1, num4 + 1, num7)
            self.generate(self.put(copy.copy(res), pos, "7"), pos + 1, num4, num7 + 1)
