'''
Code by Garrett Fosdick
Runs all possible wordle games and gathers stats on bot performance.
'''

from nerdle_solver import solve_nerdle
import matplotlib.pyplot as plt
import ray
import pickle

if __name__ == "__main__":
    ray.init()
    #Loads all possbile correct wordle words.
    with open("./all_equations.p", "rb") as f:
        valid_equations = pickle.load(f)

    total_games = len(valid_equations)
    game_wins = [0, 0, 0, 0, 0, 0, 0]
    #Submits tasks with threading for speedy completion.
    task_ref_list = []
    for static_equations in valid_equations:
        task_ref_list.append(solve_nerdle.remote(secret_equation = static_equations, prune_valid_equations = True))
    #Retrieves results of threaded tasks.
    for idx, ref in enumerate(task_ref_list):
        print(str(idx) + "/" + str(total_games))
        #Increments the number of wins.
        game_wins[ray.get(ref)] += 1

    print(game_wins)
    fig = plt.figure()
    ax = fig.add_axes([0.05, 0.05, 0.9, 0.9])
    time = ["One", "Two", "Three", "Four", "Five", "Six", "Loss"]
    ax.bar(time, game_wins)
    plt.show()