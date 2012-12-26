def solve_hitori(puzzle, intelligent):

	# show the start state we are given
	print_puzzle(puzzle)

	if(intelligent == 0):
		brute_solver(puzzle)
	else:
		smart_solver(puzzle)


def is_valid(state):
	for row in range(0, len(state)):
		for col in range(0, len(state)):
			pass

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
	valid_states = []
	state = cur_state
	if is_valid(state):
		valid_states.append(state)


def brute_solver(puzzle):
	queue = []
	num_states = 0
	while len(queue) != 0:
		cur_state = queue.pop()
		new_states = find_all_valid(cur_state)
		num_states += len(new_states)
		queue.append(new_states)

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