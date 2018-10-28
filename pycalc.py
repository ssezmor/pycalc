#!/usr/bin/python

'''description'''
import builtins
import operator
import math

operators = {'log':(11, 2, math.log),
            'log1p':(11, 1, math.log1p),'log2':(11, 1, math.log2),
            'abs':(11, 1, builtins.abs),'round':(11, 2, builtins.round),
            '^':(11, 2, operator.pow),'**':(11, 2, builtins.pow),
            '//':(11, 2, operator.floordiv),'%':(11, 2, operator.mod),
            'sin':(11, 1, math.sin),'cos':(11, 1, math.cos),
            'tan':(11, 1, math.tan),'atan':(11, 1, math.atan),
            '+':(9, 2, operator.add),'-':(9, 2, operator.sub),
            '*':(10, 2, operator.mul),'/':(10, 2, operator.truediv),
             '(':(0, ''),')':(0, '')}

function_for_extend = {'round':builtins.round, 'log':math.log}

constants = {'pi':math.pi, 'e':math.e, 'tau':math.tau}

def calc(input_string):
    input_list = convert_to_list(input_string)
    if error_checker(input_list):
        input_func()
        return
    rpn_list = convert_rpn(input_list)
    calculate_rpn(rpn_list)
    #print(string_RPN)

def convert_rpn(input_list):
    '''Convert string to reverse polish notation'''

    output_list = []
    stack = []
    number = ''
    for i in input_list:
        if i == '(':
            last_el = get_last_element(stack)
            stack.append(i)
        elif i == ')':
            for j in reversed(stack):
                last_oper = stack.pop()
                if j == '(':
                    break
                output_list.append(last_oper)
        elif i in operators:
            prior = operators[i][0]
            last_el = get_last_element(stack)
            if last_el == [] or last_el == '(':
                stack.append(i)
            elif prior<=operators[last_el][0]:
                last_oper = stack.pop()
                output_list.append(last_oper)
                stack.append(i)
            elif prior>=operators[last_el][0]:
                stack.append(i)
        elif i == ',':
            last_el = get_last_element(stack)
            if last_el not in '()':
                last_oper = stack.pop()
                output_list.append(last_oper)
        else:
            output_list.append(i)
        print(output_list, stack)
    output_list.extend(reversed(stack))
    print(output_list)
    return output_list

def calculate_rpn(rpn_list):
    stack = []
    for i in rpn_list:
        if i in operators:
            oper_params = operators[i]
            if oper_params[1] == 1:
                x = stack.pop()
                result = calculate(oper_params[2], x)
                stack.append(result)
            elif oper_params[1] == 2:
                x, y = stack.pop(), stack.pop()
                result = calculate(oper_params[2], x, y)
                stack.append(result)
        else:
            stack.append(i)
        print(rpn_list, stack)
    return stack.pop()

def calculate(function, x = '0' , y = '0'):
    if function in function_for_extend.values():
        if x == '0':
            return str(function(float(y)))
        else:
            return str(function(float(y),int(x)))
    elif y == '0':
        if x.isdigit():
            return str(function(int(x)))
        else:
            return str(function(float(x)))
    else:
        if x.isdigit() and y.isdigit():
            return str(function(int(y),int(x)))
        else:
            return str(function(float(y),float(x)))

def convert_to_list(input_string):
    output_list = []
    number = ''
    command_name = ''
    for i,v in enumerate(input_string):
        if v in '1234567890.':
            if command_name == '':
                number +=v
            else:
                command_name +=v
        elif number:
            output_list.append(number)
            number = ''
        if v in ',':
            output_list.append(v)
        if v.lower() in 'abcdefghijklmnopqrstuvwxyz=><!':
            command_name += v.lower()
        if v in operators:
            if v == '-':
                prev_el = get_previous_element(input_string, i)
                if prev_el in operators or prev_el == 0:
                    number += v
                else:
                    output_list.append(v)
            elif v == '/' or v == '*':
                next_el = get_next_element(input_string, i)
                prev_el = get_previous_element(input_string, i)
                if prev_el == v:
                    continue
                if next_el == v:
                    output_list.append(2*v)
                else:
                    output_list.append(v)
            else:
                output_list.append(v)
        elif command_name in operators:
            next_el = get_next_element(input_string, i)
            if next_el == '(':
                output_list.append(command_name)
                command_name = ''
        elif command_name in constants:
            output_list.append(str(constants[command_name]))
            command_name = ''
    if number:
        output_list.append(number)
    extend_func(output_list)
    print(output_list)
    return output_list

def extend_func(input_list):
    comma_count = 0
    round_find = False
    j = None
    for f in function_for_extend:
        for i,v in enumerate(input_list):
            print(i,v)
            if v in f and not round_find:
                round_find = True
                continue
            elif v in f and round_find:
                #print('(in)', i, input_list[i:])
                j = extend_func(input_list[i:])
                input_list.insert(i + j,'0')
                input_list.insert(i + j,',')
                j = j + i + 2
                print(j)
            if round_find:
                if v == '(':
                    continue
                elif v == ')':
                    print(v, i, j, comma_count)
                    if comma_count == 0 and j == None:
                        return i
                    elif comma_count == 0 and j != None:
                        if i > j:
                            input_list.insert(i,'0')
                            input_list.insert(i,',')
                            comma_count = 0
                            round_find = False
                        return i
                    else:
                        return i
                elif v == ',':
                    if j == None:
                        comma_count +=1
                    elif i > j:
                        comma_count +=1

def get_last_element(user_list):
    if user_list == []:
        return []
    else:
        return user_list[-1]

def get_previous_element(string, pos):
    if pos == 0:
        return 0
    else:
        prev_el = ' '
        n = 1
        while prev_el == ' ':
            prev_el = string[pos - n]
            n += 1
            if prev_el != ' ':
                break
        return prev_el

def get_next_element(string, pos):
    if pos == 0:
        return 0
    else:
        next_el = ' '
        n = 1
        while next_el == ' ':
            next_el = string[pos + n]
            n += 1
            if next_el != ' ':
                break
        return next_el

def error_checker(input_list):
    if input_list == []:
        print('ERROR: entered expression is empty')
        return 1
    if brackets_count(input_list): 
        return 1
    if number_checker(input_list):
        return 1
    return 0

def brackets_count(input_list):
    counter = 0
    for i in input_list:
        if i == '(':
            counter +=1
        elif i == ')':
            counter -=1
    if counter != 0:
        print('ERROR: brackets are not balanced')
        return 1
    return 0

def number_checker(input_list):
    for i in input_list:
        if i.count('.', 0, len(i)) > 1:
            print('ERROR: incorrect number', i)
            return 1
    return 0

def input_func():
    return input('Please enter expression: ')

calc(input_func())
