__author__ = "Grant Kurtz"

import copy

"""
	Rules of Hitori
	Rule One: When Solved, the same number does not appear twice (unblackened)
				in any single row or column.
	Rule Two: No two black squares are horizontally or vertically adjacent
				(diagonal is OK).
	Rule Three: All of the white squares form a single
				(horizontally and/or vertically) connected group.

	Puzzle Format
		* All puzzles are given as an N * N grid.
		* Each tile is a single string.
		* Each tile will be of the format [M]V, where M is an optional mark
		to indicate the tile is either White (W) or Black (B). V is the
		value of the tile (in the range of 1-n).
			* Example:
				B2	W1
				1	1
"""

class Puzzle:

	puzzle = []
	rows = 0

	def __init__(self, puzzle):
		self.puzzle = puzzle
		self.rows = len(puzzle)

	def getRows(self):
		return self.rows

	"""
		return		True if the puzzle state conforms to rules Two and Three of
					a Hitori puzzle (as defined above).
	"""
	def isValid(self):

		# First, check rule Two
		for row in range(0, self.rows):
			for col in range(0, self.rows):
				if self.isBlack(row, col):
					if row + 1 < self.rows and self.isBlack(row + 1, col):
						return False
					if col + 1 < self.rows and self.isBlack(row, col + 1):
						return False

		# Check rule Three


		return True

	def isSolved(self):
		return False

	def isBlack(self, row, col):
		return self.puzzle[row][col][0:1] == "B"

	def isWhite(self, row, col):
		return self.puzzle[row][col][0:1] == "W" \
		or self.puzzle[row][col].isnumeric()

	def markBlack(self, row, col):
		self.puzzle[row][col] = "B" + self.puzzle[row][col]

	def markWhite(self, row, col):
		self.puzzle[row][col] = "W" + self.puzzle[row][col]

	def getNum(self, row, col):
		tile = self.puzzle[row][col]
		if tile.isnumeric():
			return tile
		else:
			return self.puzzle[row][col][1:2]

	def getPuzzle(self):
		return self.puzzle

	def getCopy(self):
		return copy.deepcopy(self.puzzle)

"""
	solve_hitori

	Given a Hitori puzzle, will attempt to find a solution for that puzzle.

	puzzle		The puzzle to solve
	smart		If 0, then a brute force solver will be used to solve the
				puzzle, otherwise an intelligent solver will be used.
"""
def solve_hitori(puzzle, smart):

	# show the start state we are given
	print_puzzle(puzzle)

	if smart == 0:
		brute_solver(puzzle, 0)
	else:
		smart_solver(puzzle)

def find_all_valid(cur_state):
	valid_states = []
	for row in range(0, cur_state.getRows()):
		for col in range(0, cur_state.getRows()):
			if cur_state.isBlack(row, col):
				continue
			state = Puzzle(cur_state.getCopy())
			state.markBlack(row, col)
			if state.isValid():
				valid_states.append(state)
	return valid_states

def not_seen(state):
	return True


def print_states_gen(total_states):
	print("Total States Generated: " + str(total_states))


"""
	brute_solver

	Attempts to solve the given Hitori puzzle using the DFS algorithm.
	DFS was chosen for its low memory requirements.  Since Hitori only has a
	single valid solution for each puzzle, BFS isn't necessary to optimize for
	the fewest tiles to turn black. DFS was also chosen for its simple
	implementation.

	puzzle		The puzzle to solve
"""
def brute_solver(puzzle, total_states):

	# termination case
	if puzzle.isSolved():
		print_states_gen(total_states)
		print_puzzle(puzzle)
		return

	new_states = find_all_valid(puzzle)
	n_total_states = len(new_states) + total_states
	for state in new_states:
		if not_seen(state):
			brute_solver(state, n_total_states)

def smart_solver(puzzle):
	print("Finding Solution...")

def print_puzzle(puzzle):
	board = puzzle.getPuzzle()
	for row in board:
		for col in row:
			print(col, end=" ")
		print()

# Puzzles
puzzle1 = Puzzle([
	["2", "1"],
	["1", "1"]
])

# Brute-Force Solver
solve_hitori(puzzle1, 0)

# Smart solver
# solve_hitori(puzzle1, 1)

