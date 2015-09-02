import random

class State:
	utility = 0
	visitation = 0
	worker = None
	parent = None
	children = []
	def __init__(self, parent, V, W):
		self.V = V
		self.W = W

class System:
	counts: {}
	total = 0
	start = 0
	root: State()
	def __init__(self, start):
		self.start = start
	def sample(self, samples, horizon, task, workers):
		for i in range(0, samples):
			cursor = root
			hired = 0
			rank = 0
			while hired < horizon:
				worker = workers[rank]
				rank += 1






				hired += 1

	def evaluate(self):

	def hire(self):
