# Bug Rush

This repository contains a Python program developed to solve the "bugrush" puzzles, using an efficient Breadth First Search (BFS) algorithm to navigate through puzzle states and identify solutions or unsolvable configurations.

A Bug Rush puzzle is considered solved when the '>' piece reaches the rightmost space of the board within its row.

## Key Components and Technologies:

**Modules and Constants:**
- `sys`: Used for processing command-line arguments.
- `FILENAME`: The default file name containing the puzzle layout.
- `N` and `M`: Dimensions of the puzzle board (rows and columns).

**Testing Mechanism:**
- `TESTS`: A boolean flag to enable running tests with predefined puzzle states.
- `RAND_FILES` and `PLAY_FILES`: Sets of files used for testing, each containing the expected outcomes.

**Primary Functionality:**
- `main()`: The main entry point of the program, handling input and managing the puzzle-solving process.

### Bugrush Class Details:

The `bugrush` class is at the heart of this project, encapsulating the puzzle logic and solving algorithm.

- `__init__(self, n, m, board=None)`: Initializes the puzzle with specified dimensions and state.
- `__copy__(self)`: Creates a deep copy of the puzzle state.
- `__str__(self)`: Returns a string representation of the puzzle.
- `__eq__(self)`: Checks the equivalence of two puzzle states.
- `moves(self)`: Determines possible moves in the current puzzle configuration.
- `move(self, newMove)`: Applies a move to the puzzle.
- `target(self)`: Identifies the target row in the puzzle.
- `solved(self)`: Checks if the puzzle is in a solved state.
- `bfs_solution(self)`: Implements the BFS algorithm to find the shortest solution path.

### Auxiliary Function:

- `read_board(filename)`: Reads the puzzle layout from a file.

### Setup and Execution Instructions:

**Prerequisites:**
- Python should be installed on your system.

**Setup:**
1. Clone or download the repository to your local environment.
2. Ensure puzzle files are in the same directory as the script.

**Running the Solver:**
- Execute the script with `python bugrush.py filename n m` in the command line.
- The script will output the number of moves to solve the puzzle or 'unsat' for unsolvable puzzles.

### Example Puzzle Layout:

Design your puzzles adhering to the format below

1. The first line should contain only '-' characters, spanning the entire width of the puzzle.
2. Use '-' to depict horizontal cars, which can move either left or right.
3. Use '|' for vertical cars that can shift a single space up or down.
4. Incorporate just one '>' to denote the bug, which can traverse left or right.
5. Pieces can only be moved into a space where there is no existing piece at that moment. (An empty space)
6. A puzzle is deemed "sat" if the bug can navigate to the far-right boundary of the puzzle.

#### Example 5x7:

\-------

|--|---

|----||

\> |||||

||-|-||

&nbsp;|-|||-


