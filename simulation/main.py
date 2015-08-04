import sys
import numpy as np
import matplotlib.pyplot as plot
import learn
import simulate
import algorithm

if __name__ == '__main__':
	print 'Simulation Test'
	workers = simulate.createWorker(1000, 20, 1)
	tasks = simulate.createBinaryTasks(1000)
	
	print 'Pick 5 workers randomly'
	answers = algorithm.pickRandomly(tasks, workers, 10)

	#analyze answers
	total = len(tasks)
	step = 10
	avg = 3
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


	x = np.arange(0, total, step)
	plot.plot(x, stepAccuracies)
	plot.plot(x, cumulatedAccuracies)
	plot.show()