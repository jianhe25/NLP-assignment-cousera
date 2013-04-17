from collections import defaultdict
import sys
import math


INF = 1e10
max_gram = 3
emission_counts = defaultdict(int)
ngram_counts = [defaultdict(int) for i in xrange(max_gram)]
all_tags = set()

def read_counts(train_counts_file):
	for line in train_counts_file:
		parts = line.strip().split(" ")
		count = int(parts[0])
		if parts[1] == "WORDTAG":
			ne_tag = parts[2]
			word = parts[3]
			emission_counts[(word, ne_tag)] = count
		elif parts[1].endswith("GRAM"):
			gram_num = int(parts[1].replace("-GRAM",""))
			if gram_num == 1:
				all_tags.add(parts[2])
				ngram_counts[gram_num-1][parts[2]] = count
			else:
				ngram = tuple(parts[2:])
				ngram_counts[gram_num-1][ngram] = count

def sentence_iterator(raw_data_file):
	current_sentence = []
	for line in raw_data_file:
		word = line.strip()
		if word:
			current_sentence.append(word)
		else:
			if current_sentence:
				yield current_sentence
				current_sentence = []
			else:
				sys.stderr.write("Warning: empty line\n")
				raise StopIteration
	if current_sentence:
		yield current_sentence

class Record:
	def __init__(self, value = 0.0, prev = ""):
		self.value = value
		self.prev = prev 

def isNumeric(word):
	for letter in word:
		if (letter <= '9' and letter >= '0'):
			return True
	return False

def isAllCap(word):
	for letter in word:
		if not (letter <= 'Z' and letter >= 'A'):
			return False
	return True

def isLastCap(word):
	return word[-1] <= 'Z' and word[-1] >= 'A'

def update(tag1, tag2, word, old, new, round):
	if (tag1, tag2) not in old:
		return

	is_rare = True 
	for tag in all_tags:
		if emission_counts[(word, tag)] != 0:
			is_rare = False 
			break
	
	if is_rare:
		if isNumeric(word):
			new_word = "_NUMERIC_"
		elif isAllCap(word):
			new_word = "_ALLCAP_"
		elif isLastCap(word):
			new_word = "_LASTCAP_"
		else:
			new_word = "_RARE_" 
	else:
		new_word = word

	for tag in all_tags:
		if tag == "*" or (tag == "STOP" and word != "$$$$"): # tag Cannot be "*"
			continue
		trigram = (tag1, tag2, tag)
		bigram = (tag1, tag2)
		value = old[(tag1, tag2)].value + math.log(ngram_counts[3-1][trigram]) - math.log(ngram_counts[2-1][bigram]);
		adaptive_counts = emission_counts[(new_word, tag)] #if (emission_counts[(new_word,tag)] > 0) else emission_counts[("_RARE_", tag)]
		if tag != "STOP":
			if adaptive_counts == 0:
				value = -INF;
			else:
				value += math.log(adaptive_counts) - math.log(ngram_counts[0][tag])
		
		if value > -INF and ((tag2, tag) not in new or value > new[(tag2, tag)].value):
			new[(tag2, tag)].value = value 
			new[(tag2, tag)].prev = tag1
			#print "insert ", tag2, tag, " value = ",value, tag1 

def emit_tag(raw_data_file, output_file):
	all_tags.add("*")
	all_tags.add("STOP")
	for sentence in sentence_iterator(raw_data_file):
		n = len(sentence)
		dp = [defaultdict(Record) for i in xrange(n+2)]
		dp[0][("*","*")] = Record(math.log(1.0), "$")
		sentence.append("$$$$")
		for i in xrange(n + 1):
			word = sentence[i]
			for tag1 in all_tags:
				for tag2 in all_tags:
					update(tag1, tag2, word, dp[i], dp[i+1], i)
		
		max_tag = "!"
		max_probability = -INF 
		for tag in all_tags:
			if (tag, "STOP") in dp[n+1]:
				if dp[n+1][(tag, "STOP")].value > max_probability:
					max_tag = tag
					max_probability = dp[n+1][(tag, "STOP")].value

		emit_tags = range(n)
		tag1 = max_tag
		tag2 = "STOP"
		for i in xrange(n+1, 1, -1):
			emit_tags[i - 2] = tag1
			assert (tag1, tag2) in dp[i], "round = %d, tag1 = %s, tag2 = %s\n" % (i, tag1, tag2)
			oldTag1 = tag1;
			tag1 = dp[i][(tag1, tag2)].prev
			tag2 = oldTag1

		for i in xrange(n):
			output_file.write(sentence[i] + " " + emit_tags[i] + "\n")
		output_file.write("\n")

def usage():
	print """
	python tagger.py [raw_data] (train_counts) > [tagged_file]
		Read in a untagged input and produce tagged filed, train_counts is optional
	"""

if __name__ == "__main__":

	if len(sys.argv) < 2 or len(sys.argv) > 3 :
		usage()
		sys.exit(2)

	train_counts_file_name = "gene.counts"
	if len(sys.argv) == 3:
		train_counts_file_name = sys.argv[2]	

	try:
		train_counts_file = file(train_counts_file_name, "r")
		raw_data_file = file(sys.argv[1], "r")
	except IOError:
		sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
		sys.exit(1)
	
	read_counts(train_counts_file)
	emit_tag(raw_data_file, sys.stdout);

