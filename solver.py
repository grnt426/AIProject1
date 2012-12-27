__author__ = "Grant Kurtz"

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

"""
	return		True if the puzzle state conforms to rules Two and Three of
				a Hitori puzzle (as defined above).
"""
def is_valid(state):

	# First, check rule Two
	for row in range(0, len(state)):
		for col in range(0, len(state)):
			if is_black(state, row, col):
				if row + 1 < len(state) and is_black(state, row + 1, col):
					return False
				if col + 1 < len(state) and is_black(state, row, col + 1):
					return False

	# Check rule Three


	return True

def is_solved(state):
	return False

def is_black(puzzle, row, col):
	return puzzle[row][col].index(0, 1) == "B"

def is_white(puzzle, row, col):
	return puzzle[row][col].index(0, 1) == "W" or puzzle[row][col].isnumeric()

def mark_black(puzzle, row, col):
	puzzle[row][col] = "B" + puzzle[row][col]
	return puzzle

def mark_white(puzzle, row, col):
	puzzle[row][col] = "W" + puzzle[row][col]
	return puzzle

def get_num(puzzle, row, col):
	tile = puzzle[row][col]
	if tile.isnumeric():
		return tile
	else:
		return puzzle[row][col].index(1)


def find_all_valid(cur_state):
	valid_states = []
	for row in range(0, len(cur_state)):
		for col in range(0, len(cur_state)):
			if is_black(cur_state, row, col):
				continue
			state = cur_state.deepcopy()
			mark_black(state, row, col)
			if is_valid(state):
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
	if is_solved(puzzle):
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
	for row in puzzle:
		for col in row:
			print(col, end=" ")
		print()

# Puzzles
puzzle1 = [
	["2", "1"],
	["1", "1"]
]

# Brute-Force Solver
solve_hitori(puzzle1, 0)

# Smart solver
# solve_hitori(puzzle1, 1)