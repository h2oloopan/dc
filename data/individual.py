import csv
import numpy as np
import matplotlib.pyplot as plot
import os
import sys
import statsmodels.api as sm
from scipy import stats
from dateutil import parser
import time
import datetime

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
			pair = [float(row['start']), float(row['end']), str(row['annotation_time'])]
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

names = []

#do actual work
for f in os.listdir('.'):
	if f.endswith('.csv'):
		if 'expert' not in f and 'notime' not in f: 
			worker = readData(f)
			workers.append(worker)
			names.append(f)
		elif 'expert' in f:
			expert = readData(f)


f, ax = plot.subplots(4, 3)
index = 0
for i in range(0, len(workers)):
	worker = workers[i]
	name = names[i]
	xs = []
	precisions = []
	recalls = []
	fscores = []
	cursor = 0
	step = 20
	end = 1080
	x = 0

	c_precision = 0
	c_recall = 0
	t_precision = 0
	t_recall = 0

	times = []
	timer = 0

	print name
	while cursor < end:
		range_start = cursor
		range_end = cursor + step

		#time
		previous_time = timer
		#precision
		for spindle in worker:
			if range_start <= spindle[0] and spindle[1] < range_end:
				#timestamp
				curTime = parser.parse(spindle[2])
				epoch = (curTime - datetime.datetime(1970, 1, 1)).total_seconds()
				if epoch > timer:
					timer = epoch

				for truth in expert:
					if overlap(truth, spindle):
						c_precision += 1
						break
				t_precision += 1
		precision = 0.0
		if t_precision != 0:
			precision = float(c_precision) / float(t_precision)

		times.append(timer - previous_time)
		previous_time = timer
		#print times[-1]

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
		x += 1
		xs.append(x)


	#plot
	#size = 25
	xs = xs[10:]
	ys = fscores[10:]


	max_estimated = 0
	min_estimated = 1

	max_average = 0
	min_average = 1

	last = ys[-1]

	for size in range(25, 44):
		x2l = list(xs)[0:size]
		y2l = list(ys)[0:size]
		zs = []
		for y in y2l:
			zs.append(1.0 / (1.0 - float(y)))

		slope, intercept, rvalue, pvalue, evalue = stats.linregress(x2l, zs)

		r = 1.0 / slope
		p = (intercept - 1.0) * r

		predict = float(xs[-1] + p) / float(xs[-1] + p + r)

		if predict > max_estimated:
			max_estimated = predict

		if predict < min_estimated:
			min_estimated = predict

		#print len(ys), size
		predict = ys[size]
		#print predict

		if predict > max_average:
			max_average = predict

		if predict < min_average:
			min_average = predict


	print last
	print min_estimated, max_estimated, (max_estimated - min_estimated) / last
	print min_average, max_average, (max_average - min_average) / last

#plot.show()




