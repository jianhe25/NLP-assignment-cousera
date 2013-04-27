import sys
from itertools import izip
from collections import defaultdict

EM_ITERATE_STEPS = 7
nCount = defaultdict(set)
count2d = defaultdict( lambda : defaultdict(float) )
t = defaultdict( lambda : defaultdict(float) )
count = defaultdict(float)

def train(english, french):
	global t, count2d, count
	english.insert(0, "NULL") # represent position zero

	delta = [ [0.0 for j in xrange(len(english))] for i in xrange(len(french)) ]
	for i in xrange( len(french) ):
		sumT = 0.0
		for j in xrange( len(english) ):
			sumT += t[ french[i] ][ english[j] ]
		for j in xrange( len(english) ):
			delta[i][j] = t[ french[i] ][ english[j] ] / sumT
	
	for i in xrange( len(french) ):
		for j in xrange( len(english) ):
			count2d[ french[i] ][ english[j] ] += delta[i][j]
			count[ english[j] ] += delta[i][j]

def strip(x):
	return x.strip()

def notNULL(x):
	return x != ""

def initializeParameters(sourceCorpus, targetCorpus):
	global nCount, t
	for english, french in zip(sourceCorpus, targetCorpus):
		englishList = filter(notNULL, map(strip, english.split(" ")))
		frenchList = filter(notNULL, map(strip, french.split(" ")))
		englishList.insert(0, "NULL")
		for eWord in englishList:
			for fWord in frenchList:
				nCount[eWord].add(fWord)
	
	for eWord in nCount:
		for fWord in nCount[eWord]:
			t[fWord][eWord] = 1.0 / len(nCount[eWord])
"""
	print "fWord.size() = ", len(t)
	entry_number = 0
	for fWord in t:
		entry_number += len(t[fWord])
	print "entry_number = ", entry_number
"""

def outputResult():
	global count2d
	for fWord in count2d:
		for eWord in count2d[fWord]:
			print fWord, eWord, count2d[fWord][eWord]
	
def main(source_file, target_file):
	global count2d, count
	sourceCorpus = [line for line in open(source_file)]
	targetCorpus = [line for line in open(target_file)]
	initializeParameters(sourceCorpus, targetCorpus)

	for emStep in xrange(EM_ITERATE_STEPS):
		count2d.clear()
		count.clear()
		for source_line, target_line in zip(sourceCorpus, targetCorpus):
			train(filter(notNULL, map(strip, source_line.split(" "))), 
				  filter(notNULL, map(strip, target_line.split(" "))))
		
		for fWord in count2d:
			for eWord in count2d[fWord]:
				assert eWord in count
				t[fWord][eWord] = count2d[fWord][eWord] / count[eWord]

	outputResult()

def usage():
	print "trainEM_1 [source_file] [target_file] > [count_file]"

if __name__ == "__main__":
	if len(sys.argv) != 3:
		usage()
		sys.exit(1)
	
	main(sys.argv[1], sys.argv[2])

