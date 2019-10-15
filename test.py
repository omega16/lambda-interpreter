#! /usr/bin/env python3

from main import parser

from pathlib import Path

def test_folder(path,test_function):
    if isinstance(path,str):
        path = Path(path)
    if not isinstance(path,Path):
        raise Exception("expected Path class on test_folder")
    test_iterator(path.glob("*.lambda"),test_function)

def test_iterator(iterator,test_function):
    for rute in iterator:
        print(80*"~","\n\nTesting file : {}".format(str(rute)) )
        try:
            test_function(rute)
        except : 
            print("Parsing error")
            return False
        print("sucess")
        print("\n",80*"~")
    return True


def test_parsing():
    print("Test for parsing")
    test_folder("test/Parser", test_file_parse)

def test_file_parse(path):
    with open(path,"r") as program :
        tree = myl_parser.parse(program.read())
        # compare = str(tree.pretty())
        # print(compare)
    
if __name__ == '__main__':
    import sys
    if len(sys.argv)>1:
        test_iterator(sys.argv[1:],test_file_parse)
    else :
        test_parsing()