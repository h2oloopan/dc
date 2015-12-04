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


for f in os.listdir('.'):
	if f.endswith('.csv'):
		if 'expert' not in f:
			pass
		else:
			expert = readData(f)

workers.append(readData('A1T9IKE8GV4LR3.csv'))
workers.append(readData('A1YC558J4E5KZ.csv'))

f, ax = plot.subplots(1, 2)

worker = workers[0]
recalls = []
total = 0
correct = 0
for truth in expert:
	found = False
	for spindle in worker:
		if overlap(truth, spindle):
			found = True
			break
	if found:
		correct += 1
	else:
		correct += 0
	total += 1

	recall = 0.0
	if total > 0:
		recall = float(correct) / float(total)
	recalls.append(recall)

xs = np.arange(1, len(expert) + 1, 1)
ax[0].plot(xs, recalls)
ax[0].set_xlabel('tasks')
ax[0].set_ylabel('recall')

worker = workers[1]
recalls = []
total = 0
correct = 0
for truth in expert:
	found = False
	for spindle in worker:
		if overlap(truth, spindle):
			found = True
			break
	if found:
		correct += 1
	else:
		correct += 0
	total += 1

	recall = 0.0
	if total > 0:
		recall = float(correct) / float(total)
	recalls.append(recall)

ax[1].plot(xs, recalls)

plot.show()




