from solver import Puzzle
from solver import clearSeen
from solver import notSeen
from solver import markedSeen

def test_isBlack():
	p = Puzzle( [["B2", "1"], ["1", "1"]], True)
	assert(p.isBlack(0, 0))
def test_isWhite():
	p = Puzzle( [["B2", "1"], ["1", "1"]], True)
	assert(p.isWhite(0, 1))
def test_getRows():
	p = Puzzle( [["B2", "1"], ["1", "1"]], True)
	assert(p.getRows() == 2)
def test_markBlack():
	p = Puzzle( [["B2", "1"], ["1", "1"]], True)
	p.markBlack(1, 1)
	assert(p.isBlack(1, 1))
def test_getMarkedNum():
	p = Puzzle( [["B2", "1"], ["1", "1"]], True)
	assert(int(p.getNum(0, 0)) == 2)
def test_getUnmarkedNum():
	p = Puzzle( [["B2", "1"], ["1", "1"]], True)
	assert(int(p.getNum(0, 1)) == 1)
def test_conformsToRuleTwoUnmarked():
	p = Puzzle( [["2", "1"], ["1", "1"]], False)
	assert(p.conformsToRuleTwo())
def test_conformsToRuleTwoSingleMark():
	p = Puzzle( [["B2", "1"], ["1", "1"]], True)
	assert(p.conformsToRuleTwo())
def test_conformsToRuleTwoNonAdjacentMarks():
	p = Puzzle( [["B2", "1"], ["1", "B1"]], True)
	assert(p.conformsToRuleTwo())
def test_conformsToRuleTwoVerticallyAdjacentMarks():
	p = Puzzle( [["B2", "1"], ["B1", "1"]], True)
	assert(not p.conformsToRuleTwo())
def test_conformsToRuleTwoHorizontallyAdjacentMarks():
	p = Puzzle( [["B2", "B1"], ["1", "1"]], True)
	assert(not p.conformsToRuleTwo())
def test_conformsToRuleThreeEmpty():
	p = Puzzle( [["2", "1"], ["1", "1"]], False)
	assert(p.conformsToRuleThree())
def test_conformsToRuleThreeSingleMarked():
	p = Puzzle( [["B2", "1"], ["1", "1"]], True)
	assert(p.conformsToRuleThree())
def test_conformsToRuleThreeDiagonallyDivided():
	p = Puzzle( [["B2", "1"], ["1", "B1"]], True)
	assert(not p.conformsToRuleThree())
def test_conformsToRuleThreeIsolatedWhiteTile():
	p = Puzzle( [["2", "1", "3"],
				 ["1", "B1", "2"],
				 ["B3", "2", "B1"]], True)
	assert(not p.conformsToRuleThree())
def test_conformsToRuleOneNoneMarked():
	p = Puzzle( [["2", "1"], ["1", "1"]], False)
	assert(not p.conformsToRuleOne())
def test_conformsToRuleOneMultipleMarked():
	p = Puzzle( [["2", "B1"], ["B1", "1"]], False)
	assert(p.conformsToRuleOne())
def test_SeenList():
	p = Puzzle( [["2", "1"], ["1", "1"]], False)
	p2 = Puzzle( [["2", "1"], ["1", "1"]], False)
	clearSeen()
	assert(notSeen(p))
	markedSeen(p)
	assert(not notSeen(p))
	assert(not notSeen(p2))

# Execute Tests
test_isBlack()
test_isWhite()
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