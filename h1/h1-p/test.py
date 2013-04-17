from collections import defaultdict

class Record:
	value = 0
	prev = 0
	def __init__(self, value, prev):
		self.prev = prev 
		self.value = value

old = defaultdict(Record)

def number_generator():
	for i in xrange(10):
		yield range(i) 

if __name__ == "__main__":
	dict = defaultdict(int)
	dict['1'] = 10
	dict[1] = 20
	for iter in dict:
		print iter, dict[iter]

