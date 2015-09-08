import random
import learn

class State:
	utility = 0.0
	visitation = 0
	hired = None
	to_hire = None
	parent = None
	children = {}
	answers = []
	hirings = []
	def __init__(self, parent):
		self.parent = parent

class System:
	counts = None
	total = 0
	root = State(None)
	hire_pointer = None
	w_belief = 1.0
	w_quality = 1.0
	def __init__(self, outcomes, start, weights):
		self.counts = {}
		for outcome in outcomes:
			self.counts[str(outcome)] = start
			self.total += start
		if weights is not None and weights['belief'] is not None:
			self.w_belief = weights['belief']
		if weights is not None and weights['quality'] is not None:
			self.w_quality = weights['quality']
		self.reset()
	def reset(self):
		self.root = State(None)
		self.root.visitation = 1
		self.hire_pointer = self.root

	def rankWorkers(self, workers):
		sorted(workers, key=lambda worker: )

	def dh(self, tasks, outcomes, workers, ps):
		#l is the horizon -> maximum number of workers to hire
		#s is the number of samples
		l = ps[0]
		s = ps[1]
		t = ps[2] #number of tutorials
		result = []
		for task in tasks:
			self.reset()
			self.sample(s, l, task, outcomes, self.rankWorkers(workers))
			self.evaluate()
			last_hire = None
			last_answer = None
			hired = []
			answers = []
			while True:
				next_worker = self.hireNext(last_hire, last_answer)
				if next_worker is None:
					break
				else:
					answer = next_worker.doTask(task, outcomes, worker.c)
					hired.append(worker)
					answers.append(answer)
			#hiring is done
			prediction = self.aggregate(hired, answers)
			result.append(prediction)
		return result

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
				worker = workers[rank]
				rank += 1

				probabilities = [] #probability for each outcome
				sum_prob = 0
				for outcome in outcomes:
					p1 = 1.0
					p2 = 1.0
					p3 = 1.0
					for truth in outcomes:
						if outcomes == truth:
							p1 = worker.getEstimatedQualityAtX(worker.x)
						else:
							p1 = 1 - worker.getEstimatedQualityAtX(worker.x)
						for j in range(0, len(cursor.answers)):
							answer = cursor.answers[j]
							hire = cursor.hirings[j]
							if answer == truth:
								p2 = p2 * hire.getEstimatedQualityAtX(hire.x)
							else:
								p2 = p2 * (1 - hire.getEstimatedQualityAtX(hire.x))
						p3 = float(self.counts[str(truth)]) / float(self.total)
					probabilities.append(p1 * p2 * p3)
					sum_prob += p1 * p2 * p3

				#need to normalize probability
				for o in range(0, len(outcomes)):
					outcome = outcomes[o]
					probabilities[o] = probabilities[o] / sum_prob
				pick = self.pickOutcome(outcomes, probabilities)

				key = str(worker.uuid) + '.' + str(pick)
				if key not in cursor.children:
					nextState = State(cursor)
					nextState.hired = worker
					nextState.answers = list(cursor.answers)
					nextState.answers.append(pick)
					nextState.hirings = list(cursor.hirings)
					nextState.hirings.append(worker)
					cursor.children[key] = nextState
				cursor.children[key].visitation += 1
				cursor = cursor.children[key]
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
		delta = worker.getEstimatedQualityAtX(worker.x + 1) - worker.getEstimatedQualityAtX(worker.x)
		utility = self.w_quality * delta - float(worker.c)
		visitation = 0
		for state in states:
			visitation += state.visitation
		for state in states:
			utility += (float(state.visitation) / float(visitation)) * state.utility
		return utility

	def getAnswerUtility(self, hirings, answers):
		answer, count = self.aggregate(hirings, answers)
		return self.w_belief * (float(count) / float(len(answers)))

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
		return max_vote_answer, max_vote_count
	def update(self, workers, answers, outcome):
		if self.counts[str(outcome)] is None:
			self.counts[str(outcome)] = 1
		else:
			self.counts[str(outcome)] += 1
		self.total += 1
		#update workers
		for i in range(0, len(workers)):
			worker = workers[i]
			answer = answers[i]
			if answer == outcome:
				worker.updateLearning(True)
			else:
				worker.updateLearning(False)
			worker.learn()





