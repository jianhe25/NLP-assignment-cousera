import json
import sys

def loadCountFile(count_file):
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
			rule[x].count
		if (attribute == "UNARYRULE"):
			x, y = parts[2], parts[3].strip()
			rule[x].push_back(Record(y))
		if (attribute == "BINARYRULE"):
			x, y, z = parts[2], parts[3], parts[4].strip()
		
def main(argv):
	loadCountFile("parse_train.counts.out");

def usage():
	print "usage : parser data > result"

if __name__ == "__main__":
	if len(sys.argv) != 2:
		usage()
		sys.exit(1)
	main(sys.argv[1])


