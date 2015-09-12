import random
import learn
import simulate


class State:
	utility = 0.0
	visitation = 0
	hired = None
	to_hire = None
	parent = None
	children = None
	answers = None
	hirings = None
	def __init__(self, parent):
		self.parent = parent
		self.children = {}
		self.answers = []
		self.hirings = []
	def __str__(self):
		s = ''
		#s += 'hired: ' + str(self.hired) + '\n'
		if self.to_hire is not None:
			s += 'to hire: ' + str(self.to_hire.uuid) + '\n'
		s += 'answers: ' + str(self.answers) + '\n'
		#s += 'hirings: ' + str(self.hirings) + '\n'
		s += 'utility: ' + str(self.utility) + '\n'
		s += 'visitation: ' + str(self.visitation) + '\n'
		return s

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
		self.root.visitation = 0
		self.hire_pointer = self.root

	def rankWorkers(self, workers, projection=100):
		available = []
		for worker in workers:
			if worker.isAvailable():
				available.append(worker)

		return sorted(available, key=lambda worker: worker.calculate(projection))

	def dh(self, tasks, outcomes, workers, ps):
		#l is the horizon -> maximum number of workers to hire
		#s is the number of samples
		l = ps[0]
		s = ps[1]
		t = ps[2] #number of tutorials
		result = []

		total_tasks = len(tasks)
		completed_tasks = 0

		#running tutorials
		tutorials = simulate.createBinaryTasks(t)
		for worker in workers:
			for tutorial in tutorials:
				answer = worker.doTask(tutorial, outcomes)
				if answer == tutorial:
					worker.updateLearning(True)
				else:
					worker.updateLearning(False)
			worker.learn()

		for task in tasks:
			self.reset()
			self.sample(s, l, task, outcomes, self.rankWorkers(workers, total_tasks - completed_tasks))
			#continue
			self.evaluate()
			#print 'Evaluation done'
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
					last_hire = next_worker
					last_answer = answer
			#hiring is done
			prediction = self.aggregate(hired, answers)
			#print answers, prediction
			#update all hired workers
			self.update(hired, answers, prediction)
			result.append((prediction[0], len(hired)))
			completed_tasks += 1
		return result

	def pickOutcome(self, outcomes, probabilities):
		levels = []
		total = 0
		#print probabilities
		for o in range(0, len(outcomes)):
			total += probabilities[o]
			levels.append(total)
		r = random.uniform(0, total)
		for l in range(0, len(levels)):
			level = levels[l]
			if r < level:
				#print r, level
				return outcomes[l]
		return None
	def sample(self, samples, horizon, task, outcomes, workers):
		for i in range(0, samples):
			cursor = self.root
			number = 0
			rank = 0

			cursor.visitation += 1
			#print str(cursor)
			while number < horizon:
				#print 'at', str(cursor)
				#worker = workers[rank] #next worker to hire
				#ank += 1
				worker = workers[rank]
				rank += 1

				probabilities = [] #probability for each outcome
				#sum_prob = 0
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
					#sum_prob += p1 * p2 * p3

				#need to normalize probability
				#for o in range(0, len(outcomes)):
				#	outcome = outcomes[o]
				#	probabilities[o] = probabilities[o] / sum_prob
				pick = self.pickOutcome(outcomes, probabilities)

				key = str(worker.uuid) + '.' + str(pick)
				#print 'children', cursor.children.keys()
				if key not in cursor.children.keys():
					#print key
					nextState = State(cursor)
					nextState.hired = worker
					nextState.answers = list(cursor.answers)
					nextState.answers.append(pick)
					nextState.hirings = list(cursor.hirings)
					nextState.hirings.append(worker)
					cursor.children[key] = nextState
					#print 'added', nextState
				cursor.children[key].visitation += 1
				cursor = cursor.children[key]
				number += 1

				#print str(cursor)


	def evaluateState(self, state):
		cl = state.children.items()
		#print 'evaluate'
		#print state
		#print cl
		if len(cl) == 0:
			#this is a leaf node
			state.utility = self.getAnswerUtility(state.hirings, state.answers)
			state.to_hire = None
		else:
			total_visitation = 0
			#first loop
			for key, child in cl:
				self.evaluateState(child)
				total_visitation += child.visitation
			#second loop
			worker = cl[0][1].hired
			voi = self.getWorkerUtility(worker)
			for key, child in cl:
				voi += (float(child.visitation) / float(total_visitation)) * child.utility
			utility = voi
			voi -= self.getAnswerUtility(state.hirings, state.answers)
			if voi <= 0:
				state.to_hire = None
				state.utility = utility - voi
			else:
				state.to_hire = worker
				state.utility = utility


		print 'evaluated'
		print state

		#print 'evaluate state'
		#print state



	def getWorkerUtility(self, worker):
		delta = worker.getEstimatedQualityAtX(worker.x + 1) - worker.getEstimatedQualityAtX(worker.x)
		return self.w_quality * delta - float(worker.c)

	def getAnswerUtility(self, hirings, answers):
		if len(answers) == 0:
			return 0
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
			#print self.hire_pointer
			#print self.hire_pointer.children
			self.hire_pointer = self.hire_pointer.children[key]
			return self.hire_pointer.to_hire
	def aggregate(self, workers, answers):
		max_vote_count = 0
		max_vote_answer = None
		votes = {}
		for answer in answers:
			if str(answer) not in votes.keys():
				votes[str(answer)] = 1
			else:
				votes[str(answer)] += 1
			if votes[str(answer)] > max_vote_count:
				max_vote_count = votes[str(answer)]
				max_vote_answer = answer
		return max_vote_answer, max_vote_count
	def update(self, workers, answers, outcome):
		#print 'update system'
		#print workers, answers, outcome
		outcome = outcome[0]
		if outcome is None:
			pass
			return #nothing to update
		if str(outcome) not in self.counts.keys():
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





