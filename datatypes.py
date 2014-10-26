from sympy import Expr, IndexedBase, decorators

from bf_symbols import tape, tape_index, read_index

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
        return self.expr+other

    def repeat(self, count):
        return self

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
        return self.expr+other

    def repeat(self, count):
        return increment(self.expr*count)

    def __eq__(self, value):
        return isinstance(value, increment) and value.expr == self.expr
    
    def __repr__(self):
        return 'increment('+str(self.expr)+')'

class loop:

    def __init__(self, blocks):
        self.blocks = blocks

    def __eq__(self, value):
        return isinstance(value, loop) and self.blocks == value.blocks

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
            temp_tape = IndexedBase('temp_tape')
            new_computations = {}
            subs0 = [(tape_index, self.shift), (read_index, self.reads)]
            subs = []
            for index, compute in self.computations.items():
                compute = compute.subs(tape, temp_tape)
                if isinstance(compute, assign):
                    subs.append((index, compute.expr))
                else:
                    subs.append((index, compute.expr+index))
                    
            for index, compute in value.computations.items():
                new_compute = compute.subs(subs0).subs(subs).subs(temp_tape, tape)
                new_computations[index.subs(subs0)] = new_compute
                
            for index, compute in self.computations.items():
                if index not in new_computations:
                    new_computations[index] = compute
                else:
                    new_computations[index] = compute + new_computations[index] #adding not communitive
                    
            new_shift = self.shift + value.shift - tape_index
            new_reads = self.reads + value.reads - read_index
            new_writes = self.writes + tuple(w.subs(subs0).subs(subs).subs(temp_tape, tape) for w in value.writes)
            return block(new_computations, new_shift, new_reads, new_writes)
        return NotImplemented

    def __eq__(self, value):
        return isinstance(value, block) and \
               self.computations == value.computations and \
               self.shift == value.shift and \
               self.reads == value.reads and \
               self.writes == value.writes

    def __repr__(self):
        return 'block' + ", ".join(str(x) for x in [self.computations, self.shift, self.reads, self.writes])+')'
