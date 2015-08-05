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
	lower = -0.5
	upper = 0.5
	mu = 0
	sigma = 0.1
	
	X = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)

	samples = X.rvs(n) + 0.5
	ps = (samples * r) / (1 - samples)
	#ps are initial qualities

	availabilities = X.rvs(n) + 0.5

	workers = []
	for i in range(0, len(ps)):
		w = Worker(str(uuid.uuid1()), 0, ps[i], r, c, availabilities[i])
		workers.append(w)

	return workers

