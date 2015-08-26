import sys
import uuid
import numpy as np
import matplotlib.pyplot as plot
import simulate
import learn
import random
from worker import Worker


def getAnswer(task, p):
	rand = random.random()
	if rand >= p:
		return not task
	else:
		return task

def getCurves(worker, tasks, runs, prob):
	#the following two are always fixed
	cqs = [] #cumulative quality
	qs = [] #quality
	aqs = [] #average quality
	ecqs = [] #estimated by linear regression
	eqs = [] #estimated by linear regression
	fqs = []
	###for learning
	cs = []
	ts = []
	errs = []
	count = 0
	for i in range(0, len(tasks)):
		task = tasks[i]
		answer = worker.doTask(task)
		if answer == getAnswer(task, prob):
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
		errs.append(learning['e'])
		if i == 0:
			fqs.append(float(count) / float(i+1))
		else:
			fqs.append(float(i+1)*aqs[i] - float(i)*aqs[i-1])

	for j in range(0, runs - 1):
		worker.reset()
		count = 0
		cs = []
		ts = []
		for i in range(0, len(tasks)):
			task = tasks[i]
			answer = worker.doTask(task)
			if answer == getAnswer(task, prob):
				count += 1
			aqs[i] += float(count) / float(i + 1)
			ts.append(i + 1)
			cs.append(count)
			learning = learn.learnCurve(cs, ts)
			fake = Worker(str(uuid.uuid1()), i+1, learning['p'], learning['r'], 1, 1)
			ecqs[i] += fake.getCumulativeQuality(i+1)
			eqs[i] += fake.getQuality()
			errs[i] += learning['e']
			if i == 0:
				fqs[i] += (float(count) / float(i+1))
			else:
				fqs[i] += (float(i+1)*aqs[i] - float(i)*aqs[i-1])

	for i in range(0, len(tasks)):
		aqs[i] = aqs[i] / float(runs)
		ecqs[i] = ecqs[i] / float(runs)
		eqs[i] = eqs[i] / float(runs)
		errs[i] = errs[i] / float(runs)
		fqs[i] = fqs[i] / float(runs)


	result = {'cqs': cqs, 'qs': qs, 'aqs': aqs, 'ecqs': ecqs, 'eqs': eqs}
	return result

if __name__ == '__main__':
	print 'Regression Test'
	worker = Worker(str(uuid.uuid1()), 0, 5, 20, 1, 1)
	tasks = simulate.createBinaryTasks(800)
	

	c1 = getCurves(worker, tasks, 5, 1)
	c2 = getCurves(worker, tasks, 5, 0.9)
	c3 = getCurves(worker, tasks, 5, 0.8)
	c4 = getCurves(worker, tasks, 5, 0.7)

	#initialize plots
	#f, ax = plot.subplots(2, sharex=True)

	


	x = np.arange(1, len(tasks) + 1, 1)

	f, (bx, ax) = plot.subplots(1, 2)

	bx.set_title('Estimated vs. Averaged Quality, 80% Aggregate Accuracy')
	bx.grid(True)
	ba = bx.plot(x, c1['qs'], '-', label='actual quality')
	b8e = bx.plot(x, c3['eqs'], '--', label='estimated quality')
	b8a = bx.plot(x, c3['aqs'], '--', label='averaged quality')
	bx.legend(bbox_to_anchor=(1, 0.6))


	#ax1.xlabel('Number of Tasks')
	#ax1.ylabel('Quality')
	ax.set_title('Different Aggregate Accuracy')
	ax.grid(True)
	pa, = ax.plot(x, c1['qs'], '-', label='actual quality')
	p1, = ax.plot(x, c1['eqs'], '--', label='100% aggregate accuracy')
	p09, = ax.plot(x, c2['eqs'], '--', label='90% aggregate accuracy')
	p08, = ax.plot(x, c3['eqs'], '--', label='80% aggregate accuracy')
	p07, = ax.plot(x, c4['eqs'], '--', label='70% aggregate accuracy')
	ax.legend(bbox_to_anchor=(1,0.6))
	plot.show()

	#print eqs

	



