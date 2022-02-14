
import pickle
import math
from utils import nerdle_key_gen
import ray

valid_nerdle_keys = "012"

def trim_dictionary_by_key(guess, guess_key, dictionary):
    '''
    Trims dictionary of equationss that would not provide the associated nerdle key given the guess.
    '''
    new_dictionary = []
    for word in dictionary:
        iter_key = nerdle_key_gen(guess, word)
        if iter_key == guess_key:
            new_dictionary.append(word)
    return new_dictionary

@ray.remote(num_cpus=1)
def solve_nerdle(secret_equation = None, prune_valid_equations = False):
    '''
    secret_word:  The equation nerdle bot is solving for.  If given, the nerdle bot will run automatically.  If None is given, wordle bot will ask for user inputs.
    prune_valid_words:  Sometimes guessing words you know are incorrect to gather info is the better strategy.  However, this makes things run longer as there are more words to go through.
    Turn on prune_valid_words for better performance but slightly worse results.

    Returns the amount of guesses it took to win the provided game.
    '''
    with open("./all_equations.p", "rb") as f:
        valid_equations = pickle.load(f)

    correct_equations = valid_equations.copy()
    equation_to_guess = secret_equation
    guess = "48-32=16"
    
    for guess_iteration in range(6):
        print("-----------------------------------------------------------------------")
        print("Guessing: " + guess)

        if secret_equation:
            guess_key = nerdle_key_gen(guess, equation_to_guess)
        else:
            while True:
                guess_key = list(input("Entere Wordle Key: (Green = 2, Purple = 1, Black = 0)"))
                if len(guess_key) == 8 and all(elem in guess_key for elem in valid_nerdle_keys):
                    break
                else:
                    print("Invalid input.  Do not use spaces and make sure to only use 8 numbers.  The nerdle key is the colors you get back after your guess.")
        if guess_key == ['2', '2', '2', '2', '2', '2', '2', '2']:
            print("YOU WIN ON ITERATION: " + str(guess_iteration + 1))
            return guess_iteration

        if prune_valid_equations:
            valid_equations = trim_dictionary_by_key(guess, guess_key, valid_equations)
        correct_equations = trim_dictionary_by_key(guess, guess_key, correct_equations)

        if len(correct_equations) == 1:
            guess = correct_equations[0]
            continue
        elif len(correct_equations) == 2:
            valid_equations = correct_equations
        
        total_correct_words = len(valid_equations)
        best_word = ""
        best_group_worth = 0
        for v in valid_equations:
            dictionary_word_groups = {}
            for c in correct_equations:
                key = nerdle_key_gen(v, c)
                key = "".join(key)
                if key in dictionary_word_groups:
                    dictionary_word_groups[key] += 1
                else:
                    dictionary_word_groups[key] = 1
            word_worth = 0
            for key in dictionary_word_groups:
                group_count = dictionary_word_groups[key]
                probability = group_count/total_correct_words
                word_worth += -probability * math.log2(probability)

            if word_worth > best_group_worth:
                best_group_worth = word_worth
                best_word = v
        guess = best_word
    return 6

def solve_nerdle_no_ray(secret_equation = None, prune_valid_equations = False):
    '''
    Same code as above but does not run ray.
    secret_word:  The equation nerdle bot is solving for.  If given, the nerdle bot will run automatically.  If None is given, wordle bot will ask for user inputs.
    prune_valid_words:  Sometimes guessing words you know are incorrect to gather info is the better strategy.  However, this makes things run longer as there are more words to go through.
    Turn on prune_valid_words for better performance but slightly worse results.

    Returns the amount of guesses it took to win the provided game.
    '''
    with open("./all_equations.p", "rb") as f:
        valid_equations = pickle.load(f)

    correct_equations = valid_equations.copy()
    equation_to_guess = secret_equation
    guess = "48-32=16"
    
    for guess_iteration in range(6):
        print("-----------------------------------------------------------------------")
        if secret_equation is None:
            print("Please enter the following guess into nerdle and then enter the key you recieve.")
        print("Guessing: " + guess)
        if secret_equation:
            guess_key = nerdle_key_gen(guess, equation_to_guess)
        else:
            while True:
                guess_key = list(input("Entere Wordle Key: (Green = 2, Yellow = 1, Black = 0)"))
                if len(guess_key) == 8 and all(elem in valid_nerdle_keys for elem in guess_key):
                    break
                else:
                    print("Invalid input.  Do not use spaces and make sure to only use 8 numbers.  The nerdle key is the colors you get back after your guess.")
        if guess_key == ['2', '2', '2', '2', '2', '2', '2', '2']:
            print("YOU WIN ON ITERATION: " + str(guess_iteration + 1))
            return guess_iteration

        if prune_valid_equations:
            print("Previous possible valid_equations count = " + str(len(valid_equations)))
            valid_equations = trim_dictionary_by_key(guess, guess_key, valid_equations)
            print("Current possible valid_equations count = " + str(len(valid_equations)))

        print("Previous possible correct_equations count = " + str(len(correct_equations)))
        correct_equations = trim_dictionary_by_key(guess, guess_key, correct_equations)
        print("Current possible correct_equations count = " + str(len(correct_equations)))

        if len(correct_equations) == 1:
            guess = correct_equations[0]
            continue
        elif len(correct_equations) == 2:
            valid_equations = correct_equations
        
        total_correct_words = len(valid_equations)
        best_word = ""
        best_group_worth = 0
        for v in valid_equations:
            dictionary_word_groups = {}
            for c in correct_equations:
                key = nerdle_key_gen(v, c)
                key = "".join(key)
                if key in dictionary_word_groups:
                    dictionary_word_groups[key] += 1
                else:
                    dictionary_word_groups[key] = 1
            word_worth = 0
            for key in dictionary_word_groups:
                group_count = dictionary_word_groups[key]
                probability = group_count/total_correct_words
                word_worth += -probability * math.log2(probability)

            if word_worth > best_group_worth:
                best_group_worth = word_worth
                best_word = v
        guess = best_word
    return 6