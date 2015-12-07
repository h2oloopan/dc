import random
import learn
import simulate
import math


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
		if self.hired is not None:
			s += 'hired: ' + str(self.hired.uuid)  + ' ' + str(self.hired.getEstimatedQualityAtX(self.hired.x)) + '\n'
		s += 'answers: ' + str(self.answers) + '\n'
		#s += 'hirings: ' + str(self.hirings) + '\n'
		s += 'utility: ' + str(self.utility) + '\n'
		s += 'visitation: ' + str(self.visitation)
 		return s

class System:
	keep_hiring = False
	belief_threshold = 0.85
	dont_update = False

	def __init__(self, outcomes, start, weights):
		self.root = State(None)
		self.hire_pointer = None
		self.w_belief = 1.0
		self.w_quality = 1.0
		self.total = 0
		self.average_worker_quality = 0.0
		self.counts = {}
		self.workerpool = {}
		self.default_worker_projection = 0
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
		self.average_worker_quality = 0.0
		self.workerpool = {}

	def getCappedQuality(self, quality, average_quality, x):
		cap = 0.0045 * x + 0.1
		#print 'quality', quality
		#print 'average', average_quality
		#print 'x', x
		return min(quality, average_quality * (1.0 + cap))

	def rankWorkers(self, workers, projection=100):
		available = []
		for worker in workers:
			if worker.isAvailable():
				available.append(worker)
				#print worker.getQuality(), self.getCappedQuality(worker.getHybridQuality(), self.average_worker_quality, worker.x)

		result = sorted(available, key=lambda worker: worker.calculateProjection(self.getCappedQuality(worker.getHybridQuality(), self.average_worker_quality, worker.x), projection), reverse=True)

		return result

	def confidence(self, x):
		x = int(x)
		return float(x - 50) / (25.0 * math.sqrt(1.0 + math.pow(float(x - 50) / 10, 2))) + 0.6

	def coverage(self, p):
		p = float(p)
		return min(1.0, (2.0 * p) / (p / 2 + 1))


	def getAvailableWorkers(self, workers):
		result = []
		for worker in workers:
			if worker.isAvailable():
				result.append(worker)
				worker.presence[0] += 1
			worker.presence[1] += 1
		return result


	def calculateAverageWorkerQuality(self):
		if len(self.workerpool) == 0:
			self.average_worker_quality = 0.5
		else:
			average = 0.0
			for uuid in self.workerpool:
				average += self.workerpool[uuid].getHybridQuality()
			self.average_worker_quality = float(average) / float(len(self.workerpool))

	def getRankedWorkers(self, workers, horizon, projection=100):
		existings = []
		newcomers = []
		for worker in workers:
			if worker.x > 0:
				worker.w = worker.calculateProjection(self.getCappedQuality(worker.getHybridQuality(), self.average_worker_quality, worker.x), projection)
				existings.append(worker)
			else:
				worker.w = worker.calculateDefaultProjection(projection)
				if self.default_worker_projection == 0:
					self.default_worker_projection = worker.w
				newcomers.append(worker)

		result = []

		existings = sorted(existings, key=lambda worker: worker.w, reverse=True)
		cursor_existing = 0
		cursor_newcomer = 0
		while len(result) < horizon:
			if cursor_existing >= len(existings):
				result.append(newcomers[cursor_newcomer])
				cursor_newcomer += 1
			else:
				candidate = existings[cursor_existing]
				if candidate.w <= self.default_worker_projection:
					if cursor_newcomer >= len(newcomers):
						result.append(existings[cursor_existing])
						cursor_existing += 1
					else:
						result.append(newcomers[cursor_newcomer])
						cursor_newcomer += 1
				else:
					score = self.confidence(candidate.w * 100.0)
					#print 'candidate', candidate.w, score
					temp = random.random()
					if temp < score:
						result.append(existings[cursor_existing])
						cursor_existing += 1
					else:
						if cursor_newcomer >= len(newcomers):
							result.append(existings[cursor_existing])
							cursor_existing += 1
						else:
							result.append(newcomers[cursor_newcomer])
							cursor_newcomer += 1


		#print 'workers:'
		#for worker in result:
		#	print worker.getHybridQuality(), self.getCappedQuality(worker.getHybridQuality(), self.average_worker_quality, worker.x)

		return result


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

		#step = 10
		#step_counter = 0

		#self.reset()
		#self.calculateAverageWorkerQuality(workers)
		#availables = getAvailableWorkers(workers)
		#rankedWorkers = self.randomRank(workers, total_tasks - completed_tasks, l) #self.rankWorkers(workers, total_tasks - completed_tasks)# - completed_tasks)
		#self.sample(s, l, outcomes, availables)
		#self.evaluate(outcomes)

		totalTutorials = 0
		

		for task in tasks:
			#self.reset()
			#self.sample(s, l, task, outcomes, self.rankWorkers(workers, total_tasks - completed_tasks))
			#continue
			#self.evaluate(outcomes)
			#print 'Evaluation done'

			#step_counter = (step_counter + 1) % step
			#if step_counter == 0:
			#this rerank workers and do sampling and evaluation again
			self.reset()
			self.calculateAverageWorkerQuality()
			#rankedWorkers = self.randomRank(workers, total_tasks - completed_tasks, l) #rankedWorkers = self.rankWorkers(workers, total_tasks - completed_tasks)# - completed_tasks)
			availables = self.getAvailableWorkers(workers)
			rankedWorkers = self.getRankedWorkers(availables, l, total_tasks - completed_tasks)
			self.sample(s, l, outcomes, rankedWorkers)#, rankedWorkers)
			self.evaluate(outcomes)
				

			self.hire_pointer = self.root
			last_hire = None
			last_answer = None
			hired = []
			answers = []
			while True:
				if len(hired) >= l:
					break
				else:
					next_worker = self.hireNext(last_hire, last_answer)
					if next_worker is None:						
						break
					else:
						if next_worker.x < t:
							for tutorial in tutorials:
								answer = next_worker.doTask(tutorial, outcomes)
								if answer == tutorial:
									next_worker.updateLearning(True)
								else:
									next_worker.updateLearning(False)
							next_worker.learn()
							totalTutorials += t

						answer = next_worker.doTask(task, outcomes, next_worker.c)
						hired.append(next_worker)
						answers.append(answer)
						last_hire = next_worker
						last_answer = answer
			#hiring is done
			prediction, probability = self.aggregate(hired, answers, outcomes)
			#print '----------'
			#for i in range(0, len(hired)):
			#	worker = hired[i]
			#	answer = answers[i]
			#	print answer, worker.getHybridQuality()
			#print prediction, probability, '|', task
			#print '-----'
			#print answers
			#for w in hired:
			#	print w.getEstimatedQualityAtX(w.x)
			#print 'actual result', prediction, probability
			#print answers, prediction
			#update all hired workers
			self.update(hired, answers, prediction)
			result.append((prediction, len(hired)))


			#if len(hired) == 1:
				#print task, prediction, self.getCappedQuality(hired[0].getHybridQuality(), self.average_worker_quality, hired[0].x), hired[0].getHybridQuality(), hired[0].getQuality()

			completed_tasks += 1

		print totalTutorials, ' tutorials'
		return result

	def pickOutcome(self, outcomes, probabilities):
		#print '*picking outcome'
		#print outcomes
		#print probabilities
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
	def normalize(self, probabilities):
		result = []
		total = 0.0
		for probability in probabilities:
			total += probability
		for probability in probabilities:
			result.append(probability / total)
		return result
	def sample(self, samples, horizon, outcomes, workers):
		
		for i in range(0, samples):
			cursor = self.root
			number = 0
			rank = 0

			cursor.visitation += 1
			#print str(cursor)
			hired = []
			while number < horizon:
				#print 'at', str(cursor)
				#worker = workers[rank] #next worker to hire
				#ank += 1
				#worker = self.getNextWorker(workers, hired, projection)#workers[rank]
				worker = workers[number]
				hired.append(worker)
				#print worker.er, worker.ep, worker.getEstimatedQualityAtX(worker.x), worker.getQuality()
				rank += 1

				probabilities = [] #probability for each outcome
				#sum_prob = 0
				for outcome in outcomes:
					p1 = 1.0
					p2 = 1.0
					p3 = 1.0
					for truth in outcomes:
						if outcome == truth:
							p1 = worker.getHybridQuality()
						else:
							p1 = 1.0 - worker.getHybridQuality()
						for j in range(0, len(cursor.answers)):
							answer = cursor.answers[j]
							hire = cursor.hirings[j]
							if answer == truth:
								p2 = p2 * hire.getHybridQuality()
							else:
								p2 = p2 * (1.0 - hire.getHybridQuality())
						p3 = float(self.counts[str(truth)]) / float(self.total)
					#print outcome, p1, p2, p3
					probabilities.append(p1 * p2 * p3)
					#sum_prob += p1 * p2 * p3

				#need to normalize probability
				#for o in range(0, len(outcomes)):
				#	outcome = outcomes[o]
				#	probabilities[o] = probabilities[o] / sum_prob
				pick = self.pickOutcome(outcomes, self.normalize(probabilities))

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

	def getAnswerUtility(self, probability):
		#print probability, self.w_belief
		if probability > self.belief_threshold:
			return (math.pow(2.0, probability) - 1.0) * self.w_belief
		else:
			return 0
		#return (1 - math.sqrt(1 - probability * probability)) * self.w_belief

	def evaluateState(self, state, outcomes):
		cl = state.children.items()
		#print 'evaluate'
		#print state
		#print cl
		if len(cl) == 0:
			#this is a leaf node
			prediction, probability = self.aggregate(state.hirings, state.answers, outcomes)
			state.utility = self.w_belief * probability
			state.to_hire = None
		else:
			total_visitation = 0
			#first loop
			for key, child in cl:
				self.evaluateState(child, outcomes)
				total_visitation += child.visitation
			#second loop
			worker = cl[0][1].hired
			voi = self.getWorkerUtility(worker)
			#print voi
			for key, child in cl:
				#print 'child ', child.visitation, total_visitation, child.utility
				voi += (float(child.visitation) / float(total_visitation)) * child.utility
			utility = voi
			prediction, probability = self.aggregate(state.hirings, state.answers, outcomes)
			voi -= self.getAnswerUtility(probability)# * self.w_belief
			#print 'utility ', utility, 'voi ', voi, 'probability ', probability
			if voi <= 0:
				state.to_hire = None
				state.utility = utility - voi
			else:
				state.to_hire = worker
				state.utility = utility


		#print 'evaluated'
		#print state
		#print '-----opinion aggregation-----'
		#print prediction, probability
		#print ''

		#print 'evaluate state'
		#print state



	def getWorkerUtility(self, worker):
		delta = worker.getEstimatedQualityAtX(worker.x + 1) - worker.getEstimatedQualityAtX(worker.x)
		return self.w_quality * delta - float(worker.c)

	def evaluate(self, outcomes):
		self.evaluateState(self.root, outcomes)
	def hireNext(self, lastHire, lastAnswer):
		if lastHire is None or lastAnswer is None:
			#this is at root
			return self.hire_pointer.to_hire
		elif self.hire_pointer is None:
			return None
		else:
			#update hire_pointer
			key = str(lastHire.uuid) + '.' + str(lastAnswer)
			#print self.hire_pointer
			#print self.hire_pointer.children
			if key in self.hire_pointer.children:
				self.hire_pointer = self.hire_pointer.children[key]
				return self.hire_pointer.to_hire
			else:
				self.hire_pointer = None
				return None
	def aggregate(self, workers, answers, outcomes):

		if len(answers) == 0:
			return None, 0

		#print hirings, answers, prediction, outcomes

		#for i in range(0, len(workers)):
		#	worker = workers[i]
		#	answer = answers[i]
		#	print answer, worker.getEstimatedQualityAtX(worker.x)

		#print self.__dict__

		prob_sum = 0.0
		prob_pick = None
		prob_max = 0.0
		for outcome in outcomes:
			p1 = 1.0
			p2 = 1.0
			for i in range(0, len(workers)):
				worker = workers[i]
				answer = answers[i]
				#print self.average_worker_quality
				#print worker.getHybridQuality(), self.average_worker_quality, worker.x
				cappedQuality = self.getCappedQuality(worker.getHybridQuality(), self.average_worker_quality, worker.x)
				#print cappedQuality

				if str(answer) == str(outcome):
					#p1 = p1 * worker.getEstimatedQualityAtX(worker.x)
					p1 = p1 * cappedQuality
				else:
					#p1 = p1 * (1.0 - worker.getEstimatedQualityAtX(worker.x))
					p1 = p1 * (1.0 - cappedQuality)
			p2 = float(self.counts[str(outcome)]) / float(self.total)
			prob_sum += p1 * p2

			if p1 * p2 > prob_max:
				prob_max = p1 * p2
				prob_pick = outcome

			#print 'aggregate'
			#print outcome, p1 * p2


		prob = prob_max / prob_sum

		#print prob_pick, prob



		return prob_pick, prob
	def update(self, workers, answers, outcome):
		if self.dont_update:
			return None
		#print 'update system'
		#print workers, answers, outcome
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
			self.workerpool[worker.uuid] = worker

		self.calculateAverageWorkerQuality()





