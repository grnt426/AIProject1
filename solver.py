import copy
from collections import deque

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
	markedPuzzle = []
	rows = 0
	_markedBlack = 0
	_ruleOne = 0
	_ruleTwo = 0
	_brokeRuleTwo = 0
	_ruleThree = 0

	_WHITE = 0
	_BLACK = 1
	_ADJACENT = 2
	_EXPLICITLY_WHITE = 3


	"""
		puzzle	The array to use to define this Puzzle.
		marked	Whether elements in the array were pre-marked before passing
				to this class.
	"""
	def __init__(self, puzzle, marked):
		self.puzzle = puzzle
		self.rows = len(puzzle)
		self.markedPuzzle = [[self._WHITE]*self.rows for x in range(self.rows)]
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
					if num in rowData or \
					   (col in colData and num in colData[col]):
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
				if self.markedPuzzle[row][col] == self._BLACK:
					if row + 1 < self.rows and self.markedPuzzle[row + 1][col] == self._BLACK:
						self._ruleTwo = 0
						return False
					if col + 1 < self.rows and self.markedPuzzle[row][col + 1] == self._BLACK:
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
			if row >= 1 and not self.markedPuzzle[row - 1][col] == self._BLACK:
				queue.append((row - 1, col))
			if row < self.rows - 1 and not self.markedPuzzle[row + 1][col] == self._BLACK:
				queue.append((row + 1, col))
			if col >= 1 and not self.markedPuzzle[row][col - 1] == self._BLACK:
				queue.append((row, col - 1))
			if col < self.rows - 1 and not self.markedPuzzle[row][col + 1] == self._BLACK:
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
		return self.markedPuzzle[row][col] == self._BLACK

	def isWhite(self, row, col):
		return self.markedPuzzle[row][col] == self._WHITE or \
			   self.markedPuzzle[row][col] == self._EXPLICITLY_WHITE

	def isExplicitlyMarkedWhite(self, row, col):
		return self.markedPuzzle[row][col] == self._EXPLICITLY_WHITE

	def markBlack(self, row, col):
		self.invalidateRuleCache()
		self.markedPuzzle[row][col] = self._BLACK
		self._markedBlack += 1

		# To speed things up, quickly check if we broke rule two
		if self.isBlack(row - 1, col) or self.isBlack(row + 1, col) \
		or self.isBlack(row, col - 1) or self.isBlack(row, col + 1):
			self._brokeRuleTwo = 1

	def undoBlackMark(self, row, col):
		self.invalidateRuleCache()
		self.markedPuzzle[row][col] = self._WHITE
		self._markedBlack -= 1

	def markWhite(self, row, col):
		self.invalidateRuleCache()
		self.markedPuzzle[row][col] = self._WHITE

	def markExplicitlyWhite(self, row, col):
		self.markedPuzzle[row][col] = self._EXPLICITLY_WHITE

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
				if self.markedPuzzle[row][col] == self._BLACK:
					self._markedBlack += 1

	def invalidateRuleCache(self):
		self._ruleOne = 0
		self._ruleTwo = 0
		self._ruleThree = 0
		self._brokeRuleTwo = 0

	def markAdjacent(self, row, col):
		self.markedPuzzle[row][col] = self._ADJACENT

	def isMarkedAdjacent(self, row, col):
		return self.markedPuzzle[row][col] == self._ADJACENT

"""
	solve_hitori

	Given a Hitori puzzle, will attempt to find a solution for that puzzle.

	:param puzzle:		The puzzle to solve
	:type puzzle: Puzzle
	smart		If 0, then a brute force solver will be used to solve the
				puzzle, otherwise an intelligent solver will be used.
"""

def solve_hitori(puzzle, smart):

	# Make sure our Seen List is empty
	clearSeen()
	markedSeen(puzzle)
	totalStates = 0

	# show the start state we are given
	print("Start Puzzle State")
	print_puzzle(puzzle)
	print()

	if smart == 0:
		if not brute_solver(puzzle):
			print("No Solution")
#		if not brute_solver2(puzzle):
#			print("No Solution")
	else:
		smart_solver(puzzle)


def find_all_valid(cur_state):
	valid_states = []
	for row in range(0, cur_state.getRows()):
		for col in range(0, cur_state.getRows()):
			if cur_state.markedPuzzle[row][col] == cur_state._BLACK:
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
	return repr(state.markedPuzzle)


def markedSeen(state):
	seenDict[flattenState(state)] = 1
	if len(seenDict) % 5000 == 0:
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

def brute_solver(puzzle):

	global totalStates

	# termination case
	if puzzle.isSolved():
		print("Final Solution State")
		print_puzzle(puzzle)
		print_states_gen(totalStates)
		return True

	new_states = find_all_valid(puzzle)
	totalStates += len(new_states)
	for state in new_states:
		if notSeen(state):
			markedSeen(state)
			if brute_solver(state):
				return True
	return False

def brute_solver2(puzzle):
	queue = deque([puzzle])
	totalStates = 0

	while len(queue) > 0:
		state = queue.popleft()

		if notSeen(state):
			markedSeen(state)
		else:
			continue

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


def markTheseBlack(puzzle, toBeMarked, notThese):
	for coords in toBeMarked:
		if coords in notThese:
			continue
		puzzle.markBlack(coords[0], coords[1])

"""
	For marking the most restricted values, we rely on two Forced Actions and
	the limitations of the puzzle configuration, as discussed below.
	
	The Configuration Constraints are derived from all the Rules, which	disallow
	certain puzzle configurations from being possible. If a Puzzle has an 
	invalid configuration, then the Puzzle can not be solved.
	
	Configuration Constraints:
		- No more than three like-numbers may be adjacent in a row (xor column).
			- Otherwise Rule Two and Rule One are broken.
			
		- No more than four like-numbers may be touching (in a combination of
		both rows and columns).
			- Otherwise Rule Three might be broken (an isolated White tile in 
			the center), and Rules One and Two would be broken for the same
			reason as the first configuration constraint.
			
		- Only one adjacent group is possible for each number on any given row
		(xor column).
			- Otherwise Rule One and Rule Two would be broken.
			
	From these puzzle Configuration Constraints, we can always safely make two 
	Forced Actions. If the Forced Actions result in an invalid Puzzle state that
	would break any of the Rules, then the Puzzle is not solvable.
	
	Forced Actions:
		- If three like-numbers are adjacent, the middle MUST be White, and 
		all other like-number tiles on that row (xor column) MUST be Black.
			
		- If two like-numbers are adjacent, all other like-numbers on that row
		(xor column) MUST be Black, and the two adjacent MUST be oppositely 
		assigned.
		
		- If a tile has more than one adjacent neighbor on its row and column,
		then it is always safe to assume that first tile is Black. In the case
		like below:
				
				X X X X
				X 5 5 X
				X 5 5 X
				X X X X						Figure 1.
		
		for any arbitrary sized board where a configuration of a two-by-two
		block of numbers appears. This is only true because we first check for
		explicit Black neighbors first.  If we have no Black neighbors, but we
		have two (or more) unassigned adjacent neighbors, then we have to be
		Black.  This is also because in puzzles like the one below:

				X X X X X
				X 1 1 1 X
				X 1 1 X X
				X 1 X X X
				X X X X X					Figure 2.
				
		when our algorithm first finds pairs of adjacent tiles, we immediately
		mark everything else in that row (xor column) as Black.  This guarantees
		that any arbitrary groups of similar numbers, so long as they are
		conforming to the Puzzle Configuration Constraints, and because of how
		the puzzle is traversed when marking pairs, the third element of each
		"branch" will already be Black. This forces the element next to us to
		be White anyway, and us Black. This leap in logic is necessary,
		because it saves us from having to explicitly check for Figure 2 and
		have foregone solving Figure 1.  We can't solve Figure 1 until we are
		sure that it is not a subset of Figure 2. Since we know that Figure 2
		would already be partially-solved, we can treat all examples of Figure 1
		indiscriminately.
				

	possibles	An array of possible tiles that need consideration for being
				marked black. The array looks as follows:

					[2][rows][rows][x][2]

				Where the first array marks if the coordinate is from a vertical
				group, or a horizontal group.  The second nested array is the
				particular row of the horizontal group (or column of a vertical
				group). The third array groups the coordinates into the number
				of that coordinate. This ensures that we are only looking at
				coordinates for like-numbers. The fourth array is the number of
				like numbers in that group. The final nested array gives the
				row and column of the coordinate of the tile that needs to be
				considered for marking Black. Note, that the third nested array
				assumes that the coordinates are given in ascending order
				(closest to the origin first).
"""

def findMostRestricted(puzzle, possibles, relaxed):

	# The selector is for controlling if we are scanning DOWN a COLUMN or
	# ACROSS a ROW (0 is ROW, and 1 is COLUMN).
	for selector in range(0, 2):

		# For all in each row or column
		for possible in range(0, puzzle.rows):
			
			# For all in each particular row or column
			for nums in range(0, puzzle.rows):
				similarNums = len(possibles[selector][possible][nums])
				for i in range(0, similarNums):
					coords = possibles[selector][possible][nums][i]

					# This may have been marked Black already from a previous
					# operation. If so, then skip it.
					if puzzle.isBlack(coords[0], coords[1]):
						continue

					# If this tile is already marked adjacent, see
					# if maybe we can resolve it
					if puzzle.isMarkedAdjacent(coords[0], coords[1]):

						# Check around us for neighbors (pretty ugly...)
						blackNeighbor = False
						adjacentNeighbors = 0
						explicitWhiteNeighbor = False
						above = coords[0] - 1
						below = coords[0] + 1
						left = coords[1] - 1
						right = coords[1] + 1
						if above >= 0 and puzzle.getNum(above, coords[1]) - 1 == nums:
							if puzzle.isBlack(above, coords[1]):
								blackNeighbor = True
							elif puzzle.isExplicitlyMarkedWhite(above, coords[1]):
								explicitWhiteNeighbor = True
							elif puzzle.isMarkedAdjacent(above, coords[1]):
								adjacentNeighbors += 1
						if below < puzzle.rows and puzzle.getNum(below, coords[1]) - 1 == nums:
							if puzzle.isBlack(below, coords[1]):
								blackNeighbor = True
							elif puzzle.isExplicitlyMarkedWhite(below, coords[1]):
								explicitWhiteNeighbor = True
							elif puzzle.isMarkedAdjacent(below, coords[1]):
								adjacentNeighbors += 1
						if left >= 0 and puzzle.getNum(coords[0], left) - 1 == nums:
							if puzzle.isBlack(coords[0], left):
								blackNeighbor = True
							elif puzzle.isExplicitlyMarkedWhite(coords[0], left):
								explicitWhiteNeighbor = True
							elif puzzle.isMarkedAdjacent(coords[0], left):
								adjacentNeighbors += 1
						if right < puzzle.rows and puzzle.getNum(coords[0], right) - 1 == nums:
							if puzzle.isBlack(coords[0], right):
								blackNeighbor = True
							elif puzzle.isExplicitlyMarkedWhite(coords[0], right):
								explicitWhiteNeighbor = True
							elif puzzle.isMarkedAdjacent(coords[0], right):
								adjacentNeighbors += 1

						# If we have any Black neighbors, we MUST be White to
						# conform to Rule Two. We are also free to mark all
						# similar numbers in this group Black (to conform with
						# Rule 1).
						if blackNeighbor:
							markTheseBlack(puzzle,
										   possibles[selector][possible][nums],
										   [coords])
							removeFromPossibles(possibles,
												possibles[selector][possible][nums],
												[])
							puzzle.markExplicitlyWhite(coords[0], coords[1])
							break

						# If we have any (explicitly) White neighbors, we MUST
						# be Black to conform to Rule Two. We are also free to
						# mark all similarly unassigned numbers in this group
						# Black.
						elif explicitWhiteNeighbor:
							markTheseBlack(puzzle,
										   possibles[selector][possible][nums],
										   [])
							removeFromPossibles(possibles,
												possibles[selector][possible][nums],
												[])
							break

						# If we have more than one adjacent neighbor, it is
						# always safe to assume that we are Black (as explained
						# in great length in the function documentation).
						# However, we are NOT free to mark anything else.
						# We will just be lazy and have the next call to this
						# resolve the remaining parts (much easier).
						elif adjacentNeighbors > 1:
							puzzle.markBlack(coords[0], coords[1])
							removeFromPossibles(possibles, [coords], [])
							break
						
					# Otherwise we are processing this for the first time, and
					# need to search for adjacent neighbors
					else:

						# We need to find the first adjacent group
						if i + 1 < similarNums:
	
							# The coordinates are given in ascending order, so we
							# can assume that the very next coordinate is the next
							# closest like-number in our group.
							nextCoords = possibles[selector][possible][nums][i + 1]
							if (selector == 0 and coords[1] + 1 == nextCoords[1]) \
							or (selector == 1 and coords[0] + 1 == nextCoords[0]):
	
								# Otherwise we are seeing this pair for the first
								# time
								puzzle.markAdjacent(coords[0], coords[1])
								puzzle.markAdjacent(nextCoords[0], nextCoords[1])
	
								# mark everyone, but this adjacent group, black
								markTheseBlack(puzzle,
											   possibles[selector][possible][nums],
											   [coords, nextCoords])
								removeFromPossibles(possibles,
													possibles[selector][possible][nums],
													[coords, nextCoords])
	
								# We don't need to keep processing the rest of this
								# group of numbers within this selector since we marked
								# everything already
								break

	return possibles

def removeFromPossibles(possibles, removeThese, notThese):
	removeThese = copy.deepcopy(removeThese)
	for selector in possibles:
		for possible in selector:
			for nums in possible:
				for element in removeThese:
					if element in nums and element not in notThese:
						nums.remove(element)
	return possibles

def sum(li):
	s = 0
	for l in li:
		if isinstance(l, list):
			s += sum(l)
		elif l:
			s += 1
	return s

def MRVSolver(puzzle, possible):
	global totalStates
	if sum(possible) == 0:
		return
	if not puzzle.isValid():
		return
	totalStates += 1
	if notSeen(puzzle):
		markedSeen(puzzle)
		MRVSolver(puzzle, findMostRestricted(puzzle, possible, False))
	# If we have already seen this puzzle before, that implies that we have no
	# forced moves to make.  Instead, we are free to make a move that
	# isn't as forced, but that makes the most logical sense
	else:
		MRVSolver(puzzle, findMostRestricted(puzzle, possible, True))

"""
	Checks for all tiles that must conform to Rule One (the most
	restrictive Rule)
"""
def findAllPossible(puzzle):
	board = puzzle.getPuzzle()
	rows = puzzle.getRows()

	# First array denotes a col group or a row group
	# Second array groups possibles into their col/row group
	possibles = [[[[] for x in range(rows)] for y in range(rows)] for z in range(2)]
	valSeenC = [0] * rows
	valSeenR = [0] * rows
	for row in range(0, rows):
		for col in range(0, rows):

			# Find possibles in this row
			val = board[row][col] - 1
			valSeenR[val] += 1

			# We only need to add all like-numbers once
			if valSeenR[val] == 2:
				for innerCol in range(0, rows):
					if board[row][innerCol] - 1 == val:
						possibles[0][row][val].append([row, innerCol])

			# Find possibles in this col
			val = board[col][row] - 1
			valSeenC[val] += 1
			if valSeenC[val] == 2:
				for innerCol in range(0, rows):
					if board[innerCol][row] - 1 == val:
						possibles[1][row][val].append([innerCol, row])
		valSeenC = [0] * rows
		valSeenR = [0] * rows
	return possibles


def smart_solver(puzzle):
	print("Finding Solution...")
	if puzzle.isSolved():
		return True
	MRVSolver(puzzle, findAllPossible(puzzle))
	if puzzle.isSolved():
		print("Final Solution State")
		print_puzzle(puzzle)
		print_states_gen(totalStates)
	else:
		print("No Solution")



def print_puzzle(puzzle):
	board = puzzle.getPuzzle()
	marked = puzzle.markedPuzzle
	rows = puzzle.getRows()
	for row in range(0, rows):
		for col in range(0, rows):
			if marked[row][col] == puzzle._BLACK:
				print("B", end="")
			print(str(board[row][col]), end=" ")
		print()

# Seen List
seenList = []
seenDict = {}
totalStates = 0

if __name__ == "__main__":

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

	# Brute-Force Solver
#	solve_hitori(puzzle1, 1)
#	print()
#	solve_hitori(puzzle2, 1)
#	print()
#	solve_hitori(puzzle3, 1)
	print()
	solve_hitori(puzzle4, 1)
#	cProfile.run('solve_hitori(puzzle4, 0)', 'output.txt')
#	p = pstats.Stats('output.txt')
#	p.sort_stats('time')
#	p.print_stats()


	# Smart solver
	# solve_hitori(puzzle1, 1)

