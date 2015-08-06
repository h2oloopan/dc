import sys
import numpy as np
import matplotlib.pyplot as plot
import learn
import simulate
import algorithm


def analyze(tasks, answers, costs, step, smooth, graph):
	#analyze answers
	total = len(tasks)
	stepCorrect = 0
	totalCorrect = 0
	counter = 0

	stepAccuracies = []
	cumulatedAccuracies = []
	smoothedAccuracies = []

	while counter < total:
		stepCorrect = 0
		for i in range(0, step):
			if tasks[counter+i] == answers[counter+i]:
				stepCorrect += 1
				totalCorrect += 1
		counter += step
		stepAccuracies.append(float(stepCorrect) / float(step))
		cumulatedAccuracies.append(float(totalCorrect) / float(counter))
		#calculate smoothed accuracies
		avg = 0
		num = 0
		for j in range(0, smooth):
			index = (counter / step) - 1 - j
			if index >= 0:
				avg += stepAccuracies[index]
				num += 1
		avg = float(avg) / float(num)
		smoothedAccuracies.append(avg)

	x1 = np.arange(0, total, step)
	graph[0].plot(x1, stepAccuracies)
	graph[0].plot(x1, cumulatedAccuracies)
	graph[0].plot(x1, smoothedAccuracies)

	x2 = np.arange(0, total, 1)
	graph[1].plot(x2, costs)
def resetWorkers(workers):
	for i in range(0, len(workers)):
		workers[i].reset()

if __name__ == '__main__':
	print 'Simulation Test'
	workers = simulate.createHyperbolicWorker(1000, 30, 1)
	tasks = simulate.createBinaryTasks(1000)

	#initialize plots
	f, ax = plot.subplots(4, 2, sharex=True)
	
	#analyze answers
	step = 10
	smooth = 3
	
	print 'Pick 5 workers randomly'
	answers = algorithm.pickRandomly(tasks, workers, 5)
	costs = [5 for i in range(0, len(tasks))]
	analyze(tasks, answers, costs, step, smooth, ax[0])

	resetWorkers(workers)
	print 'Pick 5 workers randomly with 5 tutorials'
	answers = algorithm.pickRandomlyWithTutorials(tasks, workers, 5, 5)
	costs = [5 for i in range(0, len(tasks))]
	analyze(tasks, answers, costs, step, smooth, ax[1])

	#reset workers
	#workers = simulate.createHyperbolicWorker(1000, 10, 1)
	resetWorkers(workers)
	print 'Pick top 5 workers with 5 tutorials'
	answers = algorithm.pickTopK(tasks, workers, 5, 5)
	costs = [5 for i in range(0, len(tasks))]
	analyze(tasks, answers, costs, step, smooth, ax[2])

	resetWorkers(workers)
	print 'Pick top 3 workers with 5 tutorials'
	answers = algorithm.pickTopK(tasks, workers, 3, 5)
	costs = [3 for i in range(0, len(tasks))]
	analyze(tasks, answers, costs, step, smooth, ax[3])


	plot.show()
