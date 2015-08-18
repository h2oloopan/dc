import sys
import uuid
import numpy as numpy
import matplotlib.pyplot as plot
import simulate
import learn
from worker import Worker


if __name__ == '__main__':
	print 'Regression Test'
	worker = Worker(str(uuid.uuid1()), 0, 5, 20, 1, 1)
	tasks = simulate.createBinaryTasks(1000)

	#initialize plots
	f, ax = plot.subplots(2, 2, sharex=True)

	cqs = [] #cumulative quality
	qs = [] #quality
	aqs = [] #average quality
	ecqs = [] #estimated by linear regression
	eqs = [] #estimated by linear regression
	count = 0
	for i in range(0, len(tasks)):
		task = tasks[i]
		answer = worker.doTask(task)
		if answer == task:
			count += 1
		cqs.append(worker.getCumulativeQuality(i + 1))
		qs.append(worker.getQuality())
		aqs.append(count / (i + 1))





