import csv
import numpy as np
import matplotlib.pyplot as plot
import os
import sys
import algorithm


sys.path.append('../simulation')
import learn
from system import System
from person import Worker

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

def resetWorkers(workers):
	for worker in workers:
		worker.reset()

#do actual work
for f in os.listdir('.'):
	if f.endswith('.csv'):
		if 'expert' not in f:
			worker = readData(f)
			workers.append(worker)
		else:
			expert = readData(f)

people = []
for i in range(0, len(workers)):
	worker = Worker(i, 0, 1)
	worker.loadData(expert, workers[i])
	people.append(worker)



#analysis
f, ax = plot.subplots(3, 2)
outcomes = [True, False]

#k random 3
k = 3
resetWorkers(people)
answers = []
cs = []
qs = []
ws = []
for index in range(0, len(expert)):
	task = True
	availables = list(people)
	hired = 0
	votes = {}
	vote = None
	max_vote = 0
	while hired < k:
		pick = random.randint(0, len(availables) - 1)
		worker = availables[pick]
		answer = worker.doTask(index, task, outcomes)
		key = str(answer)
		votes.setdefault(key, 0)
		votes[key] += 1
		if votes[key] > max_vote:
			max_vote = votes[key]
			vote = answer
		availables.pop(pick)
		hired += 1
	answers.append(vote, k)




#k top 3


#dynamic hiring horizon 3









