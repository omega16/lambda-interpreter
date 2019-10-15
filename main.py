#! /usr/bin/env python3

from lark import Lark,Token,Tree

from lark import Transformer




class Variable:
    def __init__(self,value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Function:
    def __init__(self,variable,term):
        self.variable = variable
        self.term = term

    def __str__(self):
        return "Function \n var: {} \n term: {}\n".format(
            str(self.variable).replace("\n","\n"+4*" "),
            str(self.term).replace("\n","\n"+4*" ")
        )

class Application:
    def __init__(self,term1, term2):
        self.term1 = term1
        self.term2 = term2

    def __str__(self):
        return "Application \n term1: {} \n term2: {}\n".format(
            str(self.term1).replace("\n","\n"+4*" "),
            str(self.term2).replace("\n","\n"+4*" ")
        )

def unsugar_function(variables,items):
    if len(variables) == 1:
        return Function(variables[0],items)
    return Function(variables[0],unsugar_function(variables[1:],items))

def unsugar_terms(terms):
    if len(terms) == 1:
        return terms[0]

    if len(terms) == 2:
        return Application(*terms)
    last = terms.pop()
    return Application(unsugar_terms(terms),last)



def substitution(exp,var,value):
    # print("substitution \n    exp : {} \n    var : {} \n    value : {}\n".format(
    #     str(exp).replace("\n","\n"+8*" "),
    #     str(var).replace("\n","\n"+8*" "),
    #     str(value).replace("\n","\n"+8*" ")
    #     ))

    if isinstance(exp,Variable) :
        # print("checando ",exp,var)
        if exp.value == var.value :
            # print("match")
            return value
        return exp
    if isinstance(exp,Application):
        return Application(substitution(exp.term1,var,value) , substitution(exp.term2,var,value) )
    if isinstance(exp,Function) :
        if exp.variable.value == var.value:
            return substitution(exp.term,var,value)
        return Function(exp.variable,substitution(exp.term,var,value))
    # if isinstance(exp,Term):
    #     return substitution(exp.value,var,value)
    
def print_lambda(exp):
    s = lambda2str(exp)
    print(s)
    ident=0
    out=[]
    for i in s:
        if i=="(":
            out.append("\n")
            out.append(ident*" ")
            out.append(i)
            ident+=1
            continue
        elif i==")":
            ident-=1
            out.append(i)
            out.append("\n")
            out.append(ident*" ")
            continue
        out.append(i)
    print("".join(out))

def lambda2str(exp):
    if isinstance(exp,Variable):
        return " {} ".format(exp.value)
    if isinstance(exp,Function):
        variables = []
        func=exp
        while(isinstance(func,Function)):
            variables.append(lambda2str(func.variable))
            func = func.term
        if isinstance(func,Application):
            return "{{\\{}.{}{}}}".format("".join(variables),lambda2str(func.term1),lambda2str(func.term2))
        return "{{\\{}.{}}}".format("".join(variables),lambda2str(func))
    if isinstance(exp,Application):
        return "({}{})".format(lambda2str(exp.term1),lambda2str(exp.term2))

exp_count=0

def show_expression(exp,count=None):
    if count is None:
        global exp_count
        count = exp_count
        exp_count+=1
    print("({})  .  .  .  {}".format(count,lambda2str(exp)))

def show_replace(right,count=None):
    if count is None:
        global exp_count
        count = exp_coun
    if right:
        print("replace in {} right ".format(count))
        return
    print("replace in {} left ".format(count))

def reduction(app):
    global exp_count 
    local_exp_count=exp_count
    show_expression(app)
    if isinstance(app,Application):
        if isinstance(app.term1,Function):
            return reduction(substitution(app.term1,app.term1.variable,app.term2))
        if isinstance(app.term1,Variable):
            if isinstance(app.term2,Variable):
                return app
            left = reduction(app.term2)
            show_replace(False,local_exp_count)
            return Application(app.term1,left)
        right = reduction(app.term1)
        show_replace(True,local_exp_count)
        return reduction(Application(right,app.term2))
    return app

class LambdaTransform(Transformer):
    def variable(self,items):
        return Variable(items[0])

    def variables(self,items):
        return items

    def terms(self,items):
        return unsugar_terms(items)

    def term(self,items):
        return items[0]

    def function(self,items):
        # print(items)
        return unsugar_function(items[1],items[2])

    def application(self,items):
        return Application(items[0],items[1])

    def outermost_sugar(self,items):
        # print(items)
        if len(items) == 1:
            return items[0]
        if len(items) == 3:
            return unsugar_function(items[1],items[2])
        return items

    def program(self,items):
        return [items[i] for i in range(0,len(items),2)]
        
        


grammar =r"""

    EOE : ";"

    LAMBDA : "\\"

    variable : /[a-z][a-zA-Z_0-9]*/

    term : variable     
        | function
        | application

    variables : variable+

    terms : term+

    function : "(" LAMBDA variables "." terms ")" 
        | "{" LAMBDA variables "." terms "}"

    application : "(" term terms ")" | "{" term terms "}"


    outermost_sugar : LAMBDA variables "." terms
        | terms

    program : ( outermost_sugar EOE)*

    %import common.WS
    %ignore WS

 """

parser = Lark(grammar,start='program')

def evaluate_exp(exp):
    # print(str(func))
    # print(lambda2str(exp))
    # print_lambda(exp)
    if isinstance(exp,Function):
        return exp
    if isinstance(exp,Application):
        return reduction(exp)


def evaluate_program(expressions):
    out = []
    for exp in expressions:
        out.append( evaluate_exp(exp) )
    return out

def test_parser(name):
    tree = parser.parse(open(name,"r").read())
    # print(tree.pretty())
    program = LambdaTransform().transform(tree)
    for exp,result in zip(program,evaluate_program(program)):
        print("input : {} \noutput: {} ".format(lambda2str(exp),lambda2str(result)))


lines=[]
def interprete(line):
    global lines
    for i in line : 
        if i!= ";":
            lines.append(i)
        else :
            lines.append(";")
            real_line = "".join(lines)
            lines=[]
            tree = parser.parse(real_line)
            program = LambdaTransform().transform(tree)
            for result in evaluate_program(program):
                print("-> {} ".format(lambda2str(result)))

if __name__ == '__main__':
    import sys
    if len(sys.argv)>1:
        test_parser(sys.argv[1])
    else : 
        while(True):
            line = input("Yuki.N> ")
            interprete(line)
