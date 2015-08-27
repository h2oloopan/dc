import sys
import uuid
import numpy as np
import matplotlib.pyplot as plot
import simulate
import learn
import random
from worker import Worker

if __name__ == '__main__':
	p = 0
	r_start = 1
	r_end = 200
	runs = 1
	horizon = 100
	threshold = 0.01

	tasks = simulate.createBinaryTasks(horizon)

	ys1 = []
	ys2 = []
	for r in range(r_start, r_end + 1):
		total = 0
		ts = []
		cs = []
		count = 0
		worker = Worker(str(uuid.uuid1()), 0, p, r, 1, 1)
		for i in range(0, runs):
			for j in range(0, horizon):
				task = tasks[j]
				answer = worker.doTask(task)
				if answer == task:
					count += 1
				ts.append(j + 1)
				cs.append(count)
				learning = learn.learnCurve(cs, ts)
				err = learning['e']
				if err < threshold:
					total += j + 1
					break
		ys.append(float(total) / float(runs))

		

	xs = np.arange(r_start, r_end + 1, 1)

	f, (ax, bx) = plot.subplots(1, 2)
	ax.plot(xs, ys)
	plot.show()



		
