import sys
import uuid
import numpy as np
import matplotlib.pyplot as plot
import simulate
import learn
import random
from worker import Worker

if __name__ == '__main__':
	tasks = simulate.createBinaryTasks(800)

	p = 0
	r_start = 1
	r_end = 100
	runs = 5
	threshold = 0.1

	for r in range(r_start, r_end + 1):
		
