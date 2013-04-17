import sys
import math
from collections import defaultdict

emission_counts = defaultdict(int)

def count_words(input_file):
	line = input_file.readline()
	while line:
		line = line.strip()
		if line:
			fields = line.split(" ")
			word = fields[0]
			emission_counts[word] += 1;
		line = input_file.readline();

def isNumeric(word):
	for letter in word:
		if letter <= '9' and letter >= '0':
			return True
	return False

def isAllCap(word):
	for letter in word:
		if not (letter <= 'Z' and letter >= 'A'):
			return False
	return True

def isLastCap(word):
	return word[-1] <= 'Z' and word[-1] >= 'A'

def write_counts(input_file, output_file):
	line = input_file.readline()
	while line:
		line = line.strip()
		if line:
			fields = line.split(" ")
			word = fields[0]
			if emission_counts[word] < 5:
				if isNumeric(word):
					fields[0] = "_NUMERIC_"
				elif isAllCap(word):
					fields[0] = "_ALLCAP_"
				elif isLastCap(word):
					fields[0] = "_LASTCAP_"
				else:
					fields[0] = "_RARE_"
			output_line = " ".join(fields)
		else:
			output_line = line
		output_file.write(output_line + '\n')
		line = input_file.readline()

def usage():
		print """
		python data_normlizer [input_file] > [output_file]
		Read in a gene tagged training input file and replace word which counts less than 5 with _RARE_
		"""

if __name__ == "__main__":
	
	if len(sys.argv) != 2:
		usage()
		sys.exit(2)
	
	try:
		input = file(sys.argv[1], "r")
	except IOError:
		sys.stderr.write("ERROR: Cannot open inputfile %s.\n" % arg)
		sys.exit(1)
	
	count_words(input);

	#Reopen input_file to rewrite it 
	try:
		input = file(sys.argv[1], "r")
	except IOError:
		sys.stderr.write("ERROR: Cannot open inputfile %s.\n" % arg)
		sys.exit(1)
	write_counts(input, sys.stdout);

