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

def createHyperbolicWorker(n, r, p, v, c):
	#create n workers
	#r is the number of runs to reach 0.5 quality

	#create RS
	lower = 0
	upper = float('inf')
	mu = r['mu']
	sigma = r['sigma']
	RS = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
	rs = RS.rvs(n)
	#create XS in between 0 and 1
	lower = 0
	upper = float('inf')
	mu = p['mu']
	sigma = p['sigma']
	PS = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
	ps = PS.rvs(n)

	#create availability
	lower = 0
	upper = 1
	mu = v['mu']
	sigma = v['sigma']
	VS = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
	vs = VS.rvs(n)

	workers = []
	for i in range(0, len(ps)):
		w = Worker(str(uuid.uuid1()), 0, ps[i], rs[i], c, vs[i])
		workers.append(w)

	return workers

