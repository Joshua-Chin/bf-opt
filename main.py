from bf_parser import parse
from optimizer import optimize
string = '''++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]
>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.'''


if __name__=='__main__':
    from pprint import pprint
    while True:
        try:
            p=parse(input())
            x=optimize(p)
            pprint(x)
        except KeyboardInterrupt:
            break
