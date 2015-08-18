import random


class Worker:
	uuid = ''
	#learning curve
	x = 0 #tasks has completed
	p = 0 #prior quality
	r = 0 #time to reach 1/2 quality
	c = 0 #cost to hire
	a = 0 #availability
	m = 0 #money a worker has made
	def __init__(self, uuid, x, p, r, c, a):
		self.uuid = uuid
		self.x = x
		self.p = p
		self.r = r
		self.c = c
		self.a = a
		#print x, p, r, c, a
	def getCumulativeQuality(self, x):
		return (float(x) + float(self.p)) / (float(x) + float(self.p) + float(self.r))
	def getQuality(self):
		#get current quality
		return float(self.x) * self.getCumulativeQuality(self.x) - (float(self.x) - 1.0) * self.getCumulativeQuality(float(self.x) - 1.0)
	def isAvailable(self):
		rand = random.random()
		if rand >= self.a:
			return False
		else:
			return True
		return
	def doTask(self, task, payment=0):
		self.x = self.x + 1
		self.m += payment
		rand = random.random()
		if rand >= self.getQuality():
			return not task
		else:
			return task
	def reset(self):
		self.x = 0


