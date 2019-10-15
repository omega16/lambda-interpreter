#! /usr/bin/env python3

from lark import Lark


grammar =r"""
    variable : /[^()\n\s\.0-9][^()\n\s\.]*/

    expression : variable     
        | abstraction
        | application

    abstraction : "(" "\\" variable "." expression ")" 

    application : "(" expression expression ")" 

    %import common.WS
    %ignore WS

 """

parser = Lark(grammar,start='expression')


def parse_file(path):
    with open(path,"r") as source_file:
        source = source_file.read()
    return parser.parse(source)

def parse_string(source):
    return parser.parse(source)


def test_file(path):
    tree = parse_file(path)
    print(tree.pretty())

def test_string(source):
    tree = parse_string(source)
    print(tree.pretty())


def interpreter():
    while(True):
        try :
            line = input("Lambda >> ")
        except (EOFError,KeyboardInterrupt) :
            break
        print("-> \n",end="")
        test_string(line)


if __name__ == '__main__':
    import sys 
    if (len(sys.argv)>1):
        for path in sys.argv[1:]:
            test_file(path)
    else :
        interpreter()