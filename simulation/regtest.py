import sys
import uuid
import numpy as np
import matplotlib.pyplot as plot
import simulate
import learn
from worker import Worker


if __name__ == '__main__':
	print 'Regression Test'
	worker = Worker(str(uuid.uuid1()), 0, 5, 20, 1, 1)
	tasks = simulate.createBinaryTasks(10)

	#initialize plots
	f, ax = plot.subplots(1, 5, sharex=True, sharey=True)

	cqs = [] #cumulative quality
	qs = [] #quality
	aqs = [] #average quality
	ecqs = [] #estimated by linear regression
	eqs = [] #estimated by linear regression
	###for learning
	cs = []
	ts = []
	count = 0
	for i in range(0, len(tasks)):
		task = tasks[i]
		answer = worker.doTask(task)
		if answer == task:
			count += 1
		cqs.append(worker.getCumulativeQuality(i + 1))
		qs.append(worker.getQuality())
		aqs.append(float(count) / float(i + 1))
		#learn
		ts.append(i + 1)
		cs.append(count)
		learning = learn.learnCurve(cs, ts)
		fake = Worker(str(uuid.uuid1()), i+1, learning['p'], learning['r'], 1, 1)
		ecqs.append(fake.getCumulativeQuality(i+1))
		eqs.append(fake.getQuality())


	x = np.arange(1, len(tasks), 1)
	ax[0][0].plot(x, cqs)
	ax[0][1].plot(x, qs)
	ax[0][2].plot(x, aqs)
	ax[0][3].plot(x, ecqs)
	ax[0][4].plot(x, eqs)
	plot.show()

	



