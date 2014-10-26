from datatypes import block, increment, assign, loop
from bf_symbols import tape,tape_index, read_index

def optimize(ir):
    opt_ir = optimize_pass(ir)
    while opt_ir != ir:
        print('pass complete')
        opt_ir, ir = optimize_pass(opt_ir), opt_ir
    return opt_ir

def optimize_pass(ir):
    return dead_loop_elimination(flatten_assign_0_loop(flatten_no_shift_loop(constant_fold(ir))))

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
            if current is not None:
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
            elem = flatten_no_shift_loop(elem.blocks)
            if len(elem) == 1 and isinstance(elem[0], block) \
               and elem[0].shift == tape_index \
               and elem[0].reads == read_index \
               and not elem[0].writes:
                blk = elem[0]
                step = blk.computations[tape[tape_index]]
                if isinstance(step, increment):
                    step = step.expr
                    mult = tape[tape_index]/-step
                    new_computations = {}
                    for index, compute in blk.computations.items():
                        if index == tape[tape_index]:
                            continue
                        new_computations[index] = compute.repeat(mult)
                    out.append(block(new_computations, tape_index, read_index, ()))
                else:
                    out.append(loop(elem))
            else:
                out.append(loop(elem))
        else:
            out.append(elem)
    return out

def flatten_assign_0_loop(ir):
    """Flattens loops which assign their index to 0"""
    out = []
    for elem in ir:
        if isinstance(elem, loop):
            elem = flatten_assign_0_loop(elem.blocks)
            if len(elem) > 0:
                blk = elem[-1]
                end = blk.shift
                if blk.computations.get(tape[end]) == assign(0):
                    out += elem
                else:
                    out.append(loop(elem))
            #else infinite loop
        else:
            out.append(elem)
    return out

def dead_loop_elimination(ir):
    """Removes loops when their index is preset to 0"""
    out = []
    prev = None
    for elem in ir:
        if isinstance(elem, loop):
            if prev is not None and prev.computations.get(tape[prev.shift]) == assign(0):
                continue
        out.append(elem)
        prev = elem
    return out
            

def unroll_loop(ir):
    """Attempts to prove which elements are positive, in order to convert loops into direct jump"""
    out = []
    prev = None
    for elem in ir:
        if isinstance(elem, loop):
            elem = unroll_loop(elem)
            if len(elem) == 1 and isinstance(elem[0], block) \
               and not elem[0].computations \ #Improve latter
               and elem[0].reads == read_index \
               and not elem[0].writes \
               and prev is not None:
                blk = elem[0]
                step = blk.shift-tape_index
                start = prev.shift
                continue
        out.append(elem)

