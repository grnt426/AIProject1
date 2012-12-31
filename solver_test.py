__author__ = 'grnt426'

from solver import Puzzle

def test_isBlack():
	p = Puzzle( [["B2", "1"], ["1", "1"]])
	assert(p.isBlack(0, 0))
def test_isWhite():
	p = Puzzle( [["B2", "1"], ["1", "1"]])
	assert(p.isWhite(0, 1))
def test_getRows():
	p = Puzzle( [["B2", "1"], ["1", "1"]])
	assert(p.getRows() == 2)
def test_markBlack():
	p = Puzzle( [["B2", "1"], ["1", "1"]])
	p.markBlack(1, 1)
	assert(p.isBlack(1, 1))
def test_getMarkedNum():
	p = Puzzle( [["B2", "1"], ["1", "1"]])
	assert(int(p.getNum(0, 0)) == 2)
def test_getUnmarkedNum():
	p = Puzzle( [["B2", "1"], ["1", "1"]])
	assert(int(p.getNum(0, 1)) == 1)
def test_conformsToRuleTwoUnmarked():
	p = Puzzle( [["2", "1"], ["1", "1"]])
	assert(p.conformsToRuleTwo())
def test_conformsToRuleTwoSingleMark():
	p = Puzzle( [["B2", "1"], ["1", "1"]])
	assert(p.conformsToRuleTwo())
def test_conformsToRuleTwoNonAdjacentMarks():
	p = Puzzle( [["B2", "1"], ["1", "B1"]])
	assert(p.conformsToRuleTwo())
def test_conformsToRuleTwoVerticallyAdjacentMarks():
	p = Puzzle( [["B2", "1"], ["B1", "1"]])
	assert(not p.conformsToRuleTwo())
def test_conformsToRuleTwoHorizontallyAdjacentMarks():
	p = Puzzle( [["B2", "B1"], ["1", "1"]])
	assert(not p.conformsToRuleTwo())


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