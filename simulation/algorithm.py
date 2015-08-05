import random


def findAvailableWorkers(workers):
	availables = []
	for i in range(0, len(workers)):
		if workers[i].isAvailable():
			availables.append(workers[i])
	return availables

def findTopKAvailableWorkers(workers, observedCorrectness, k):



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







