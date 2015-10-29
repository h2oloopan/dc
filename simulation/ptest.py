import sys
import uuid
import numpy as np
import matplotlib.pyplot as plot
import simulate
import learn
import math
import random
from worker import Worker


r = {'mu': 50, 'sigma': 10}
p = {'mu': 65, 'sigma': 10}
workers = simulate.createHyperbolicWorker(3000, r, p, None, 1)
outcomes = [True, False]

tasks = simulate.createBinaryTasks(30)

xs = np.arange(0, 101, 5)

dist_all = []
dist_p10 = []
dist_avg = []


total_all = 0.0
total_avg = 0.0

for i in range(0, len(xs)):
	dist_all.append(0)
	dist_p10.append(0)
	dist_avg.append(0)

for worker in workers:
	for task in tasks:
		answer = worker.doTask(task, outcomes)
		if answer == task:
			worker.updateLearning(True)
		else:
			worker.updateLearning(False)
	worker.learn()
	diff = abs(worker.getEstimatedQualityAtX(worker.x) - worker.getQualityAtX(worker.x)) / worker.getQualityAtX(worker.x)
	diffAvg = abs(worker.getAveragedCumulativeQuality() - worker.getQualityAtX(worker.x)) / worker.getQualityAtX(worker.x)
	total_all += diff
	total_avg += diffAvg
	for i in range(0, len(xs)):
		gap = xs[i]
		if diff * 100.0 <= gap:
			if worker.epv < math.pow(10, -10):
				#print worker.epv
				dist_p10[i] += 1
			dist_all[i] += 1
		if diffAvg * 100.0 <= gap:
			dist_avg[i] += 1



print total_all / len(workers)
print total_avg / len(workers)

f, (ax, bx) = plot.subplots(1, 2)
ax.plot(xs, dist_all, label='# tasks')
#ax[1].plot(xs, dist_p10)
bx.plot(xs, dist_avg, label='# tasks')


ax.set_title('Quality Estimation Accuracy - Linear Regression')
bx.set_title('Quality Estimation Accuracy - Averaged Quality')

ax.set_xlabel('percentage')
ax.set_ylabel('workers')
bx.set_xlabel('percentage')
bx.set_ylabel('workers')

ax.legend(bbox_to_anchor=(1, 0.3))
bx.legend(bbox_to_anchor=(1, 0.3))




plot.show()









