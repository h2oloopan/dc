class State:
	V = 0
	W = None
	def __init__(self, V, W):
		self.V = V
		self.W = W

class System:
	counts: {}
	root: State()
	def sample(self, samples, horizon):

