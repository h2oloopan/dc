import sys
import uuid
import numpy as np
import matplotlib.pyplot as plot
import simulate
import learn
import random
from worker import Worker

def resetWorkers(workers):
	for worker in workers:
		worker.reset()


if __name__ == '__main__':
	print 'Regression Test'
	r = {'mu': 50, 'sigma': 10}
	p = {'mu': 65, 'sigma': 10}

	workers = simulate.createHyperbolicWorker(1000, r, p, None, 1)
	outcomes = [True, False]

	max_length = 1000
	xs = np.arange(1, max_length + 1, 1)


	avgDiffR = []
	avgDiffQ = []
	diffR5 = []
	diffR15 = []
	diffROther = []
	diffQ5 = []
	diffQ15 = []
	diffQOther = []

	for length in range(1, max_length + 1):
		resetWorkers(workers)
		tasks = simulate.createBinaryTasks(length)
		totalDiffR = 0.0
		totalDiffQ = 0.0
		totalDiffR5 = 0
		totalDiffR15 = 0
		totalDiffROther = 0
		totalDiffQ5 = 0
		totalDiffQ15 = 0
		totalDiffQOther = 0
		for worker in workers:
			for task in tasks:
				answer = worker.doTask(task, outcomes)
				if answer == task:
					worker.updateLearning(True)
				else:
					worker.updateLearning(False)
			worker.learn()
			diffR = abs(worker.er - worker.r) / float(worker.r)
			diffQ = abs(worker.getEstimatedQualityAtX(worker.x) - worker.getQualityAtX(worker.x)) / float(worker.getQualityAtX(worker.x))
			totalDiffR += diffR
			totalDiffQ += diffQ
			if diffR <= 0.05:
				totalDiffR5 += 1
			elif diffR <= 0.15:
				totalDiffR15 += 1
			else:
				totalDiffROther += 1
			if diffQ <= 0.05:
				totalDiffQ5 += 1
			elif diffQ <= 0.15:
				totalDiffQ15 += 1
			else:
				totalDiffQOther += 1

		avgDiffR.append(totalDiffR / float(len(workers)))
		avgDiffQ.append(totalDiffQ / float(len(workers)))

		diffR5.append(float(totaldiffR5) / float(len(workers)))
		diffR15.append(float(totalDiffR15) / float(len(workers)))
		diffQ5.append(float(totalDiffQ5) / float(len(workers)))
		diffQ15.append(float(totalDiffQ15) / float(len(workers)))







