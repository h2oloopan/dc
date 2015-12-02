import csv
import numpy as np
import matplotlib.pyplot as plot
import os
import sys
import random


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
steps = 5
xs = np.arange(1, len(expert) + 1, 1)

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
	answers.append(vote)
	
	if vote == task:
		cs.append(1)
	else:
		cs.append(0)
	ws.append(k)

for i in range(0, len(cs)):
	avg = cs[i]
	count = 1
	for j in range(1, steps + 1):
		if i - j >= 0:
			avg += cs[i - j]
			count += 1
		if i + j < len(cs):
			avg += cs[i + j]
			count += 1
	qs.append(float(avg) / float(count))

cumulative = 0
for i in range(0, len(cs)):
	cumulative += cs[i]
	cs[i] = float(cumulative) / float(i + 1)



ax[0][0].plot(xs, cs)
ax[0][0].plot(xs, qs)
ax[0][1].plot(xs, ws)



#k top 3
k = 3
resetWorkers(people)
answers = []
cs = []
qs = []
ws = []
t = 15 #number of tutorials

for worker in people:
	for index in range(0 ,t):
		task = True
		answer = worker.doTask(index, task, outcomes)
		if answer == task:
			worker.updateLearning(True)
		else:
			worker.updateLearning(False)


ranked = sorted(people, key=lambda worker: worker.getAveragedCumulativeQuality(), reverse=True)

for index in range(t, len(expert)):
	task = True
	hired = 0
	votes = {}
	vote = None
	max_vote = 0
	while hired < k:
		worker = ranked[hired]
		answer = worker.doTask(index, task, outcomes)
		key = str(answer)
		votes.setdefault(key, 0)
		votes[key] += 1
		if votes[key] > max_vote:
			max_vote = votes[key]
			vote = answer
		hired += 1
	answers.append(vote)
	
	if vote == task:
		cs.append(1)
	else:
		cs.append(0)
	ws.append(k)

for i in range(0, len(cs)):
	avg = cs[i]
	count = 1
	for j in range(1, steps + 1):
		if i - j >= 0:
			avg += cs[i - j]
			count += 1
		if i + j < len(cs):
			avg += cs[i + j]
			count += 1
	qs.append(float(avg) / float(count))

cumulative = 0
for i in range(0, len(cs)):
	cumulative += cs[i]
	cs[i] = float(cumulative) / float(i + 1)


xs = np.arange(1, len(expert) + 1 - t, 1)
ax[1][0].plot(xs, cs)
ax[1][0].plot(xs, qs)
ax[1][1].plot(xs, ws)

#dynamic hiring horizon 3
resetWorkers(people)
answers = []
cs = []
qs = []
ws = []
t = 15 #number of tutorials

for worker in people:
	for index in range(0 ,t):
		task = True
		answer = worker.doTask(index, task, outcomes)
		if answer == task:
			worker.updateLearning(True)
		else:
			worker.updateLearning(False)
	worker.learn()

system = System(outcomes, 1000, {'belief': 7.0, 'quality': 400.0})
horizon = 3
samples = 1024
tutorials = 0

answers = system.dhReal(t, expert, outcomes, people, [horizon, samples, tutorials])
print answers



plot.show()





