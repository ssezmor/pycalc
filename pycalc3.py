'''pycalc'''
from operator import *
from builtins import *
from math import *
from inspect import signature

operators = {'+':(4, add), '-':(4, sub),
             '*':(3, mul), '/':(3, truediv),
             '^':(2, pow), '**':(2, pow),
             '//':(2, floordiv), '%':(2, divmod), 
             ',':(0, ), '(':(0, ), ')':(5, ),}

constants = {'e':e, 'pi':pi, 'tau':tau}

def calculate(input_string):
    input_list = convert_string_to_list(input_string)
    rpn_list = convert_list_to_rpn(input_list)
    answer = calculate_rpn(rpn_list)
    print('Result:', answer)

def convert_string_to_list(input_string):
    out = ['']
    for i in input_string.lower().replace(' ',''):
        if (i.isdigit() or i == '.') and isfloat(out[-1]):
            out[-1]=out[-1]+i
        elif i.isdigit() and out[-1] == '-' and (out[-2] in operators and out[-2] not in '()' or out[-2] == ''):
            out[-1]=out[-1]+i
        elif i.isalpha() and out[-1].isalpha():
            out[-1]=out[-1]+i
        elif i in '*/' and i == out[-1]:
            out[-1]=out[-1]+i
        else:
            out.append(i)
        print(out)
    return out

def convert_list_to_rpn(input_list):
    rpn = []
    stack = []
    for i in input_list[1:]:
        if i in operators:
            process_stack(stack, rpn, i)
        elif i in constants:
            rpn.append(constants[i])
        elif i.isdigit():
            rpn.append(int(i))
        elif isfloat(i):
            rpn.append(float(i))
        print(rpn, stack)
    rpn.extend(reversed(stack))
    print(rpn)
    return rpn

def calculate_rpn(rpn_list):
    stack = []
    for i in rpn_list:
        if i == ',':
            stack.append(i)
        elif i in operators:
            calculate_operator(operators[i], stack)
        else:
            stack.append(i)
        print(rpn_list, stack)
    return stack[0]

def process_stack(stack, rpn, i):
    for j in reversed(stack):
        if get_priority(i) >= get_priority(j):
            last_el = stack.pop()
            if j == '(':
                break
            rpn.append(last_el)
    if i != ')':
        stack.append(i)

def calculate_operator(operator_params, stack):
    params_count = len(signature(operator_params[1]).parameters)
    if params_count == 1:
        x = stack.pop()
        result = operator_params[1](x)
        stack.append(result)
    elif params_count == 2:
        y, x = stack.pop(), stack.pop()
        result = operator_params[1](x, y)
        stack.append(result)

def isfloat(ex):
    return ex.lstrip('-').replace('.','',1).isdigit()

def get_priority(operator):
    return operators[operator][0]

user_expression = input('Please input expression ')
calculate(user_expression)