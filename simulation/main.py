import sys
import numpy as np
import matplotlib.pyplot as plot
import learn
import simulate
import algorithm


if __name__ == '__main__':
	print 'Simulation Test'
	workers = simulate.createHyperbolicWorker(1000, 10, 1)
	tasks = simulate.createBinaryTasks(2000)
	
	print 'Pick 5 workers randomly'
	answers = algorithm.pickRandomly(tasks, workers, 10)

	#analyze answers
	total = len(tasks)
	step = 10
	smooth = 5
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

	x = np.arange(0, total, step)
	plot.plot(x, stepAccuracies)
	plot.plot(x, cumulatedAccuracies)
	plot.plot(x, smoothedAccuracies)
	plot.show()

	#recreate some workers
	#workers = simulate.createHyperbolicWorker(1000, 10, 1)


