import sys
from trainEM_1 import notNULL
from trainEM_1 import strip
from itertools import izip
from collections import defaultdict

translate = defaultdict(lambda : defaultdict(float))

def load_count(count_file):
	for line in open(count_file):
		parts = line.split(" ")
		translate[ parts[0] ][ parts[1] ] = float(parts[2])

def getMaxAlignment(fWord, english):
	maxProbability = 0
	maxJ = -1
	for j in xrange(len(english)):
		if translate[fWord][english[j]] > maxProbability:
			maxProbability = translate[fWord][english[j]]
			maxJ = j

	assert maxJ != -1
	return maxJ

def main(source_file, target_file):
	lineNo = 0
	for english, french in izip(open(source_file), open(target_file)):
		lineNo += 1
		english = filter(notNULL, map(strip, english.split(" ")))
		french = filter(notNULL, map(strip, french.split(" ")))
		english.insert(0, "NULL")
		for i in xrange(len(french)):
			alignment = getMaxAlignment(french[i], english)
			print lineNo, alignment, i+1

def usage():
	print "python align.py [source_file] [target_file] [count_file] > [alignment_file]"

if __name__ == "__main__":
	if len(sys.argv) != 4:
		usage()
		sys.exit(1)

	load_count(sys.argv[3])
	main(sys.argv[1], sys.argv[2])

