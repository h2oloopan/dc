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

#f, ax = plot.subplots(2)
cursor = 0
step = 20
end = 1080
recalls = []
xs = []
precisions = []
fscores = []
f2scores = []
correct_precision = 0
total_precision = 0
correct_recall = 0
total_recall = 0
total_truth = 0
x = 0
while cursor < end:
	range_start = cursor
	range_end = cursor + step
	
	#recall
	for truth in expert:
		if range_start <= truth[0] and truth[1] < range_end:
			total_truth += 1
			for worker in workers:
				for spindle in worker:
					if overlap(truth, spindle):
						correct_recall += 1

	recall = float(correct_recall) / float(len(workers) * total_truth)
	recalls.append(recall)

	#precision
	for worker in workers:
		for spindle in worker:
			if range_start <= spindle[0] and spindle[1] < range_end:
				for truth in expert:
					if overlap(truth, spindle):
						correct_precision += 1
						break
				total_precision += 1
	precision = 0.0
	if total_precision != 0:
		precision = float(correct_precision) / float(total_precision)
	precisions.append(precision)

	fscore = 2.0 * precision * recall / (precision + recall)
	f2score = 5.0 * precision * recall / (4.0 * precision + recall)

	fscores.append(fscore)
	f2scores.append(f2score)

	cursor += step
	x += 1
	xs.append(x)



xs = xs[10:]
#ys = recalls[10:]
#zs = []
#for y in ys:
#	zs.append(1.0 / (1.0 - float(y)))


#slope, intercept, r_value, p_value, std_err = stats.linregress(xs, zs)

#r = 1.0 / slope
#p = (intercept - 1.0) * r

#print r, p, p_value, std_err

#curve = []
#for x in xs:
#	curve.append(float(x + p) / float(x + p + r))



f, g = plot.subplots(1, 2)

yF1 = fscores[10:]
yF2 = f2scores[10:]

zF1 = []
zF2 = []

for y in yF1:
	zF1.append(1.0 / (1.0 - float(y)))
for y in yF2:
	zF2.append(1.0 / (1.0 - float(y)))

s1, i1, rv1, pv1, e1 = stats.linregress(xs, zF1)
s2, i2, rv2, pv2, e2 = stats.linregress(xs, zF2)

r1 = 1.0 / s1
p1 = (i1 - 1.0) * r1

r2 = 1.0 / s2
p2 = (i2 - 1.0) * r2


c1 = []
c2 = []
for x in xs:
	c1.append(float(x + p1) / float(x + p1 + r1))
	c2.append(float(x + p2) / float(x + p2 + r2))


g[0].plot(xs, yF1, label='actual F1-score')
g[0].plot(xs, c1, label='estimated F1-score')
g[1].plot(xs, yF2, label='actual F2-score')
g[1].plot(xs, c2, label='estimated F2-score')

g[0].set_xlabel('windows')
g[0].set_ylabel('cumulative F1-score')
g[0].legend(bbox_to_anchor=(1, 0.3))
g[1].set_xlabel('windows')
g[1].set_ylabel('cumulative f2-score')
g[1].legend(bbox_to_anchor=(1, 0.3))

print r1, p1, pv1, e1
print r2, p2, pv2, e2


#plot.plot(xs, ys, label='actual recall')
#plot.plot(xs, curve, label='estimated recall')
#plot.legend(bbox_to_anchor=(1, 0.3))
#plot.xlabel('windows')
#plot.ylabel('cumulative recall')
plot.show()







