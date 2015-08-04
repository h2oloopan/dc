import sys
import learn
import simulate
import algorithm

if __name__ == '__main__':
	print 'Simulation Test'
	workers = simulate.createWorker(1000, 100, 1)
	tasks = simulate.createBinaryTasks(1000)
	
	answers = algorithm.pickRandomly(tasks, workers, 5)

	#analyze answers
	