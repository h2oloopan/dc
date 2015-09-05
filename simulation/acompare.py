import sys
import numpy as np
import matplotlib.pyplot as plot
import simulate
import learn
import random
import algorithm
from system import System
from worker import Worker



def resetWorkers(workers):
	for worker in workers:
		worker.reset()

if __name__ == '__main__':
	r = {'mu': 10, 'sigma': 2.5}
	p = {'mu': 5, 'sigma': 1}

	workers = simulate.createHyperbolicWorker(100, r, p, None, 1)
	tasks = simulate.createBinaryTasks(1000)
	outcomes = [True, False]

	runs = 5


	f, ax = plot.subplots(2, 2)

	print 'Random K'
	for i in range(0, runs):
		
