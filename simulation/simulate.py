import matplotlib.pyplot as pyplot
import scipy.stats as stats
import random
import uuid

from worker import Worker

def createBinaryTasks(n):
	tasks = []
	for i in range(0, n):
		sample = random.random()
		if sample >= 0.5:
			tasks.append(True)
		else:
			tasks.append(False)
	return tasks

def createHyperbolicWorker(n, r, c):
	#create n workers
	#r is the number of runs to reach 0.5 quality

	#create RS
	lower = 0
	upper = float('inf')
	mu = r
	sigma = 2
	RS = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
	rs = RS.rvs(n)
	#create XS in between 0 and 1
	lower = -0.5
	upper = 0.5
	mu = 0
	sigma = 0.1
	XS = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
	xs = XS.rvs(n) + 0.5

	ps = [(xs[i] * rs[i]) / (1 - xs[i]) for i in range(0, n)]
	#print rs

	#create availability
	lower = -0.5
	upper = 0.5
	mu = -0.2
	sigma = 1
	AS = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
	availabilities = AS.rvs(n) + 0.5

	workers = []
	for i in range(0, len(ps)):
		w = Worker(str(uuid.uuid1()), 0, ps[i], rs[i], c, availabilities[i])
		workers.append(w)

	return workers

