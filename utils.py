'''
Provices the common processes nerdle would typically supply.
'''

import numpy as np
import pickle

valid_nerdle_characters = "0123456789+-*/="
valid_nerdle_equation_characters = "0123456789+-*/"
valid_nerdle_numbers = "0123456789"
valid_nerdle_functions = "+-*/"

def check_validity(guess: str):
    '''
    Checks if an equation is a valid nerdle equation.
    '''
    if not len(guess) == 8:
        return False
    if not guess.count("=") == 1:
        return False
    for char in guess:
        if not char in valid_nerdle_characters:
            return False
    if guess[0] == "=" or guess[-1] == "=":
        return False
    split_equation = guess.split("=")
    left_side_solution = string_equation_solver(split_equation[0])
    right_side_solution = string_equation_solver(split_equation[1])
    if not left_side_solution or not right_side_solution or left_side_solution != right_side_solution:
        return False
    return True

def string_equation_solver(equation: str):
    '''
    Solves an equation given as a string.  Returns None if invalid equation.
    '''
    if equation[0] in valid_nerdle_functions or equation[-1] in valid_nerdle_functions:
        return None

    #Addition and Subtraction Pass
    for idx, char in enumerate(equation):
        if char == "+":
            right_side = equation[idx+1:]
            if "+" in right_side or "-" in right_side:
                continue
            left_side = string_equation_solver(equation[0:idx])
            right_side = string_equation_solver(right_side)
            if left_side is not None and right_side is not None:
                return left_side+right_side
            else:
                return None
        elif char == "-":
            right_side = equation[idx+1:]
            if "+" in right_side or "-" in right_side:
                continue
            left_side = string_equation_solver(equation[0:idx])
            right_side = string_equation_solver(right_side)
            if left_side is not None and right_side is not None:
                return left_side-right_side
            else:
                return None

    #Multiplication and Division Pass
    for idx, char in enumerate(equation):
        if char == "*":
            right_side = equation[idx+1:]
            if "*" in right_side or "/" in right_side:
                continue
            left_side = string_equation_solver(equation[0:idx])
            right_side = string_equation_solver(right_side)
            if left_side is not None and right_side is not None:
                return left_side*right_side
            else:
                return None
        elif char == "/":
            right_side = equation[idx+1:]
            if "*" in right_side or "/" in right_side:
                continue
            left_side = string_equation_solver(equation[0:idx])
            right_side = string_equation_solver(right_side)
            if left_side is not None and right_side is not None:
                if right_side != 0:
                    return left_side/right_side
                else:
                    return None
            else:
                return None

    if equation[0] == "0":
        return None
    return int(equation)

def nerdle_key_gen(v, c):
    '''
    The nerdle key is the string of symbol colors given for each guess.
    We use these keys to group the words.  Entropy is calculated based on group sizes.
    v: guessed equation (pull from Valid equations.)
    c: secret equation (pull from Corret equations.)
    '''
    key = list("00000000")
    #  Correct Position Pass
    correct_letters = {}
    for idx in range(8):
        if v[idx] == c[idx]:
            if v[idx] in correct_letters:
                correct_letters[v[idx]].append(idx)
            else:
                correct_letters[v[idx]] = [idx]
            key[idx] = "2"
    #  Correct Letter Pass
    for idx in range(8):
        if key[idx] != "2":
            if v[idx] in c:
                #  There are some weird interactions when there are multiple copies of the same letter.
                #  The reason this section of code might seem more complicated than you might expect is because of that.
                v_count = v[:idx].count(v[idx])
                c_count = c.count(v[idx])
                correct_count = 0
                if v[idx] in correct_letters:
                    correct_count = 0
                    for cor_idx in correct_letters[v[idx]]:
                        if cor_idx > idx:
                            correct_count += 1
                if v_count + correct_count < c_count:
                    key[idx] = "1"
    return key

def generate_all_equations():
    '''
    This is a bit brute force but works!  This will generate every equation possible for nerdle and store it in a file.
    There are more efficient ways to do this, but we only have to generate it once, so I went with a quick implementation.
    '''
    valid_equations = []
    for equal_point in range(5,8):
        idx_limit = np.ones(equal_point-1)*13
        idx_limit[0] = 9
        idx_limit[-1] = 9

        current_idxs = np.zeros(equal_point-1)
        current_idxs[-2] = 10

        final_rollover = False
        while not final_rollover:
            equation_string = ""
            for idx in current_idxs:
                equation_string += valid_nerdle_characters[int(idx)]
            solution = string_equation_solver(equation_string)
            if solution is not None and float(solution).is_integer():
                equation_string += "=" + str(int(solution))
            if len(equation_string) == 8:
                valid_equations.append(equation_string)

            target_idx = 1

            current_idxs[-target_idx] += 1
            final_rollover = rollover_idxs(current_idxs, idx_limit)
            while not (current_idxs >= 10).any():
                current_idxs[-target_idx] += 1
                final_rollover = rollover_idxs(current_idxs, idx_limit)
            print(current_idxs)

    with open("./all_equations.p", "wb") as f:
        pickle.dump(valid_equations, f)
    print(valid_equations)

def rollover_idxs(idx_list, idx_limit):
    '''
    Checks if an index has gone over the corresponding index limit.  If so reduce to zero and carry the one.
    '''
    for idx in reversed(range(idx_list.shape[0])):
        if idx_list[idx] > idx_limit[idx]:
            if idx == 0:
                return True
            idx_list[idx-1] += 1
            idx_list[idx] = 0
        else:
            break
    return False
    

if __name__ == "__main__":
    generate_all_equations()