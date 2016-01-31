import csv
import numpy as np
import matplotlib.pyplot as plot
import matplotlib
import os
import sys
from scipy import stats

sys.path.append('../simulation')
from worker import Worker
import learn

font = {
	'size': 18
}

matplotlib.rc('font', **font)
matplotlib.rc('legend', fontsize=14)

expert = []
workers = []

start = 280.0
end = 1060.0
step = 20.0

def readData(fname):
	result = []
	with open(fname) as csvFile:
		reader = csv.DictReader(csvFile)
		for row in reader:
			pair = [float(row['start']), float(row['end'])]
			result.append(pair)
	return result

def overlap(p1, p2):
	if p1[0] < p2[0] and p2[0] < p1[1]:
		return True
	elif p1[0] < p2[1] and p2[1] < p1[1]:
		return True
	elif p2[0] < p1[0] and p1[1] < p2[1]:
		return True
	else:
		return False


#do actual work
for f in os.listdir('.'):
	if f.endswith('.csv'):
		if 'expert' not in f and '_' in f:
			worker = readData(f)
			workers.append(worker)
		else:
			expert = readData(f)


f, ax = plot.subplots(2, 5)
index = 0
for worker in workers:
	cursor = 0
	step = 20
	end = 1080


	cumulative_precision = 0
	cumulative_precision_total = 0
	cumulative_recall = 0
	cumulative_recall_total = 0

	cps = []
	crs = []
	cfs = []

	#cumulative stuff
	while cursor < end:
		range_start = cursor
		range_end = cursor + step

		#precision
		for spindle in worker:
			if range_start <= spindle[0] and spindle[1] < range_end:
				for truth in expert:
					if overlap(truth, spindle):
						cumulative_precision += 1
						break
				cumulative_precision_total += 1
		precision = 0.0
		if cumulative_precision_total != 0:
			precision = float(cumulative_precision) / float(cumulative_precision_total)

		#recall
		for truth in expert:
			if range_start <= truth[0] and truth[1] < range_end:
				for spindle in worker:
					if overlap(truth, spindle):
						cumulative_recall += 1
						break
				cumulative_recall_total += 1

		recall = 0.0
		if cumulative_recall_total != 0:
			recall = float(cumulative_recall) / float(cumulative_recall_total)

		#fscore
		fscore = 0.0
		if precision + recall > 0:
			fscore = 2.0 * precision * recall / (precision + recall)

		cps.append(precision)
		crs.append(recall)
		cfs.append(fscore)

		cursor += step

	#actual stuff
	cursor = 0
	precisions = []
	recalls = []
	fscores = []


	while cursor < end:
		range_start = cursor - 2 * step
		range_end = cursor + 3 * step

		c_precision = 0
		c_recall = 0
		t_precision = 0
		t_recall = 0

		#precision
		for spindle in worker:
			if range_start <= spindle[0] and spindle[1] < range_end:
				for truth in expert:
					if overlap(truth, spindle):
						c_precision += 1
						break
				t_precision += 1
		precision = 0.0
		if t_precision != 0:
			precision = float(c_precision) / float(t_precision)

		#recall
		for truth in expert:
			if range_start <= truth[0] and truth[1] < range_end:
				for spindle in worker:
					if overlap(truth, spindle):
						c_recall += 1
						break
				t_recall += 1

		recall = 0.0
		if t_recall != 0:
			recall = float(c_recall) / float(t_recall)

		#fscore
		fscore = 0.0
		if precision + recall > 0:
			fscore = 2.0 * precision * recall / (precision + recall)


		precisions.append(precision)
		recalls.append(recall)
		fscores.append(fscore)


		cursor += step


	xs = np.arange(1, len(cfs) + 1, 1)

	#plot
	xs = xs[10:]
	#ys = fscores[10:]
	#ys = fscores[10:]
	ys = cfs[10:]
	zs = []
	for y in ys:
		zs.append(1.0 / (1.0 - float(y)))

	slope, intercept, rvalue, pvalue, evalue = stats.linregress(xs[0:30], zs[0:30])

	r = 1.0 / slope
	p = (intercept - 1.0) * r


	print r, p, evalue, pvalue
	print '---'


	cs = []
	for x in xs:
		cq = float(x + p) / float(x + p + r)
		q = cq
		if x > 1:
			q = float(x) * cq - float(x - 1) * (float(x - 1 + p) / float(x - 1 + p + r)) 
		#cs.append(float(x + p) / float(x + p + r))
		cs.append(cq)

	print 'actual [45] ', cfs[44]
	print 'average [45] ', cfs[39]
	print 'projected [45] ', cs[34]

	print 'actual [55]', cfs[-1]
	print 'average [55]', cfs[39]
	print 'projected [55] ', cs[-1]




	print '---' 

	a = index / 5
	b = index % 5

	#ax[a][b].plot(xs, ys)
	#ax[a][b].plot(xs, fscores[10:])
	ax[a][b].plot(xs, cfs[10:], label='actual F1')
	ax[a][b].plot(xs, cs, 'b--', label='estimated F1')
	ax[a][b].legend(bbox_to_anchor=(1, 0.2))
	index += 1


plot.show()




