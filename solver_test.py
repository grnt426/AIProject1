from solver import Puzzle
from solver import clearSeen
from solver import notSeen
from solver import markedSeen

def test_getRows():
	p = Puzzle( ((2, 1), (1, 1)), True)
	assert(p.getRows() == 2)
def test_markBlack():
	p = Puzzle( ((2, 1), (1, 1)), True)
	p.markBlack(1, 1)
	assert(p.isBlack(1, 1))
def test_getMarkedNum():
	p = Puzzle( ((2, 1), (1, 1)), True)
	assert(p.getNum(0, 0) == 2)
def test_getUnmarkedNum():
	p = Puzzle( ((2, 1), (1, 1)), True)
	assert(int(p.getNum(0, 1)) == 1)
def test_conformsToRuleTwoUnmarked():
	p = Puzzle( ((2, 1), (1, 1)), False)
	assert(p.conformsToRuleTwo())
def test_conformsToRuleTwoSingleMark():
	p = Puzzle( ((2, 1), (1, 1)), True)
	p.markBlack(1, 1)
	assert(p.conformsToRuleTwo())
def test_conformsToRuleTwoNonAdjacentMarks():
	p = Puzzle( ((2, 1), (1, 1)), True)
	p.markBlack(1, 1)
	p.markBlack(0, 0)
	assert(p.conformsToRuleTwo())
def test_conformsToRuleTwoVerticallyAdjacentMarks():
	p = Puzzle( ((2, 1), (1, 1)), True)
	p.markBlack(1, 1)
	p.markBlack(0, 1)
	assert(not p.conformsToRuleTwo())
def test_conformsToRuleTwoHorizontallyAdjacentMarks():
	p = Puzzle( ((2, 1), (1, 1)), True)
	p.markBlack(0, 0)
	p.markBlack(0, 1)
	assert(not p.conformsToRuleTwo())
def test_conformsToRuleThreeEmpty():
	p = Puzzle( ((2, 1), (1, 1)), False)
	assert(p.conformsToRuleThree())
def test_conformsToRuleThreeSingleMarked():
	p = Puzzle( ((2, 1), (1, 1)), True)
	p.markBlack(0, 0)
	assert(p.conformsToRuleThree())
def test_conformsToRuleThreeDiagonallyDivided():
	p = Puzzle( ((2, 1), (1, 1)), True)
	p.markBlack(0, 0)
	p.markBlack(1, 1)
	assert(not p.conformsToRuleThree())
def test_conformsToRuleThreeIsolatedWhiteTile():
	p = Puzzle( ((2, 1, 3),
				 (1, 1, 2),
				 (3, 2, 1)), True)
	p.markBlack(1, 1)
	p.markBlack(2, 0)
	p.markBlack(2, 2)
	assert(not p.conformsToRuleThree())
def test_conformsToRuleOneNoneMarked():
	p = Puzzle( ((2, 1), (1, 1)), False)
	assert(not p.conformsToRuleOne())
def test_conformsToRuleOneMultipleMarked():
	p = Puzzle( ((2, 1), (1, 1)), False)
	p.markBlack(1, 1)
	assert(p.conformsToRuleOne())
def test_SeenList():
	p = Puzzle( ((2, 1), (1, 1)), False)
	p2 = Puzzle( ((2, 1), (1, 1)), False)
	clearSeen()
	assert(notSeen(p))
	markedSeen(p)
	assert(not notSeen(p))
	assert(not notSeen(p2))

# Execute Tests
test_getRows()
test_markBlack()
test_getMarkedNum()
test_getUnmarkedNum()
test_conformsToRuleTwoUnmarked()
test_conformsToRuleTwoSingleMark()
test_conformsToRuleTwoNonAdjacentMarks()
test_conformsToRuleTwoVerticallyAdjacentMarks()
test_conformsToRuleTwoHorizontallyAdjacentMarks()
test_conformsToRuleThreeEmpty()
test_conformsToRuleThreeSingleMarked()
test_conformsToRuleThreeDiagonallyDivided()
test_conformsToRuleThreeIsolatedWhiteTile()
test_conformsToRuleOneNoneMarked()
test_conformsToRuleOneMultipleMarked()
test_SeenList()