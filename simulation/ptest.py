import sys
import uuid
import numpy as np
import matplotlib.pyplot as plot
import simulate
import learn
import random
from worker import Worker


r = {'mu': 50, 'sigma': 10}
p = {'mu': 65, 'sigma': 10}
workers = simulate.createHyperbolicWorker(1000, r, p, None, 1)
outcomes = [True, False]

tasks＝ simulate.createBinaryTasks(30)

xs = np.arange(0, 101, 5)

dist_all = []
dist_p10 = []
dist_avg = []

for i in range(0, len(xs)):
	dist_all.append(0)
	dist_p10.append(0)
	dist_avg.append(0)

for worker in workers:
	for task in tasks:
		answer = worker.doTask(task, outcomes)
		if answer = task:
			worker.updateLearning(True)
		else:
			worker.updateLearning(False)
	worker.learn()
	for i in range(0, len(xs)):
		gap = xs[i]
		diff = abs(worker.getEstimatedQualityAtX(worker.x) - worker.getQualityAtX(worker.x)) / worker.getQualityAtX(worker.x)
		if diff * 100.0 <= gap:
			if worker.epv < math.pow(10, -10):
				dist_p10[i] += 1
			dist_all[i] += 1
		diffAvg = abs(worker.getAveragedCumulativeQuality() - worker.getQualityAtX(worker.x)) / worker.getQualityAtX(worker.x)
		if diffAvg * 100.0 <= gap:
			dist_avg[i] += 1

f, ax = plot.subplots(3)
ax[0].plot(xs, dist_all)
ax[1].plot(xs, dist_p10)
ax[2].plot(xs, dist_avg)


plot.show()









