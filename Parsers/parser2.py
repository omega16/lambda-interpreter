#! /usr/bin/env python3

from lark import Lark,Token,Tree

from lark import Transformer

class StringTransformer(Transformer):
    def variable(self,items):
        return " {} ".format(items[0].value)

    def expression(self,items):
        return items[0] 

    def abstraction(self,items):
        variables = "".join(items[:-1]) 
        expression = items[-1]
        return "(\\{}. {})".format(variables,expression)

    def application(self,items):
        left = items[0]
        right = " ".join(items[1:])
        return "({} {})".format(left,right)

    def sugar_start(self,items):
        if len(items)==1:
            return items[0]
        variables = "".join(items[:-1]) 
        expression = items[-1]
        return "\\{}. {}".format(variables,expression)



grammar =r"""
    variable : /[^()\n\s\.\\0-9][^()\n\s\.\\]*/

    expression : variable 
        | abstraction
        | application

    abstraction : "(" "\\" variable+ "." expression ")"

    application : "(" expression expression+ ")" 
        | expression expression+ 


    sugar_start : "\\" variable+ "." expression 
        | expression

    %import common.WS
    %ignore WS

 """

parser = Lark(grammar,start='sugar_start')


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
    print(StringTransformer().transform(tree))

    


def interpreter():
    while(True):
        try :
            line = input("Lambda >> ")
        except (EOFError,KeyboardInterrupt) :
            print("\nLambda session end")
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