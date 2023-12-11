import sys
import re
from collections import deque
from copy import copy, deepcopy
FILENAME = "dumb3x3.bugs"


def main():
    filename = ""
    numArgs = len(sys.argv)
    if numArgs < 2:
        filename = FILENAME
    else:
        filename = sys.argv[1]

    board = read_board(filename)
    solver = bugrush(3, board=board)
    solver.__str__()
    moves = solver.moves()
    print(moves)

    # Make a copy of an object with the given class but no fields.
# https://www.oreilly.com/library/view/python-cookbook/0596001673/ch05s12.html


def empty_copy(obj):
    class Empty(obj.__class__):
        def __init__(self): pass
    newcopy = Empty()
    newcopy.__class__ = obj.__class__
    return newcopy


class bugrush(object):

    def __init__(self, n, sat=True, board=None):
        self.sat = sat
        self.board = board
        self.n = n

    def __copy__(self):
        newcopy = empty_copy(self)
        newcopy.board = deepcopy(self.board)
        newcopy.n = self.n
        # newcopy.blank = self.blank
        # newcopy.g = self.g
        return newcopy

    def __str__(self) -> str:
        n = self.n
        for x in range(1, n + 1):
            for y in range(0, n):
                print(self.board[x][y], end='')
            print()

    def moves(self):
        print(self.board)
        n = self.n
        moves = []
        for x in range(1, n + 1):
            for y in range(0, n):
                piece = self.board[x][y]
                if piece == '>' or piece == '-':
                    if y > 0 and self.board[x][y-1] == ' ':
                        moves.append([(x, y-1), (x, y)])
                    if y < n - 1 and self.board[x][y+1] == ' ':
                        moves.append([(x, y+1), (x, y)])
                elif piece == '|':
                    if x > 1 and self.board[x - 1][y] == ' ':
                        moves.append([(x-1, y), (x, y)])
                    if x < n and self.board[x + 1][y] == ' ':
                        moves.append([(x+1, y), (x, y)])
        return moves

    def bfs_solution(self):
        # Don't mess up this state, just make a new start
        # state.
        start = copy(self)
        start.parent = None
        start.moved = None
        visited = {hash(start)}

        # Run the BFS.
        q = deque()
        q.appendleft(start)
        while len(q) > 0:
            # Get next state to expand.
            s = q.pop()

            # Try to expand each child.
            ms = s.moves()
            for m in ms:
                # Make the child.
                c = copy(s)
                c.move(m)

                # Found a solution. Reconstruct and return
                # it.
                if c.solved():
                    soln = [m]
                    while True:
                        s = s.parent
                        if not s:
                            break
                        soln.append(s.moved)
                    return list(reversed(soln))

                # Don't re-expand a closed state.
                h = hash(c)
                if h in visited:
                    continue

                # Expand and enqueue this child.
                c.parent = s
                c.moved = m
                visited.add(h)
                q.appendleft(c)

        # No solution exists.
        return None


def read_board(filename):
    print("filename: " + filename)
    boardFile = open(filename, 'r')
    board = []
    for row in boardFile:

        piece = [str(i) for i in row.removesuffix('\n')]
        board.append(piece)
    return board


main()
