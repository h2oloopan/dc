import sys
import numpy as np
import matplotlib.pyplot as plot
import simulate
import learn
import random
import algorithm
from another import System



def resetWorkers(workers):
	for worker in workers:
		worker.reset()

def analyze(graph, runs, steps, algorithm, tasks, outcomes, workers, parameters):
	total_ws = []
	total_cs = []
	cs = []
	qs = []
	ws = []

	#print tasks

	for i in range(0, runs):
		resetWorkers(workers)
		answers = algorithm(tasks, outcomes, workers, parameters)
		#print answers
		#print tasks
		#print answers
		#print tasks
		#print answers
		for i in range(0, len(tasks)):
			if i >= len(ws):
				ws.append(answers[i][1])
			else:
				ws[i] += answers[i][1]

			if answers[i][0] == tasks[i]:
				if i >= len(cs):
					cs.append(1)
				else:
					cs[i] += 1
			else:
				if i >= len(cs):
					cs.append(0)

	#print cs
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
		qs.append(float(avg) / (float(runs) * float(count)))



	cumulative = 0
	cumulative_worker = 0
	for i in range(0, len(cs)):		
		cs[i] = cs[i] + cumulative
		total_cs.append(cs[i] / runs)
		#total_ws.append(k * (i + 1))
		cumulative = cs[i]
		cumulative_worker += ws[i]


		if i == len(cs) - 1:
			print cs[i] / runs
			print cumulative_worker / runs

		cs[i] = float(cs[i]) / (float(runs) * float(i + 1))
		ws[i] = float(ws[i]) / float(runs)

	#print cs
	#print qs


	#labels


	xs = np.arange(1, len(tasks) + 1, 1)
	graph[0].plot(xs, cs, label='cumulative quality')
	graph[0].plot(xs, qs, label='quality')
	#graph[1].plot(total_ws, total_cs)
	graph[1].plot(xs, ws, label='number of hired workers')

	graph[0].legend(bbox_to_anchor=(1, 0.3))
	graph[1].legend(bbox_to_anchor=(1, 0.8))

	graph[0].set_xlabel('tasks')
	graph[0].set_ylabel('accuracy')
	graph[0].axis([0, 1000, 0.0, 1.0])
	graph[0].set_autoscale_on(False)

	graph[1].set_xlabel('tasks')
	graph[1].set_ylabel('workers')	
	graph[1].axis([0, 1000, 0.0, 5.0])
	graph[1].set_autoscale_on(False)


if __name__ == '__main__':
	#r1 = {'mu': 2000, 'sigma': 10}
	#p1 = {'mu': 2000, 'sigma': 10}

	#r2 = {'mu': 50, 'sigma': 5}
	#p2 = {'mu': 20, 'sigma': 1}

	r = {'mu': 600, 'sigma': 5}
	p = {'mu': 800, 'sigma': 5}
	a = {'mu': 0.05, 'sigma': 0.04}

	workers = simulate.createHyperbolicWorker(80, r, p, None, 1)

	r2 = {'mu': 60, 'sigma': 5}
	p2 = {'mu': 40, 'sigma': 5}
	a2 = {'mu': 0.5, 'sigma': 0.05}

	r3 = {'mu': 50, 'sigma': 10}
	p3 = {'mu': 60, 'sigma': 10}
	a3 = {'mu': 0.05, 'sigma': 0.04}

	r4 = {'mu': 100, 'sigma': 10}
	p4 = {'mu': 70, 'sigma': 10}
	a4 = {'mu': 0.5, 'sigma': 0.05}

	#workers = simulate.createHyperbolicWorker(900, r1, p1, None, 1)
	fast_workers = simulate.createHyperbolicWorker(20, r2, p2, None, 2)
	workers.extend(fast_workers)

	#available_workers = simulate.createHyperbolicWorker(100, r2, p2, a2, 1)
	#workers.extend(available_workers)

	#extra2 = simulate.createHyperbolicWorker(33, r2, p2, a2, 1)
	#extra3 = simulate.createHyperbolicWorker(50, r3, p3, a3, 1)
	#extra4 = simulate.createHyperbolicWorker(33, r4, p4, a4, 1)

	#workers.extend(extra2)
	#workers.extend(extra3)
	#workers.extend(extra4)

	tasks = simulate.createBinaryTasks(1000)
	outcomes = [True, False]
	steps = 4
	runs = 30


	f, ax = plot.subplots(3, 2)
	#f, graphs = plot.subplots(1, 2)


	print 'Random K'
	k = 3
	analyze(ax[0], runs, steps, algorithm.randomK, tasks, outcomes, workers, k)



	print 'Top K'
	k = 3
	t = 20
	analyze(ax[1], runs, steps, algorithm.topKAverageWithTutorials, tasks, outcomes, workers, [k, t])


	print 'Dynamic Hiring'
	##system = System(outcomes, 1000, {'belief' : 7.0, 'quality': 400.0})
	system = System(outcomes, 1000, {'belief' : 7.0, 'quality': 500.0})
	horizon = 5
	samples = 512
	tutorials = 20
	analyze(ax[2], runs, steps, system.dh, tasks, outcomes, workers, [horizon, samples, tutorials])

	plot.show()









