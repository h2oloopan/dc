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

def analyze(graph, runs, steps, algorithm, tasks, outcomes, workers, parameters):
	total_ws = []
	total_cs = []
	cs = []
	qs = []
	for i in range(0, runs):
		answers = algorithm(tasks, outcomes, workers, parameters)
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
	graph[0].plot(xs, cs)
	graph[0].plot(xs, qs)
	graph[1].plot(total_ws, total_cs)


if __name__ == '__main__':
	r = {'mu': 50, 'sigma': 10}
	p = {'mu': 20, 'sigma': 5}

	workers = simulate.createHyperbolicWorker(100, r, p, None, 1)
	tasks = simulate.createBinaryTasks(100)
	outcomes = [True, False]

	runs = 5
	steps = 3


	f, ax = plot.subplots(2, 2)


	print 'Random K'
	k = 5
	analyze(ax[0], runs, steps, algorithm.randomK, tasks, outcomes, workers, k)



	print 'Top K'
	k = 3
	t = 5
	analyze(ax[1], runs, steps, algorithm.topKAverageWithTutorials, tasks, outcomes, workers, [k, t])


	print 'Dynamic Hiring'
	system = System(outcomes, 10, {'belief' : 1, 'quality': 1})

	plot.show()









