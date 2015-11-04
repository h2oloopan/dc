import numpy as np
import simulate
import sys
import learn
import random
from worker import Worker
import matplotlib.pyplot as plot

r = {'mu': 50, 'sigma': 10}
p = {'mu': 65, 'sigma': 10}

length = 200
outcomes = [True, False]
tasks = simulate.createBinaryTasks(length)



workers = simulate.createHyperbolicWorker(1000, r, p, None, 1)


avgs = []
highs = []
estimates = []

for n in range(1, len(tasks) + 1, 2):
	highest_actual = 0.0
	highest_estimate = 0.0
	average = 0.0
	for worker in workers:
		worker.reset()
		for i in range(0, n):
			task = tasks[i]
			answer = worker.doTask(task, outcomes)
			if answer == task:
				worker.updateLearning(True)
			else:
				worker.updateLearning(False)
		worker.learn()
		if worker.getQuality() > highest_actual:
			highest_actual = worker.getQuality()
		if worker.getHybridQuality() > highest_estimate:
			highest_estimate = worker.getHybridQuality()
		average += worker.getQuality()
	average = average / len(workers)
	avgs.append(average)
	highs.append(highest_actual)
	estimates.append(highest_estimate)

xs = np.arange(1, length + 1, 2)

plot.xlabel('tasks')
plot.ylabel('quality')
plot.plot(xs, avgs, label='Average Quality')
plot.plot(xs, highs, label='Highest Worker Quality')
plot.plot(xs, estimates, label='Highest Estimated Quality')
plot.legend(bbox_to_anchor=(1, 0.3))
plot.show()