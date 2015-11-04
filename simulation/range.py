import numpy as np
import simulate
import sys
import learn
import random
from worker import Worker

r = {'mu': 50, 'sigma': 10}
p = {'mu': 65, 'sigma': 10}

length = 300
outcomes = [True, False]
tasks = simulate.createBinaryTasks(length)



workers = simulate.createHyperbolicWorker(1000, r, p, None, 1)

