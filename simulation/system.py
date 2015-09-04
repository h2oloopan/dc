import random

class State:
	utility = 0
	visitation = 0
	hired = None
	to_hire = None
	parent = None
	children = {}
	answers = []
	hirings = []
	def __init__(self, parent, V, W):
		self.parent = parent
		self.V = V
		self.W = W

class System:
	counts: {}
	total = 0
	start = 0
	root: State()
	def __init__(self, start):
		self.start = start
		self.root.visitation = 1
	def pickOutcome(self, outcomes, probabilities):
		levels = []
		total = 0
		for o in range(0, len(outcomes)):
			total += probabilities[o]
			levels.append(total)
		r = random.random()
		for l in range(0, len(levels)):
			level = levels[l]
			if r < level:
				return outcomes[l]
		return None
	def sample(self, samples, horizon, task, outcomes, workers):
		for i in range(0, samples):
			cursor = root
			number = 0
			#rank = 0
			while number < horizon:
				#worker = workers[rank] #next worker to hire
				#ank += 1
				for w in range(0, len(workers)):
					worker = workers[w]
					probabilities = []
					sum_prob = 0
					for o in range(0, len(outcomes)):
						outcome = outcomes[o]
						p1 = 1.0
						p2 = 1.0
						p3 = 1.0
						for t in range(0, len(outcomes)):
							truth = outcomes[t]
							if outcome == truth:
								p1 = worker.getQuality()
							else:
								p1 = 1 - worker.getQuality()
							for a in range(0, len(cursor.answers)):
								answer = cursor.answers[a]
								hire = cursor.hirings[a]
								if answer == truth:
									p2 = p2 * hire.getQuality()
								else:
									p2 = p2 * (1 - hire.getQuality())
							p3 = float(counts[truth]) / float(total)
						probabilities.append(p1 * p2 * p3)
						sum_prob += p1 * p2 * p3
					#need to normalize probability
					for o in range(0, len(outcomes)):
						outcome = outcomes[o]
						probabilities[0] = probabilities[o] / sum_prob
					pick = self.pickOutcome(outcomes, probabilities)

					key = str(worker.uuid) + '.' + str(pick)
					nextState = cursor.children[key]
					if nextState == None:
						nextState = State(cursor, 0, None)
						nextState.worker = worker
						nextState.answers = list(cursor.answers)
						nextState.answers.append(worker.doTask(task))
						nextState.hirings = list(cursor.hirings)
						nextState.hirings.append(worker)
						cursor.children[key] = nextState
					nextState.visitation += 1
					cursor = nextState
					number += 1

	def evaluateState(self, state):
		cl = state.children.items()
		if len(cl) == 0:
			state.utility = self.getAnswerUtility(state.hirings, state.answers)
		else:
			group = {}
			workers = {}
			for key, child in cl:
				self.evaluateState(child)
				if group[child.worker.uuid] is None:
					group[child.worker.uuid] = [child]
					workers[child.worker.uuid] = child.worker
				else:
					group[child.worker.uuid].append(child)
			#now all children are done
			for uuid, worker in group.items():




	def getWorkerUtility(self, state, worker, states):

	def getAnswerUtility(self, hirings, answers):
	
	def getVOI(self, state, worker):

	def evaluate(self):
		self.evaluateState(self.root)
	def hire(self):
		workers = []
		return workers



