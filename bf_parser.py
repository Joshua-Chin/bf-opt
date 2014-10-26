from bf_symbols import tape, reads, tape_index, read_index
from datatypes import assign, block, increment, loop

def parse(src):
    """Parses the source code into blocks"""
    tree = [[]]
    
    for char in src:
        if char == '[':
            l = []
            tree[-1].append(loop(l))
            tree[-1].append(block({tape[tape_index]: assign(0)}, tape_index, read_index, ()))
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
            tree[-1].append(block({tape[tape_index]: assign(reads[read_index])}, tape_index, read_index+1, ()))
    return tree[-1]
