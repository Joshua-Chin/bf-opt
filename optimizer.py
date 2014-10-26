from datatypes import block, loop
from bf_symbols import tape_index

def optimize(ir):
    return flatten_no_shift_loop(constant_fold(ir))

def constant_fold(ir):
    out = []
    current = None
    for elem in ir:
        if isinstance(elem, block):
            if current is None:
                current = elem
            else:
                current = current + elem
        else:
            out.append(current)
            current = None
            out.append(loop(constant_fold(elem.blocks)))
    else:
        if current is not None:
            out.append(current)
    return out

def flatten_no_shift_loop(ir):
    out = []
    for elem in ir:
        if isinstance(elem, loop):
            elem = flatten_no_shift_loop(elem)
            if len(elem) == 1 and isinstance(elem[0], block) and elem[0].shift == tape_index:
                blk = elem[0]
                step = blk.computations[tape[tape_index]]
                mult = tape[tape_index]
        else:
            out.append(elem)
    return out

def flatten_assign_0_loop(ir):
    """Flattens loops which assign their index to 0"""

def unroll_loop(ir):
    """Attempts to prove which elements are positive, in order to convert into direct jump"""
