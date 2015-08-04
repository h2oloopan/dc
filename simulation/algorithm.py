import random


def findAvailableWorkers(workers):
	availables = []
	for i in range(0, len(workers)):
		if workers[i].isAvailable():
			availables.append(workers[i])
	return availables




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
	observedQualities = []
	for i in range(0, len(workers)):
		worker = workers[i]
		count = 0
		for j in range(0, tutorials):
			task = tasks[j]
			answer = worker.doTask(task)
			if answer == task:
				count += 1
		observedQualities.append(float(count) / float(tutorials)) #initialize observed quality

	for i in range(0, len(tasks)):
		task = tasks[i]