from enum import Enum
from sympy import symbols, IndexedBase, Sum, pprint, Expr, decorators

#Separate assignment and increment
#Create general block class and loop clas, supporting add
class assign(Expr):

    def __init__(self, expr):
        self.expr = expr

    @decorators._sympifyit('other', NotImplemented)
    @decorators.call_highest_priority('__radd__')
    def __add__(self, other):
        if isinstance(other, assign):
            return other
        if isinstance(other, increment):
            return assign(self.expr+other.expr)
        return NotImplemented

    def __eq__(self, value):
        return isinstance(value, assign) and value.expr == self.expr
    
    def __repr__(self):
        return 'assign('+str(self.expr)+')'

class increment(Expr):

    def __init__(self, expr):
        self.expr = expr

    @decorators._sympifyit('other', NotImplemented)
    @decorators.call_highest_priority('__radd__')
    def __add__(self, other):
        if isinstance(other, assign):
            return other
        if isinstance(other, increment):
            return increment(self.expr+other.expr)
        return NotImplemented

    def __eq__(self, value):
        return isinstance(value, increment) and value.expr == self.expr
    
    def __repr__(self):
        return 'increment('+str(self.expr)+')'

class loop:

    def __init__(self, blocks):
        self.blocks = blocks

    def __repr__(self):
        return 'loop('+str(self.blocks)+')'

class block:

    def __init__(self, computations, shift, reads, writes):
        self.computations = computations
        self.shift = shift
        self.reads = reads
        self.writes = writes

    def __add__(self, value):
        if isinstance(value, block):
            raise NotImplementedError()
        return NotImplemented

    def __repr__(self):
        return 'block' + ", ".join(str(x) for x in [self.computations, self.shift, self.reads, self.writes])+')'

tape = IndexedBase('tape')
tape_index = symbols('tape_index')

reads = IndexedBase('reads')
read_index = symbols('read_index')

def parse(src):
    """Parses the source code into blocks"""
    tree = [[]]
    
    for char in src:
        if char == '[':
            l = []
            tree[-1].append(loop(l))
            tree.append(l)
        elif char == ']':
            tree.pop()
            
        elif char == '+':
            tree[-1].append(block({tape[tape_index]: increment(1)}, tape_index, read_index, ()))
        elif char == '-':
            tree[-1].append(block({tape[tape_index]: increment(-1)}, tape_index, read_index, ()))
        elif char == '>':
            tree[-1].append(block({}, tape_index+1, read_index, ()))
        elif char == '<':
            tree[-1].append(block({}, tape_index-1, read_index, ()))
        elif char == '.':
            tree[-1].append(block({}, tape_index, read_index, (tape[tape_index],)))
        elif char == ',':
            tree[-1].append(block({tape[tape_index]: reads[read_index]}, tape_index, read_index+1, ()))
    return tree[-1]

if __name__=='__main__':
    import pprint
    pprint.pprint(parse('++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.'))
