import scipy.special
import time
from sys import stdout

class lucky_v5():
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.start_time_global = 0
        self.start_time_segment = 0
        
        self.query = 0
        self.cursor = 0
        self.length = 0
        self.limit = 0
        self.pair = []
        self.seven_amount = 0
        self.reverse = False
        self.total = 0
        self.solution = ""
        
    def verbose_print(self, text_index): #ignore this, it's just display
        if self.verbose == False:
            return
                                        #stdout.write is able to print on the same line by replacing previous print
        if text_index == 0:
            self.start_time_global = time.time()
            print("Algorithm started")
        if text_index == 1:
            stdout.write("\rSolution will have a length of %d. Current length of amount of possibilities is %d" \
                % (self.length, len(str(self.total))))
        if text_index == 2:
            print("\n")
            if self.reverse == 1:
                print("Solution will be reversed")
            print("Starting length of real query : %d." % (len(str(self.query))))
            print("Real query :", self.query)
            print()
        if text_index == 3:
            length = len(str(self.query))
            left_space = self.limit-self.space
            percent = int((left_space*100)/self.limit)
            time_elapsed = int(time.time() - self.start_time_segment)
            stdout.write("\rCurrent length of real query %d. Cursor at position %d/%d (%d%%). Amount of \"7\" put %d. Time elapsed %ds." \
                % (length, left_space, self.limit, percent, self.seven_amount, time_elapsed))
        if text_index == 4:
            print("\n")
            print("Algorithm finished. Total time elapsed", time.time() - self.start_time_global)
            print("Solution have a length of", len(self.solution), "and have", self.solution.count("4"), "'4' and", \
                  self.solution.count("7"), "'7'")
            print()
    
    def is_lucky(self, number): #return 1 if number is a lucky number
        if any(x in str(number) for x in "01235689"):
            return 0
        return 1
    
    def get_palindrome_pair(self, length): #return amount of 4 and 7 that one side of a SLP can have
        pair = []
        is_odd = length % 2 #is_odd represent the possible middle digit contained in a odd length palindrome
        limit = length // 2 #we will simulate only one part of the palindrome because that's how the algorithm works
        total = 0
        for x in range(0, limit+1):
            if self.is_lucky(x*2) == 1 or self.is_lucky(x*2+is_odd) == 1 or \
            self.is_lucky(length-x*2) == 1 or self.is_lucky(length-x*2-is_odd) == 1:
                pair.append(x)
        return pair
    
    def get_possibilities(self, length): #determine how much possibility for a given length
        total = 0
        for i in self.pair:
            if i <= length:
                total += scipy.special.comb(length, i, exact=True) #exact=True return a int instead of a float
            else:
                break
        return total
    
    def get_lucky_from_index(self, index): #get lucky number from index. "4" is index 0, "7" is 1, "44" is 2 and so on
        binary = "{0:b}".format(index+2)   #I use binary numbers because 4 and 7 are like 0 and 1
        res = ""
        for idx, i in enumerate(binary[1:]):
            res += "4" if i == "0" else "7"
        return int(res)
    
    def exponential_search(self, length, target):
        idx = length-2 #start at end of array
        step = 1 #helps moving on the array 
        current = -1 #store current value
        best_idx = -1 #return idx
        best_val = 0 #return value
        over_it = False #once we've got over the target we will change the behavior of step
        
        while step > 0: #while we can move
            if over_it == True:
                step = step // 2 #need to reduce the steps to get precise

            current = self.get_possibilities(idx+1) #get the comb[idx] value
            if current <= target: # if true we update the best values because we're sure they are the current best
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
    
    def generate(self):
        self.space = self.limit
        self.solution = ["4"] * self.limit
        idx = 0
        remove = 1
        
        self.start_time_segment = time.time()
        while self.query > 0 and remove > 0:
            self.verbose_print(3)
            
            idx, remove = self.exponential_search(self.space, self.query)
            self.solution[idx] = "7"
            self.seven_amount += 1
            
            self.query -= remove
            self.space = idx
            for i in range(len(self.pair)): #update pair numbers
                self.pair[i] -= 1
            if self.pair[0] < 0: #delete because useless
                del self.pair[0]
        
        if self.query == 0:
            for i in range(self.pair[0]): #sometimes there is some remaining "7" to put
                self.solution[i] = "7"
                self.seven_amount += 1
        self.space = 0
        self.verbose_print(3)
        
        self.solution = "".join(self.solution)
    
    def get_solution(self, query): #let's go
        self.verbose_print(0)
        
        self.query = query
        index = 0
        while self.query > 0: #we need to know the length of the solution
            self.length = self.get_lucky_from_index(index) #we first get the length of out current lucky number
            self.pair = self.get_palindrome_pair(self.length) #we determine the pair numbers of the length
            self.limit = self.length // 2
            self.total = self.get_possibilities(self.limit) #we calculate how much possibilities exist
            self.query -= self.total #if query > 0 that means the solution is not in this length
            index += 1
            self.verbose_print(1)
        self.query += self.total - 1       #need to go back one step to know what is the real query
        
        self.reverse = False    #used to helps algorithm by a little bit
        if (self.query - self.total//2) > 0:
            self.query = self.total - self.query - 1
            self.reverse = True
        
        self.seven_amount = 0 #we assume that the solution is filled by 4 where some of 4s will be replaced by 7s
        self.verbose_print(2)
        
        self.generate() #everything
        
        if self.length%2 == 0: #we create the whole number from one side of it
            self.solution = self.solution[::-1] + self.solution
        else:                                        #and here we determine what is the value of the middle digit
            if self.is_lucky(self.seven_amount*2+1) == 1 or self.is_lucky((self.limit-self.seven_amount)*2) == 1:
                self.solution = self.solution[::-1] + "7" + self.solution
            else:
                self.solution = self.solution[::-1] + "4" + self.solution
        
        if self.reverse == True: #reverse the solution if needed
            self.solution = self.solution.replace("4","0")
            self.solution = self.solution.replace("7","4")
            self.solution = self.solution.replace("0","7")
        
        self.verbose_print(4)
        return self.solution
