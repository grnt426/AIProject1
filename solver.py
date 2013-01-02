import copy
import cProfile
import pstats
from collections import deque
import random

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
	puzzle = ()
	markedPuzzle = {}
	rows = 0
	_markedBlack = 0
	_ruleOne = 0
	_ruleTwo = 0
	_brokeRuleTwo = 0
	_ruleThree = 0

	"""
		puzzle	The array to use to define this Puzzle.
		marked	Whether elements in the array were pre-marked before passing
				to this class.
	"""
	def __init__(self, puzzle, marked):
		self.puzzle = puzzle
		self.rows = len(puzzle)
		self.markedPuzzle = [[False]*self.rows for x in range(self.rows)]
		if marked:
			self.countMarked()

	def getRows(self):
		return self.rows

	"""
		return		True if the puzzle state conforms to Rules Two and Three of
					a Hitori puzzle (as defined above).
	"""

	def isValid(self):
		return self.conformsToRuleTwo() and self.conformsToRuleThree()

	def conformsToRuleOne(self):

		# To help speed things up, we cache some results
		if self._ruleOne:
			return True

		colData = {}
		for row in range(0, self.rows):
			rowData = []
			for col in range(0, self.rows):
				num = self.getNum(row, col)
				if self.isWhite(row, col):
					if num in rowData or (col in colData and num in colData[col]):
						self._ruleOne = 0
						return False
					rowData.append(num)
					if col not in colData:
						colData[col] = []
					colData[col].append(num)

		self._ruleOne = 1
		return True

	def conformsToRuleTwo(self):

		# To help speed things up, we cache some results
		if self._ruleTwo:
			return True
		if self._brokeRuleTwo:
			return False

		for row in range(0, self.rows):
			for col in range(0, self.rows):
				if self.isBlack(row, col):
					if row + 1 < self.rows and self.isBlack(row + 1, col):
						self._ruleTwo = 0
						return False
					if col + 1 < self.rows and self.isBlack(row, col + 1):
						self._ruleTwo = 0
						return False
		self._ruleTwo = 1
		return True

	def conformsToRuleThree(self):

		# To help speed things up, we cache some results
		if self._ruleThree:
			return True

		totalWhite = self.rows * self.rows - self._markedBlack
		totalVisited = 0
		queue = deque()
		seen = []

		# The first or second element must be White (because otherwise this
		# puzzle would fail Rule Two), and this puzzle must minimally be
		# 2x2, so we are guaranteed to find a White tile
		if self.isWhite(0, 0):
			queue.append((0, 0))
		elif self.isWhite(0, 1):
			queue.append((0, 1))
		else:
			self._ruleThree = 0
			return False

		while len(queue) > 0:
			tile = queue.popleft()
			if tile in seen:
				continue
			else:
				seen.append(tile)
			totalVisited += 1
			row = tile[0]
			col = tile[1]
			if row - 1 >= 0 and self.isWhite(row - 1, col):
				queue.append((row - 1, col))
			if row + 1 < self.rows and self.isWhite(row + 1, col):
				queue.append((row + 1, col))
			if col - 1 >= 0 and self.isWhite(row, col - 1):
				queue.append((row, col - 1))
			if col + 1 < self.rows and self.isWhite(row, col + 1):
				queue.append((row, col + 1))

		if totalVisited == totalWhite:
			self._ruleThree = 1
			return True
		else:
			self._ruleThree = 0
			return False

	def isSolved(self):
		return self.conformsToRuleOne() and self.conformsToRuleTwo()  \
		and self.conformsToRuleThree()

	def isBlack(self, row, col):
		if row < 0 or row >= self.rows or col < 0 or col >= self.rows:
			return False
		return self.markedPuzzle[row][col]

	def isWhite(self, row, col):
		return not self.markedPuzzle[row][col]

	def markBlack(self, row, col):
		self.invalidateRuleCache()
		self.markedPuzzle[row][col] = True
		self._markedBlack += 1

		# To speed things up, quickly check if we broke rule two
		if self.isBlack(row - 1, col) or self.isBlack(row + 1, col) \
		or self.isBlack(row, col - 1) or self.isBlack(row, col + 1):
			self._brokeRuleTwo = 1

	def undoBlackMark(self, row, col):
		self.invalidateRuleCache()
		self.markedPuzzle[row][col] = False
		self._markedBlack -= 1

	def markWhite(self, row, col):
		self.invalidateRuleCache()
		self.markedPuzzle[row][col] = False

	def getNum(self, row, col):
		return self.puzzle[row][col]

	def getPuzzle(self):
		return self.puzzle

	def getCopy(self):
		return copy.deepcopy(self.puzzle)

	def makePuzzleCopy(self):
		state = self.getCopy()
		markedPuzzle = copy.deepcopy(self.markedPuzzle)
		p = Puzzle(state, False)
		p._ruleOne = self._ruleOne
		p._ruleTwo = self._ruleTwo
		p._brokeRuleTwo = self._brokeRuleTwo
		p._ruleThree = self._ruleThree
		p._markedBlack = self._markedBlack
		p.markedPuzzle = markedPuzzle
		return p

	"""
		Updates the markedBlack counter.  Useful for manually constructed
		puzzles where the Black tiles were marked in the array instead of
		through function calls.
	"""
	def countMarked(self):
		self._markedBlack = 0
		for row in range(0, self.rows):
			for col in range(0, self.rows):
				if self.isBlack(row, col):
					self._markedBlack += 1

	def invalidateRuleCache(self):
		self._ruleOne = 0
		self._ruleTwo = 0
		self._ruleThree = 0
		self._brokeRuleTwo = 0

"""
	solve_hitori

	Given a Hitori puzzle, will attempt to find a solution for that puzzle.

	puzzle		The puzzle to solve
	smart		If 0, then a brute force solver will be used to solve the
				puzzle, otherwise an intelligent solver will be used.
"""

def solve_hitori(puzzle, smart):

	# Make sure our Seen List is empty
	clearSeen()

	# show the start state we are given
	print("Start Puzzle State")
	print_puzzle(puzzle)
	print()

	if smart == 0:
#		if not brute_solver(puzzle, 0):
#			print("No Solution")
		if not brute_solver2(puzzle):
			print("No Solution")
	else:
		smart_solver(puzzle)


def find_all_valid(cur_state):
	valid_states = []
	for row in range(0, cur_state.getRows()):
		for col in range(0, cur_state.getRows()):
			if cur_state.isBlack(row, col):
				continue
			cur_state.markBlack(row, col)
			if cur_state.isValid():
				state = cur_state.makePuzzleCopy()
				valid_states.append(state)
			cur_state.undoBlackMark(row, col)
	return valid_states


def notSeen(state):
	return flattenState(state) not in seenDict


def flattenState(state):
	resultStr = ""
	rows = state.getRows()
	puzzle = state.getPuzzle()
	marked = state.markedPuzzle
	for row in range(0, rows):
		for col in range(0, rows):
			resultStr += str(marked[row][col]) + str(puzzle[row][col])
	return resultStr


def markedSeen(state):
	seenDict[flattenState(state)] = 1
	if len(seenDict) % 1000 == 0:
		print("Seen: " + str(len(seenDict)))

def clearSeen():
	seenDict.clear()


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
	return		True if the puzzle was solved, otherwise False
"""

def brute_solver(puzzle, totalStates):
	# termination case
	if puzzle.isSolved():
		print("Final Solution State")
		print_puzzle(puzzle)
		print_states_gen(totalStates)
		return True

	new_states = find_all_valid(puzzle)
	n_total_states = len(new_states) + totalStates
	for state in new_states:
		if notSeen(state):
			markedSeen(state)
			if brute_solver(state, n_total_states):
				return True
	return False

def brute_solver2(puzzle):
	queue = deque([puzzle])
	totalStates = 0

	while len(queue) > 0:
		state = queue.popleft()

		# Only bother with new states
		if notSeen(state):
			markedSeen(state)
		else:
			continue

		# Check if this is the winning state afterwards, since we are more
		# likely to find a duplicate state (and therefore not need to do more)
		# instead of finding the goal state
		if state.isSolved():
			print("Final Solution State")
			print_puzzle(state)
			print_states_gen(totalStates)
			return True

		# Otherwise we resume creating more states
		new_states = find_all_valid(state)
		queue += new_states
		totalStates += len(new_states)
	return False

def smart_solver(puzzle):
	print("Finding Solution...")


def print_puzzle(puzzle):
	board = puzzle.getPuzzle()
	marked = puzzle.markedPuzzle
	rows = puzzle.getRows()
	for row in range(0, rows):
		for col in range(0, rows):
			if marked[row][col]:
				print("B", end="")
			print(str(board[row][col]), end=" ")
		print()

# Puzzles
puzzle1 = Puzzle((
	(2, 1),
	(1, 1)
), False)

puzzle2 = Puzzle((
	(1, 2, 3),
	(1, 1, 3),
	(2, 3, 3)
), False)

puzzle3 = Puzzle((
	(1, 2, 3),
	(2, 2, 3),
	(1, 1, 3)
), False)

puzzle4 = Puzzle((
	(3, 2, 5, 4, 5),
	(2, 3, 4, 3, 5),
	(4, 3, 2, 4, 4),
	(1, 3, 3, 5, 5),
	(5, 4, 1, 2, 3)
), False)

# Seen List
seenList = []
seenDict = {}

# Brute-Force Solver
solve_hitori(puzzle1, 0)
print()
solve_hitori(puzzle2, 0)
print()
solve_hitori(puzzle3, 0)
print()
#solve_hitori(puzzle4, 0)
cProfile.run('solve_hitori(puzzle4, 0)', 'output.txt')
p = pstats.Stats('output.txt')
p.sort_stats('time')
p.print_stats()


# Smart solver
# solve_hitori(puzzle1, 1)

