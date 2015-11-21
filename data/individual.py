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
	cursor = 0
	step = 20
	end = 1080
	x = 0

	while cursor < end:
		range_start = cursor
		range_end = cursor + step

		#precision
		for spindle in worker:
			if range


		#recall

		cursor += stop
		x += 1
		xs.append(x)

	#plot
	ax[index / 5][index % 5]
	index += 1






