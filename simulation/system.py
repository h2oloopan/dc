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
	root: State()
	hire_pointer: None
	w_belief: 1.0
	def __init__(self, outcomes, start, weights):
		self.root.visitation = 1
		self.hire_pointer = self.root
		for outcome in outcomes:
			self.counts[str(outcome)] = start
			self.total += start
		if weights['belief'] is not None:
			self.w_belief = weights['belief']
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
							p3 = float(self.counts[str(truth)]) / float(self.total)
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
						nextState.hired = worker
						nextState.answers = list(cursor.answers)
						nextState.answers.append(worker.testTask(task))
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
			state.to_hire = None
		else:
			group = {}
			workers = {}
			for key, child in cl:
				self.evaluateState(child)
				if group[child.hired.uuid] is None:
					group[child.hired.uuid] = [child]
					workers[child.hired.uuid] = child.hired
				else:
					group[child.hired.uuid].append(child)
			#now all children are done
			to_hire = None
			max_voi = None
			max_utility = None
			for uuid, worker in workers.items():
				children = group[uuid]
				utility = self.getWorkerUtility(state, worker, children)
				voi = utility - self.getAnswerUtility(state.hirings, state.answers)
				if max_voi < voi or max_voi is None:
					max_voi = voi
					to_hire = worker
					max_utility = utility
			if max_voi < 0:
				to_hire = None
				max_utility = self.getAnswerUtility(state.hirings, state.answers)
			state.utility = max_utility
			state.to_hire = to_hire



	def getWorkerUtility(self, state, worker, states):

	def getAnswerUtility(self, hirings, answers):
		answer, count = self.aggregate(hirings, answers)
		return self.w_belief * (float(count) / float(len(answers)))
	
	def getVOI(self, state, worker):

	def evaluate(self):
		self.evaluateState(self.root)
	def hireNext(self, lastHire, lastAnswer):
		if lastHire is None or lastAnswer is None:
			#this is at root
			return self.hire_pointer.to_hire
		else:
			#update hire_pointer
			key = str(lastHire.uuid) + '.' + str(lastAnswer)
			self.hire_pointer = self.children[key]
			return self.hire_pointer.to_hire
	def aggregate(self, workers, answers):
		max_vote_count = 0
		max_vote_answer = None
		votes = {}
		for answer in answers:
			if votes[str(answer)] is None:
				votes[str(answer)] = 1
			else:
				votes[str(answer)] += 1
			if votes[str(answer)] > max_vote_count:
				max_vote_count = votes[str(answer)]
				max_vote_answer = answer
		return (max_vote_answer, max_vote_count)
	def update(self, outcome):
		if self.counts[str(outcome)] is None:
			self.counts[str(outcome)] = 1
		else:
			self.counts[str(outcome)] += 1
		self.total += 1




