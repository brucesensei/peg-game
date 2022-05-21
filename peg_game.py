# peg_game

# Conditions: you have 3 pegs labeled left to right a, b, c and n number of rings with decreasing diameters.
# All rings are stacked on peg 'a' with the largest ring on the bottom decreading in size to the smallest ring on top.
# Rings are modeled as numbers with the numbers representing size and pegs are modeled as lists containing the numbers.

# The objective is to move all rings from peg 'a' to peg 'c' one at a time, so the stack at 'c' is identical to the start. 
# At no time can a larger ring be placed on top of a smaller ring.
# After playing with this for more time than is reasonably healthy I discovered a few things.

# 1. The top three rings perform an unwinding pattern of 7 moves in order to expose the rings beneath for movement.
# 2. If ring number is odd, the top three rings must move to peg c on the first move and with each unwinding pattern,
#    the top three move in reverse from c -> b -> a -> ...
# 3. If the ring number is even, the top three rings must move to peg b on the first move and with each unwinding pattern,
#    the top three move forward from b -> c -> a -> ...
# 4. With the addition of one ring, the number of moves to complete the task doubles + 1 to move the exposed piece.
#    1 ring = 1 move, 2 rings = 3 moves, 3 rings = 7 moves ...

# With a little more thought, there is certainly an algorithm that could handle this more elegantly but for the moment
# it eludes me. Any suggestions would be appreciated. 

class PegGame:

    def __init__(self, number):
        self.pattern_dict = {
            'one': [['a','c']],
            'two': [['a','b'],['a','c'],['b','c']],
            'fwd0': [['a','b'],['a','c'],['b','c'],['a','b'],['c','a'],['c','b'],['a','b']],
            'fwd1': [['b','c'],['b','a'],['c','a'],['b','c'],['a','b'],['a','c'],['b','c']],
            'fwd2': [['c','a'],['c','b'],['a','b'],['c','a'],['b','c'],['b','a'],['c','a']],
            'rev0': [['a','c'],['a','b'],['c','b'],['a','c'],['b','a'],['b','c'],['a','c']],
            'rev1': [['b','a'],['b','c'],['a','c'],['b','a'],['c','b'],['c','a'],['b','a']],
            'rev2': [['c','b'],['c','a'],['b','a'],['c','b'],['a','c'],['a','b'],['c','b']],
            }  # the dictionary of unwinding patterns
        self.patterns = []  # The unwinding pattern based on ring number
        self.number = number  # The number of rings
        self.piece = 0  # The number of the ring currently in play
        self.counter = 0  # The number of iterations the game makes
        li = [i for i in range(1, self.number + 1)]
        li.reverse()
        self.start_list = li  # The initial list used to compare against the final peg to verify completion
        self.pegs = self.create_pegs()  # the pegs dictionary. Keys are abc, values are lists continaing ring numbers 
        self.a = self.pegs['a']
        self.b = self.pegs['b']  # a way to conviently access the values
        self.c = self.pegs['c']

    def create_pegs(self):
        '''Creates the peg dictionary based on the number of rings.'''
        li = [i for i in range(1, self.number + 1)]
        li.reverse()
        pegs = dict(
            a = li,
            b = [],
            c = [],
            )
        return pegs

    def run_pattern(self):
        '''Uses the pattern from the pattern dictionary to move the rings from one peg to the others.'''
        for pattern in self.patterns:
            self.piece = self.pegs[pattern[0]].pop()
            self.pegs[pattern[1]].append(self.piece)
            self.advance_count()
            print(f'{pattern[0]} -> {pattern[1]}')
            print(self.pegs)
            


    def get_cycles(self):
        '''Based on ring number, returns the number of cycles to run the for loop in the main game. '''
        if self.number < 4:
            cycles = 1
        elif self.number == 4:
            cycles = 2
        else:
            cycles = 2 ** (self.number - 3)
        return cycles
    

    def get_patterns(self):
        '''If ring number is one or two, returns those patterns, if three or more, it constructs the
           a string for the pattern dictionary key and retrieves the pattern.
           find_one is literally finding number 1 so it knows which peg pattern to choose. '''
        if self.number == 1:
            self.patterns = self.pattern_dict.get('one')
        elif self.number == 2:
            self.patterns = self.pattern_dict.get('two')
        else:
            pattern_string = ''
            if self.number % 2 == 0:
                pattern_string += 'fwd'
            else:
                pattern_string += 'rev'
            find_one = (1 in self.a, 1 in self.b, 1 in self.c)
            start_point = str(find_one.index(True))
            pattern_string += start_point
            self.patterns = self.pattern_dict.get(pattern_string)
        return self.patterns
    
    def report(self):
        '''Informs the user of the number of iterations. '''
        n = 1
        for i in range(self.number - 1):
            n = n + n
        n = n + (n-1)
        print(f'Rings should be sorted in {n} iterations.')

    
        
    def flip_condition(self):
        '''Determines where the exposed piece is and moves it to the correct peg.
            if a list is empty, number +1 is appended to facilitate comparison.
            the dictionary is sorted by value and the letter keys are returned as a list.
            list index is used to access keys in the peg dicitonary.
            number +1 is removed after operations as it seems to remain otherwise. '''
        def by_value(item):
            return item[1]
        clone_pegs = self.pegs.copy()
        for k in clone_pegs:
            if clone_pegs[k] == []:
                clone_pegs[k].append(self.number + 1)
        clone_pegs_head = {k:clone_pegs[k][-1] for k in clone_pegs}
        sorted_pegs = {k:v for k,v in sorted(clone_pegs_head.items(), key=by_value, reverse=True)}
        li = list(sorted_pegs)
        for k in clone_pegs:
            if self.number + 1 in clone_pegs[k]:
                clone_pegs[k].remove(self.number + 1)
        self.piece = self.pegs[li[1]].pop()
        self.pegs[li[0]].append(self.piece)
        self.advance_count()
        print(f'{li[1]} -> {li[0]}')
        print(self.pegs)
           
               
    def solved(self):
        '''Compares the start list with peg c to confirm if the game is complete. '''
        if self.c == self.start_list:
            print('Iteration Complete')
            return True
        return False

    def advance_count(self):
        '''Counts and reports the number of each iteration. '''
        self.counter += 1
        print(f'Current Count: {self.counter}  ', end='')



def main():   
    user_input = int(input('Enter the number of rings: '))
    p = PegGame(user_input)
    p.report()
    p.get_patterns()
    cycles = p.get_cycles()
    for cycle in range(cycles):
        p.run_pattern()
        if p.solved():
            break
        p.flip_condition()
        p.get_patterns()

if __name__ == '__main__':
    main()
