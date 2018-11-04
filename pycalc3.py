'''pycalc'''
from operator import *
from builtins import *
from math import *
from inspect import signature

operators = {'+':(4, add), '-':(4, sub),
             '*':(3, mul), '/':(3, truediv),
             '^':(2, pow), '**':(2, pow),
             '//':(2, floordiv), '%':(2, divmod), 
             '(':(0, ), ')':(5, ), ',':(0, )}

constants = {'e':e, 'pi':pi, 'tau':tau}

def calculate(input_string):
    out = ['']
    for i in input_string.lower().replace(' ',''):
        if i.isdigit() and isfloat(out[-1]):
            out[-1]=out[-1]+i
        elif i == '.' and out[-1].lstrip('-').isdigit():
            out[-1]=out[-1]+i
        elif i.isalpha() and out[-1].isalpha():
            out[-1]=out[-1]+i
        elif i == out[-1] and i in ['*', '/']:
            out[-1]=out[-1]+i
        elif i == '-' and out[-1] in operators:
            out.extend(['-1', '*'])
        else:
            out.append(i)
        print(out)

    rpn = []
    stack = []
    for i in out[1:]:
        if i in operators:
            for j in reversed(stack):
                if get_priority(i) > get_priority(j):
                    last_el = stack.pop()
                    if j == '(':
                        break
                    rpn.append(last_el)
            if i != ')':
                stack.append(i)
        elif i in constants:
            rpn.append(constants[i])
        else:
            if i.isdigit():
                rpn.append(int(i))
            else:
                rpn.append(float(i))
        print(rpn, stack)
    rpn.extend(reversed(stack))
    print(rpn)

    stack = []
    for i in rpn:
        if i == ',':
            stack.append(i)
        elif i in operators:
            oper_params = operators[i]
            params_count = len(signature(oper_params[1]).parameters)
            if params_count == 1:
                x = stack.pop()
                result = oper_params[1](x)
                stack.append(result)
            elif params_count == 2:
                y, x = stack.pop(), stack.pop()
                result = oper_params[1](x, y)
                stack.append(result)
        else:
            stack.append(i)
        print(rpn, stack)
    print(stack)

def isfloat(ex):
    return ex.lstrip('-').replace('.','',1).isdigit()

def get_priority(operator):
    return operators[operator][0]

user_expression = input('Please input expression ')
calculate(user_expression)