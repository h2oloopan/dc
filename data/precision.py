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
precisions = []
xs = []
correct = 0
total = 0
cumulative_precision = 0.0
x = 0
while cursor < end:
	range_start = cursor
	range_end = cursor + step
	cur_correct = 0
	cur_total = 0
	for worker in workers:
		for spindle in worker:
			if range_start <= spindle[0] and spindle[1] < range_end:
				for truth in expert:
					if overlap(truth, spindle):
						correct += 1
						cur_correct += 1
						break
				total += 1
				cur_total += 1

	#cur_precision = float(cur_correct) / float(cur_total)
	#cumulative_precision = (float(x) * cumulative_precision + cur_precision) / float(x + 1)

	if total == 0:
		precisions.append(0.0)
	else:
		precisions.append(float(correct) / float(total))
	
	cursor += step
	x += 1
	xs.append(x)



xs = xs[10:]
ys = precisions[10:]
zs = []
for y in ys:
	zs.append(1.0 / (1.0 - float(y)))


slope, intercept, r_value, p_value, std_err = stats.linregress(xs, zs)

r = 1.0 / slope
p = (intercept - 1.0) * r

print r, p, p_value, std_err

curve = []
for x in xs:
	curve.append(float(x + p) / float(x + p + r))


plot.plot(xs, ys, label='actual precision')
plot.plot(xs, curve, label='estimated precision')
plot.legend(bbox_to_anchor=(1, 0.3))
plot.xlabel('windows')
plot.ylabel('cumulative precision')
plot.show()







