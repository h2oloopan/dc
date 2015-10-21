import sys
import numpy as np
import simulate
from system import System

def resetWorkers(workers):
	for worker in workers:
		worker.reset()


if __name__ == '__main__':
	r = {'mu': 50, 'sigma': 10}
	p = {'mu': 40, 'sigma': 5}

	workers = simulate.createHyperbolicWorker(100, r, p, None, 1)
	tasks = simulate.createBinaryTasks(1000)
	outcomes = [True, False]


	horizon = 3
	samples = 1024
	tutorials = 10


	for b in range(1, 20):
		belief = float(b)# / 10.0
		for q in range(1, 2):
			quality = float(q)
			resetWorkers(workers)
			system = System(outcomes, 10, {'belief': belief, 'quality': quality})
			answers = system.dh(tasks, outcomes, workers, [horizon, samples, tutorials])

			count = 0
			hired = 0
			for i in range(0, len(answers)):
				if answers[i][0] == tasks[i]:
					count += 1
				hired += answers[i][1]

			percent = float(count) / float(len(tasks))
			print 'belief ', belief, ' quality ', quality, ' percent ', percent, 'hired', hired


