import sys
import numpy as np
import matplotlib.pyplot as plot
import simulate
import learn
import random
import algorithm
from system import System



def resetWorkers(workers):
	for worker in workers:
		worker.reset()

if __name__ == '__main__':
	r = {'mu': 10, 'sigma': 2.5}
	p = {'mu': 5, 'sigma': 1}

	workers = simulate.createHyperbolicWorker(1000, r, p, None, 1)
	tasks = simulate.createBinaryTasks(1000)
	outcomes = [True, False]

	runs = 5
	steps = 2


	f, ax = plot.subplots(2, 2)


	print 'Random K'
	k = 10
	cs = []
	qs = []
	for i in range(0, runs):
		answers = algorithm.randomK(tasks, outcomes, workers, k)
		resetWorkers(workers)
		#print tasks
		#print answers

		for i in range(0, len(tasks)):
			if answers[i] == tasks[i]:
				if i >= len(cs):
					cs.append(1)
				else:
					cs[i] += 1
			else:
				if i >= len(cs):
					cs.append(0)
	cumulative = 0
	#print cs
	for i in range(0, len(cs)):
		avg = cs[i]
		count = 1
		for j in range(1, steps + 1):
			if i - j >= 0:
				avg += cs[i - j]
				count += 1
			if i + j < len(cs):
				avg += cs[i + j]
				count += 1
		qs.append(float(avg) / (float(runs) * float(count)))


		cs[i] = cs[i] + cumulative
		cumulative = cs[i]
		cs[i] = float(cs[i]) / (float(runs) * float(i + 1))

	xs = np.arange(1, len(tasks) + 1, 1)
	ax[0][0].plot(xs, cs)
	ax[0][0].plot(xs, qs)
	plot.show()












