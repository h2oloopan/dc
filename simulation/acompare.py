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
	steps = 3


	f, ax = plot.subplots(2, 2)


	print 'Random K'
	k = 5


	total_ws = []
	total_cs = []

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
	for i in range(0, len(cs)):		
		cs[i] = cs[i] + cumulative
		total_cs.append(cs[i] / runs)
		total_ws.append(k * (i + 1))
		cumulative = cs[i]
		cs[i] = float(cs[i]) / (float(runs) * float(i + 1))

	#print cs
	#print qs

	xs = np.arange(1, len(tasks) + 1, 1)
	ax[0][0].plot(xs, cs)
	ax[0][0].plot(xs, qs)
	ax[0][1].plot(total_ws, total_cs)
	plot.show()


	print 'Dynamic Hiring'
	system = System(outcomes, 10, {'belief' : 1, 'quality': 1})
	










