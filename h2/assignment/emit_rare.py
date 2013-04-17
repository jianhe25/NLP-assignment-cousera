#! /usr/bin/python

import json, sys

def count(tree, wordCount):
	if isinstance(tree, unicode):
		if tree not in wordCount:
			wordCount[tree] = 1
		else:
			wordCount[tree] += 1
	elif len(tree) == 3:
		count(tree[1], wordCount)
		count(tree[2], wordCount)
	elif len(tree) == 2:
		count(tree[1], wordCount)
	
def change(tree, wordCount):
	
	if len(tree) == 3:
		change(tree[1], wordCount)
		change(tree[2], wordCount)
	elif len(tree) == 2:
		if isinstance(tree[1], unicode):
			if (wordCount[tree[1]] < 5):
				tree[1] = "_RARE_"
		else:
			change(tree[1], wordCount)

def main(parse_file):
	wordCount = dict();
	for line in open(parse_file):
		tree = json.loads(line)
		count(tree, wordCount)
	
	for line in open(parse_file):
		tree = json.loads(line)
		change(tree, wordCount)
		print json.dumps(tree)

def usage():
	sys.stderr.write("""
	Usage: python emit_rare.py tree_file > rare_tree_file.\n""")

if __name__ == "__main__":
	if len(sys.argv) != 2:
		usage()
		sys.exit(1)
	main(sys.argv[1])

