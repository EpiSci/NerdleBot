Code By Garrett Fosdick

# NerdleBot

Install:\
-Make sure to be running python 3.8.  Newer version are likely to work as well, but the code was made and tested with 3.8.\
-Install ray and matplotlib.\
Depending on how your python is set up either run:\
    python3.8 -m pip install ray\
    python3.8 -m pip install matplotlib\
Or:\
    python -m pip install ray\
    python -m pip install matplotlib\
-You are good to go!\
    python3.8 daily_nerdle_solver.py\
    python3.8 complete_nerdle_graph.py\
Or:\
    python daily_nerdle_solver.py\
    python complete_nerdle_graph.py\

Contents:
daily_nerdle_solver.py:  This python script helps the user solve the daily nerdle.  Enter the guess given to you by our wordle bot and then enter the corresponding key given to you by wordle.
For the wordle key, black = 0, yellow = 1, and green = 2.  Enter the key with no spaces in order.
Example Green, Yellow, Black, Black, Yellow would be entered as 21001.

complete_nerdle_graph.py:  This python script will make the wordle bot automatically play all 20355 possible nerdle games. (This takes a few minutes.)  Once the run is done, it will produce a graph of the number of games that ended in a set number of guesses.

nerdle_solver.py:  This is where the majority of the code exists.  The actual wordle solving code exists here and the other scripts just make use of it.

utils.py:  Several tools for the other scripts to use.  Also generates all nerdle equations.
