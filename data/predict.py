import csv
import numpy as np
import matplotlib.pyplot as plot
import os
import sys
import statsmodels.api as sm
from scipy import stats

sys.path.append('../simulation')
from worker import Worker
import learn

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
		if 'expert' not in f:
			worker = readData(f)
			workers.append(worker)
		else:
			expert = readData(f)


f, ax = plot.subplots(2, 5)
index = 0
for worker in workers:
	xs = []
	precisions = []
	recalls = []
	fscores = []
	cursor = 0
	step = 20
	end = 1080
	x = 0


	cumulative_precision = 0
	cumulative_precision_total = 0
	cumulative_recall = 0
	cumulative_recall_total = 0

	cps = []
	crs = []
	cfs = []

	#cumulative stuff



	#actual stuff


	while cursor < end:
		range_start = cursor - step
		range_end = cursor + step + step

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
						cumulative_precision += 1
						break
				t_precision += 1
				cumulative_recall_total += 1
		precision = 0.0
		if t_precision != 0:
			precision = float(c_precision) / float(t_precision)

		cp = 0.0
		if cumulative_precision_total != 0:
			cp = float(cumulative_precision) / float(cumulative_precision_total)

		#recall
		for truth in expert:
			if range_start <= truth[0] and truth[1] < range_end:
				for spindle in worker:
					if overlap(truth, spindle):
						c_recall += 1
						cumulative_recall += 1
						break
				t_recall += 1
				cumulative_recall_total += 1

		recall = 0.0
		if t_recall != 0:
			recall = float(c_recall) / float(t_recall)

		cr = 0.0
		if cumulative_recall_total != 0:
			cr = float(cumulative_recall) / float(cumulative_recall_total)

		#fscore
		fscore = 0.0
		if precision + recall > 0:
			fscore = 2.0 * precision * recall / (precision + recall)

		cf = 0.0
		if cp + cr > 0:
			cf = 2.0 * cp * cr / (cp + cr)

		precisions.append(precision)
		recalls.append(recall)
		fscores.append(fscore)

		cps.append(cp)
		crs.append(cr)
		cfs.append(cf)

		cursor += step
		x += 1
		xs.append(x)

	#plot
	xs = xs[10:]
	#ys = fscores[10:]
	#ys = fscores[10:]
	ys = cfs[10:]
	zs = []
	for y in ys:
		zs.append(1.0 / (1.0 - float(y)))

	slope, intercept, rvalue, pvalue, evalue = stats.linregress(xs[0:20], zs[0:20])

	r = 1.0 / slope
	p = (intercept - 1.0) * r


	print r, p, evalue, pvalue

	cs = []
	for x in xs:
		cq = float(x + p) / float(x + p + r)
		q = cq
		if x > 1:
			q = float(x) * cq - float(x - 1) * (float(x - 1 + p) / float(x - 1 + p + r)) 
		#cs.append(float(x + p) / float(x + p + r))
		cs.append(q)


	a = index / 5
	b = index % 5

	ax[a][b].plot(xs, ys)
	ax[a][b].plot(xs, cs)
	index += 1

plot.show()




