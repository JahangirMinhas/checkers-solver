# checkers-solver
An optimized Checkers AI solver that uses game tree search with alpha-beta pruning to solve endgame puzzles efficiently. Implements move generation, including simple moves and mandatory multi-jumps, and an evaluation function to guide decisions. Designed to find the shortest path to victory within strict runtime limits.

# Running
python3 checkers.py --inputfile (input file path) --outputfile (output file path)

# Board File:
'r' - red piece <br />
'b' - black piece <br />
'R' - king red piece <br />
'B' - king black piece <br />

Examples are in './tests'
