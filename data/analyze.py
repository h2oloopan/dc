import csv
import numpy as np
import matplotlib.pyplot as plot
import os
import sys

sys.path.append('../simulation')
from worker import Worker
import learn

expert = []
workers = []

start = 280.0
end = 1080.0
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

#precision analysis
precisions = []
maximum = 0
for worker in workers:
	precision = []
	correctness = 0
	counter = 0
	for spindle in worker:
		for truth in expert:
			if overlap(spindle, truth):
				correctness += 1
				break
		counter += 1
		precision.append(float(correctness) / float(counter))
	precisions.append(precision)
	if len(precision) > maximum:
		maximum = len(precision)

xs = np.arange(1, maximum + 1, 1)

skip = 10
for precision in precisions:
	plot.plot(precision[skip:])

aggregate = []
for i in range(0, 45):
	total = 0.0
	counter = 0
	for precision in precisions:
		if len(precision) > i:
			total += precision[i]
			counter += 1
	aggregate.append(float(total) / float(counter))

plot.plot(aggregate, linestyle='-')
plot.show()







