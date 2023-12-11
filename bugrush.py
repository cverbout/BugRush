import sys
from collections import deque
from copy import copy

# Constants
FILENAME = "unsat5x7.bugs"
N = 5
M = 7

def main():
    # Handle Command Line input and default input
    filename = ""
    n = 0
    m = 0
    numArgs = len(sys.argv)
    if numArgs < 2:
        filename = FILENAME
        n = N
        m = M
    else:
        filename = sys.argv[1]
        n = int(sys.argv[2])
        m = int(sys.argv[3])

    board = read_board(filename)
    
    solver = bugrush(n, m, board)
    sln = solver.bfs_solution()
    
    if sln:
        print(len(sln))
    else:
        print ("unsat")
    
# Make a copy of an object with the given class but no fields.
# https://www.oreilly.com/library/view/python-cookbook/0596001673/ch05s12.html
def empty_copy(obj):
    class Empty(obj.__class__):
        def __init__(self): pass
    instanceCopy = Empty()
    instanceCopy.__class__ = obj.__class__
    return instanceCopy


class bugrush(object):
    def __init__(self, n, m, board=None):
        self.board = board
        self.n = n
        self.m = m
        self.goal = self.target()
        assert n > 1
        assert m > 1
        assert board != None

    # Copy returns a deepcopy of the board
    def __copy__(self):
        instanceCopy = empty_copy(self)
        instanceCopy.board = [list(row) for row in self.board]
        instanceCopy.n = self.n
        instanceCopy.m = self.m
        instanceCopy.goal = self.goal
        return instanceCopy
        

    # Returns a string of the board
    def __str__(self):
        n = self.n
        m = self.m
        result = ""
        for row in range(1, n + 1):
            for col in range(0, m):
                result += self.board[row][col]
            result += "\n"
        return result
            
    # Board configuration equivalence determines equality
    def __eq__(self, other):
        self.board == other.board
        
    # Turns the board into a 1D list
    def board_list(self): 
        return [space for row in self.board for space in row]
    
    # Returns a unique hash. Converts 1D list of board into Tuple for hashing.
    def __hash__(self):
        return hash(tuple(self.board_list()))

    # Returns the list of actionable moves given a board configuration
    def moves(self):
        n = self.n
        m = self.m
        moves = []
        # Check each piece
        for row in range(1, n + 1):
            for col in range(0, m):
                piece = self.board[row][col]
                # Given a piece and conditions needed to move, add the move
                if piece in ('>', '-'):
                    if col > 0 and self.board[row][col-1] == ' ':
                        moves.append([(row, col-1), (row, col)])
                    if col < m - 1 and self.board[row][col+1] == ' ':
                        moves.append([(row, col+1), (row, col)])
                elif piece == '|':
                    if row > 1 and self.board[row - 1][col] == ' ':
                        moves.append([(row-1, col), (row, col)])
                    if row < n and self.board[row + 1][col] == ' ':
                        moves.append([(row+1, col), (row, col)])
        # moves stored as [(destination), (source)]
        return moves
    
    # Given a move, enact it on the board
    def move(self, newMove):
        destPos = newMove[0]
        destPiece = self.board[destPos[0]][destPos[1]]
        currentPos = newMove[1]
        currentPiece = self.board[currentPos[0]][currentPos[1]]
        # Swap pieces
        self.board[currentPos[0]][currentPos[1]] = destPiece
        self.board[destPos[0]][destPos[1]] = currentPiece
    
    # Return the solution row  
    def target(self):
        n = self.n
        m = self.m
        count = 0
        for row in range(1, n + 1):
            for col in range(0, m):
                if self.board[row][col] == '>':
                    solution = row
                    count += 1
        # Ensure 1 solution
        assert count == 1
        return solution
    
    
    # Check if the board is in a solved configuration
    def solved(self):
        return self.board[self.goal][self.m - 1] == '>'

    

    # Breadth First Search of board to find fewest moves needed to solve
    def bfs_solution(self):
        # Create a fresh state to test. Prevents erroneous state alteration
        startState = copy(self)
        startState.parent = None
        startState.moved = None
        #startState.goal = self.target()
        
        # Set for tracking visited states
        visited = {hash(startState)}
        # BFS begin
        statesToTry = deque()
        statesToTry.append(startState)
        while statesToTry:
            # Pop the next state in the queue to look at
            currentState = statesToTry.popleft()

            # Examine the possible moves of the current state
            moveSet = currentState.moves()
            for currentMove in moveSet:
                # Make the move to get the Hash then undo it
                # This will prevent us from making uneccessary deepcopies which take up the most time
                currentState.move(currentMove)
                stateHash = hash(currentState)
                undoMove = currentMove[1], currentMove[0]
                currentState.move(undoMove)
                
                # Check if this state was already hashed to prevent repetition
                if stateHash in visited:
                    continue
                
                # Create a child and try each move
                childState = copy(currentState)
                childState.move(currentMove)
            
                # Check for solved position 
                if childState.solved():
                    solution = [currentMove]
                    while True:
                        currentState = currentState.parent
                        if not currentState:
                            break
                        solution.append(currentState.moved)
                    return list(reversed(solution))

                # Store information, add to visited, and enque child
                childState.parent = currentState
                childState.moved = currentMove
                visited.add(stateHash)
                statesToTry.append(childState)

        # Unsat board, no solution.
        return None

# Read in a board given a file name, return in correct format
def read_board(filename):
    boardFile = open(filename, 'r')
    board = []
    for row in boardFile:
        piece = [str(i) for i in row.removesuffix('\n')]
        board.append(piece)
    return board
    
# Run program
main()