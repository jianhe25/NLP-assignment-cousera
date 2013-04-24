import json
import sys
import array
from collections import defaultdict
from collections import namedtuple
from sets import Set

terminalSet = Set()

class DerivedTerm:
	
	"""derived terms of one nonterm"""
	def __init__(self, count, y=None, z=None):
		self.data = []
		self.count = count
		if (y != None):
			self.data.append(y)
		if (z != None):
			self.data.append(z)

class Record:
	def __init__(self):
		self.derivedTerms = []
		self.self_count = 0

	def append(self, derivedTerm):
		self.derivedTerms.append(derivedTerm)

def loadCountFile(count_file, rule):
	global terminalSet
	x = ""
	y = ""
	z = ""
	printCount = 0

	for line in open(count_file):
		parts = line.split(" ")
		count = int(parts[0])
		attribute = parts[1]
		if (attribute == "NONTERMINAL"):
			x = parts[2].strip()
			rule[x].self_count = count
		if (attribute == "UNARYRULE"):
			x, y = parts[2], parts[3].strip()
			rule[x].append(DerivedTerm(count, y))
			terminalSet.add(y)
		if (attribute == "BINARYRULE"):
			x, y, z = parts[2], parts[3], parts[4].strip()
			rule[x].append(DerivedTerm(count, y, z))
"""
	for x in rule:
		print x, rule[x].self_count
		printCount = 0
		for derivedTerm in rule[x].derivedTerms:
			printCount += 1
			if (printCount < 5):
				print len(derivedTerm.data), derivedTerm.count
"""

def findTerminal(record, terminal):
	for derivedTerm in record.derivedTerms:
		if len(derivedTerm.data) == 1 and derivedTerm.data[0] == terminal:
			return derivedTerm.count
	return 0

class State(namedtuple('State', ['probability', 'splitPos', 'root', 'leftChild', 'rightChild', 'l', 'r'])):
	def __new__(self, probability=0, splitPos=0, root=0, leftChild=0, rightChild=0, l=0, r=0):
		return super(State, self).__new__(self, probability, splitPos, root, leftChild, rightChild, l, r)

	def __str__(self):
		return str(self.root) + "\t" + str(self.l) + "\t" + str(self.r) + '\t' + str(self.probability) + '\t' + str(self.leftChild) + '\t' + str(self.rightChild)

depth = 0
def dumpTree(state, l, r, words, dp):
	global depth
	parse_tree = []

	x = state.root
	y = state.leftChild
	z = state.rightChild
	mid = state.splitPos
	parse_tree.append(x) # parse_tree[0] indicate root symbal

	if l == r:
		parse_tree.append(words[l])
		return parse_tree

	left_tree = dumpTree(dp[l][mid][y], l, mid, words, dp)
	right_tree = dumpTree(dp[mid+1][r][z], mid+1, r, words, dp)
	parse_tree.append(left_tree)
	parse_tree.append(right_tree)

	return parse_tree

def parseSentence(line, rule):
	""" parseSentence use dynamic programming to find max(arg-p) """
	global terminalSet

	words = line.split(" ")
	n = len(words)
	dp = [[defaultdict(State) for i in xrange(n)] for i in xrange(n)]
	
	assert '?' in terminalSet
	for i in range(n):
		words[i] = words[i].strip()
		if words[i] not in terminalSet:
			words[i] = "_RARE_"
#		print "====================================initialize ", i, words[i], "=================================="
		for x in rule:
			probability = float(findTerminal(rule[x], words[i])) / rule[x].self_count;
			dp[i][i][x] = State(probability, i, x, -1, -1, i, i)
#			if (dp[i][i][x].probability > 0):
#				print dp[i][i][x]

	for length in range(2, n+1):
		for start in range(n-length+1):
			end = start + length - 1;
			for x in rule:
				for derivedTerm in rule[x].derivedTerms:
					if (len(derivedTerm.data) == 1): 
						continue
					y = derivedTerm.data[0]
					z = derivedTerm.data[1]
					state = dp[start][end][x]
					for mid in range(start, end):
						probability = float(derivedTerm.count) / rule[x].self_count * dp[start][mid][y].probability * dp[mid+1][end][z].probability;
						if probability > state.probability:
							state = State(probability, mid, x, y, z, start, end)
					dp[start][end][x] = state
#					if (state.probability > 0):
#						print state
	
	START_SYMBAL = "SBARQ"
	return dumpTree(dp[0][n-1][START_SYMBAL], 0, n-1, words, dp)
"""
	bestState = State()
	for x in rule:
		if dp[0][n-1][x].probability > bestState.probability:
			bestState = dp[0][n-1][x]
"""

def parseData(input_file, rule):
	for line in open(input_file):
		parse_tree = parseSentence(line, rule)
		print json.dumps(parse_tree)

def main(count_file, input_file):
	rule = defaultdict(Record)
	loadCountFile(count_file, rule);
	parseData(input_file, rule)

def usage():
	print "usage : parser [count] [data] > result"

if __name__ == "__main__":
	if len(sys.argv) != 3:
		usage()
		sys.exit(1)
	main(sys.argv[1], sys.argv[2])


