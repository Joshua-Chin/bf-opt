from bf_parser import parse
from optimizer import optimize, optimize_pass
from datatypes import loop
string = '''++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]
>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.'''



def to_pprint_format(ir):
    out = []
    for elem in ir:
        if isinstance(elem, loop):
            out.append(to_pprint_format(elem.blocks))
        else:
            out.append(elem)
    return out

def po(x):
    p=parse(x)
    return optimize(p)    

if __name__=='__main__':
    from pprint import pprint
    try:
        f=open('mandelbrot.bf')
        p=parse(string)
        x=optimize(p)
        pprint(to_pprint_format(x))
    except KeyboardInterrupt:
        pass
