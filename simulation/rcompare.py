import sys
import uuid
import numpy as np
import matplotlib.pyplot as plot
import simulate
import learn
import random
import math
from worker import Worker

if __name__ == '__main__':
	p = 0
	r_start = 1
	r_end = 200
	runs = 100
	horizon = 200
	threshold = 0.01

	tasks = simulate.createBinaryTasks(horizon)

	ys1 = []
	ys2 = []
	for r in range(r_start, r_end + 1):
		total = 0
		maximum = 0
		count = 0
		worker = Worker(str(uuid.uuid1()), 0, p, r, 1, 1)
		for i in range(0, runs):
			ts = []
			cs = []
			for j in range(0, horizon):
				task = tasks[j]
				answer = worker.doTask(task)
				if answer == task:
					count += 1
				ts.append(j + 1)
				cs.append(count)
				learning = learn.learnCurve(cs, ts)
				err = learning['e']
				#print err
				#print learning['r']
				if math.isnan(err):
					continue
				if err < threshold:
					total += j + 1
					if j + 1 > maximum:
						maximum = j + 1
					break
		ys1.append(float(total) / float(runs))
		ys2.append(maximum)

	xs = np.arange(r_start, r_end + 1, 1)

	f, (ax, bx) = plot.subplots(1, 2)
	ax.set_title('Averaged across 100 runs')
	ax.set_xlabel('r')
	ax.set_ylabel('tasks')
	ax.plot(xs, ys1)
	bx.set_title('Maximum  in 100 Runs')
	bx.set_xlabel('r')
	bx.set_ylabel('tasks')
	bx.plot(xs, ys2)
	plot.show()



		
