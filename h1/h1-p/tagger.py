from collections import defaultdict
import sys

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

def emit_tag(raw_data_file, output_file):
	for line in raw_data_file:
		word = line.strip()
		if word == "":
			output_file.write("\n")
			continue
		
		is_rare = True 
		for tag in all_tags:
			if emission_counts[(word, tag)] != 0:
				is_rare = False 
				break
		if is_rare:
			new_word = "_RARE_" 
		else:
			new_word = word
		max_counts = 0
		max_tag = "$"
		for tag in all_tags:
			tag_count = ngram_counts[0][tag]
			assert tag_count > 0, "Expecting tag_count > 2."
			#assert emission_counts[(word, tag)] == 0 or emission_counts[(word, tag)] >= 5, "emission_counts is larger than 5, or equals to 0, while em = %d" % emission_counts[(word, tag)]
			#replace word to _RARE_ if not found in train_counts

			if float(emission_counts[(new_word, tag)]) / tag_count > max_counts:
				max_tag = tag
				max_counts = float(emission_counts[(new_word, tag)]) / tag_count
		
		assert max_tag != "$", "max_tag not found"
		output_file.write(word + " " + max_tag + "\n")

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

