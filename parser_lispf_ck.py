import ox
import click
import re
from getch import getche

lexer = ox.make_lexer([
    ('NAME',r'[a-zA-Z]+'),
    ('NUMBER', r'\d+'),
    ('OPENING_PARENTHESES', r'\('),
    ('CLOSING_PARENTHESES', r'\)'),
])

tokens_list = ['NUMBER', 'NAME','OPENING_PARENTHESES','CLOSING_PARENTHESES','COMMA']

atom_number = lambda value: ('atom_number', float(value))

parser = ox.make_parser([
    ('simple_block : simple_block simple_term', lambda first, second: (first, second)),
    ('simple_block : simple_term', lambda simple_block: simple_block),
    ('simple_term : OPENING_PARENTHESES simple_term CLOSING_PARENTHESES', lambda opening_paretheses, term, closing_parentheses: (opening_paretheses, term, closing_parentheses)),
    ('simple_term : atom simple_term',lambda first_term, second_term : (first_term, second_term)),
    ('simple_term : atom COMMA simple_term',lambda atom, comma, simple_term : (atom, comma, simple_term)),
    ('simple_term : atom', lambda term: term),
    ('atom : OPENING_PARENTHESES atom CLOSING_PARENTHESES', lambda opening_paretheses, term, closing_parentheses: (opening_paretheses, term, closing_parentheses)),
    ('atom : NUMBER', atom_number),
    ('atom : NAME',lambda name : name),
], tokens_list)

def pretty_print(code_p):
    indent = 0

    for element in code_p:
        if(element.find('(') != -1):
            if(not indent):
                print(lexer(element))
                indent += 4
            else:
                print((' ' * indent) + str(lexer(element)))
                indent += 4
        elif(element == ")"):
            indent -= 4
            print((' ' * indent) + str(lexer(element)))
        elif(element.find(')') != -1):
            print((' ' * indent) + str(lexer(element)))
            indent -= 4
            open_parentheses = 0
        else:
            print((' ' * indent) + str(lexer(element)))

lisp_e = [0]
position = 0
code_position = 0

@click.command()
@click.argument('entry_file_name')

def read_file(entry_file_name):
    input_file = open(entry_file_name, 'r')

    args = []
    args_p = []
    code_p =[]

    for line in input_file:
        ind = line.find(';')

        if(ind != -1 or line.find('\n') != -1):
            line = line[:ind]

        args.append(line)

    for element in args:
        element_p = element.replace('    ', '')
        args_p.append(element_p)

    code = ' '.join(args_p)
    code = code.split()
    code = ' '.join(code)
    code_p = ' '.join(list(filter(None, re.split(r'(\(|\))', code)))).split()

    # pretty_print(code_p)

    code_p[0] = ''
    code_p[len(code_p) - 1] = ''
    code = ' '.join(code_p)
    code = eval(str(code.split()).replace("'(',", '[').replace("')'",']'))

    print(code)

    input_file.close()

read_file()
