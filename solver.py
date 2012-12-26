def solve_hitori(puzzle, intelligent):

	# show the start state we are given
	print_puzzle(puzzle)

	if(intelligent == 0):
		brute_solver(puzzle, 0)
	else:
		smart_solver(puzzle)


def is_valid(state):
	for row in range(0, len(state)):
		for col in range(0, len(state)):
			pass
	return False

def is_solved(state):
	return False

def is_black(puzzle, row, col):
	return puzzle[row][col].index(0, 1) == "B"

def is_white(puzzle, row, col):
	return puzzle[row][col].index(0, 1) == "W"

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
	valid_states = [cur_state]
	state = cur_state
	if is_valid(state):
		valid_states.append(state)
	return valid_states


"""
	brute_solver

	Attempts to solve the given Hitori puzzle using the DFS algorithm.
	DFS was chosen for its low memory requirements.  Since Hitori only has a
	single valid solution for each puzzle, BFS isn't necessary to optimize for
	the fewest tiles to turn black. DFS was also chosen for its simple
	implementation.

	puzzle		The puzzle to solve
"""

def not_seen(state):
	return True


def print_states_gen(total_states):
	print("Total States Generated: " + str(total_states))


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
			print(str(col), end=" ")
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