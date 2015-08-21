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
	tasks = simulate.createBinaryTasks(200)
	total = 10

	#initialize plots
	#f, ax = plot.subplots(2, sharex=True)

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
		errs.append(learning['e'])
		if i == 0:
			fqs.append(float(count) / float(i+1))
		else:
			fqs.append(float(i+1)*aqs[i] - float(i)*aqs[i-1])

	for j in range(0, total - 1):
		worker.reset()
		count = 0
		cs = []
		ts = []
		for i in range(0, len(tasks)):
			task = tasks[i]
			answer = worker.doTask(task)
			if answer == task:
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
		aqs[i] = aqs[i] / float(total)
		ecqs[i] = ecqs[i] / float(total)
		eqs[i] = eqs[i] / float(total)
		errs[i] = errs[i] / float(total)
		fqs[i] = fqs[i] / float(total)


	x = np.arange(1, len(tasks) + 1, 1)

	f, (ax1, ax2) = plot.subplots(1, 2)
	#ax1.xlabel('Number of Tasks')
	#ax1.ylabel('Quality')
	ax1.set_title('Quality Comparison')
	ax1.grid(True)
	laq, = ax1.plot(x, qs, '-', label='actual quality')
	leq, = ax1.plot(x, eqs, '--', label='estimated quality')
	lavq, = ax1.plot(x, aqs, ':', label='averaged quality')
	ax1.legend([laq, leq, lavq], bbox_to_anchor=(1,0.6))

	ax2.set_title('Linear Regression Error')
	lre, = ax2.plot(x, errs, label='error')
	ax2.legend([lre], bbox_to_anchor=(1, 0.6))
	plot.show()

	#print eqs

	



