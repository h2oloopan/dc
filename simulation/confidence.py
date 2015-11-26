import sys
import numpy as np
import matplotlib.pyplot as plot
import simulate
import learn
import random


threshold = 0.8
outcomes = [True, False]

rcaps = []
qcaps = []


r = {'mu': 50, 'sigma': 10}
p = {'mu': 60, 'sigma': 10}


length = 100
size = 500

workers = simulate.createHyperbolicWorker(size, r, p, None, 1)



def resetWorkers(workers):
	for worker in workers:
		worker.reset()


for i in range(10, length + 1):
	tasks = simulate.createBinaryTasks(i)
	resetWorkers(workers)


	

	r_differences = []
	q_differences = []

	for worker in workers:
		for task in tasks:
			answer = worker.doTask(task, outcomes)
			if answer == task:
				worker.updateLearning(True)
			else:
				worker.updateLearning(False)
		worker.learn()
		rdiff = abs(worker.er - worker.r) / worker.r
		qdiff = abs(worker.getEstimatedQualityAtX(worker.x) - worker.getQuality()) / worker.getQuality()
		#print rdiff, qdiff
		r_differences.append(rdiff)
		q_differences.append(qdiff)



	r_differences = sorted(r_differences)
	q_differences = sorted(q_differences)


	rcaps.append(r_differences[int(threshold * size) - 1] / 10.0)
	qcaps.append(q_differences[int(threshold * size) - 1])


xs = np.arange(10, length + 1, 1)

f, ax = plot.subplots(1, 2)
ax[0].plot(xs, rcaps, label='learning speed difference')
ax[1].plot(xs, qcaps, label='quality difference')

ax[0].legend(bbox_to_anchor=(1, 0.7))
ax[1].legend(bbox_to_anchor=(1, 0.7))

ax[0].set_xlabel('tasks')
ax[1].set_xlabel('tasks')
ax[0].set_ylabel('difference')
ax[1].set_ylabel('difference')

plot.show()



