import random


def findAvailableWorkers(workers):
	availables = []
	for i in range(0, len(workers)):
		if workers[i].isAvailable():
			availables.append(workers[i])
	#print len(availables)
	return availables

def findTopKAvailableWorkers(workers, observedCorrectness, k):
	top = []
	qualities = []
	amount = 0
	last = 0
	for i in range(0, len(workers)):
		worker = workers[i]
		predictedQuality = float(observedCorrectness[worker.uuid]) / float(worker.x)
		if worker.isAvailable():
			j = k - 1
			while j >= 0:
				if len(top) <= j or predictedQuality > qualities[j]:
					j -= 1
				else:
					break
			j += 1
			nextWorker = worker
			nextQuality = predictedQuality
			for n in range(j, k):
				if n < len(top):
					lastWorker = top[n]
					lastQuality = qualities[n]
					top[n] = nextWorker
					qualities[n] = nextQuality
					nextWorker = lastWorker
					nextQuality = lastQuality
				else:
					top.append(nextWorker)
					qualities.append(nextQuality)
	#print qualities
	return top


def randomK(tasks, outcomes, workers, k):
	answers = []
	for task in tasks:
		availables = findAvailableWorkers(workers)
		votes = {}
		vote = None
		max_vote = 0
		for j in range(0, k):
			worker = availables[random.randint(0, len(availables) - 1)]
			answer = worker.doTask(task, outcomes)
			if votes[str(answer)] is None:
				votes[str(answer)] = 1
			else:
				votes[str(answer)] += 1
			if votes[str(answer)] > max_vote:
				max_vote = votes[str(answer)]
				vote = answer
		answers.append(vote)
	return answers

def pickRandomly(tasks, workers, limit):
	#pick workers randomly from all available ones
	answers = []
	for i in range(0, len(tasks)):
		task = tasks[i]
		availables = findAvailableWorkers(workers)
		flag = 0
		for j in range(0, limit):
			pick = random.randint(0, len(availables) - 1)
			worker = availables[pick]
			answer = worker.doTask(task)
			if answer:
				flag = flag + 1
			else:
				flag = flag - 1
		if flag >= 0:
			answers.append(True)
		else:
			answers.append(False)
	return answers

def pickRandomlyWithTutorials(tasks, workers, limit, tutorials):
	#train
	for i in range(0, len(workers)):
		for j in range(0, tutorials):
			task = tasks[j]
			workers[i].doTask(task)
	#now do the same thing
	return pickRandomly(tasks, workers, limit)

def pickTopK(tasks, workers, k, tutorials):
	answers = []
	observedCorrectness = {} #note here observed correctness may not be the actual correctness
	#other than the tutorial, the other are just benchmarked from the aggregated avg answer
	for i in range(0, len(workers)):
		worker = workers[i]
		count = 0
		for j in range(0, tutorials):
			task = tasks[j]
			answer = worker.doTask(task)
			if answer == task:
				count += 1
		observedCorrectness[worker.uuid] = count

	for i in range(0, len(tasks)):
		task = tasks[i]
		top = findTopKAvailableWorkers(workers, observedCorrectness, k)
		currentAnswers = []
		flag = 0
		for j in range(0, len(top)):
			currentAnswer = top[j].doTask(task)
			currentAnswers.append(currentAnswer)
			if currentAnswer:
				flag += 1
			else:
				flag -= 1
		if flag >= 0:
			aggregatedAnswer = True
		else:
			aggregatedAnswer = False
		answers.append(aggregatedAnswer)
		for j in range(0, len(top)):
			if currentAnswers[j] == aggregatedAnswer:
				observedCorrectness[top[j].uuid] += 1

	return answers







