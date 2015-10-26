import random
import learn
import math

class Worker:
	uuid = ''
	#learning curve
	x = 0 #tasks has completed
	p = 0 #prior quality
	r = 0 #time to reach 1/2 quality
	c = 0 #cost to hire
	a = 0 #availability
	m = 0 #money a worker has made
	er = 0
	ep = 0
	epv = 0
	ts = []
	cs = []
	noise_mu = None
	noise_sigma = None
	def __init__(self, uuid, x, p, r, c, a):
		self.uuid = uuid
		self.x = x
		self.p = p
		self.r = r
		self.c = c
		self.a = a
		#print x, p, r, c, a
	def __str__(self):
		s = ''
		s += 'quality: ' + self.getEstimatedQualityAtX(self.x)
		return s
	def calculateProjection(self, projection):
		#calculate the weights for ranking
		#projection = (self.getEstimatedCumulativeQuality(self.x + projection) * float(self.x + projection) -
			#self.getEstimatedCumulativeQuality(self.x) * float(self.x))
		#return 1.0 * self.getEstimatedQualityAtX(self.x) + 1.0 * (1 / self.er)

		#the first term is short term while the second term is long term

		projection = self.getEstimatedCumulativeQuality(self.x + projection)
		extra = 0.0
		if self.epv < math.pow(10, -10):
			extra = 3.0
		return 2.0 * self.getEstimatedQualityAtX(self.x) + 1.0 * projection + extra

	def addNoise(self, noise_mu, noise_sigma):
		self.noise_mu = noise_mu
		self.noise_sigma = noise_sigma
	def updateLearning(self, c):
		#if c is True worker made a correct prediction, incorrect otherwise
		if len(self.ts) == 0:
			self.ts.append(1)
			if c:
				self.cs.append(1)
			else:
				self.cs.append(0)
		else:
			lastT = self.ts[-1]
			lastC = self.cs[-1]
			self.ts.append(lastT + 1)
			if c:
				self.cs.append(lastC + 1)
			else:
				self.cs.append(lastC)
	def learn(self):
		#print self.cs, self.ts
		learning = learn.learnCurve(self.cs, self.ts)
		#print learning
		if not math.isnan(learning['r']):
			#if it's too huge, just set it to 1000
			if learning['r'] > 1000.0:
				self.er = 1000.0
			else:
				if learning['r'] <= 0:
					self.er = 1000.0
				else:
					self.er = learning['r']
		else:
			self.er = 1000.0
		if not math.isnan(learning['p']):
			if learning['p'] < 0:
				self.ep = 0.0
			else:
				self.ep = learning['p']
		else:
			self.ep = 0.0
		self.epv = learning['pv']
		#print self.getEstimatedQualityAtX(self.x), self.getAveragedCumulativeQuality(), self.getQuality(), self.epv
	def getAveragedCumulativeQuality(self):
		return float(self.cs[-1]) / float(self.ts[-1])
	def getEstimatedCumulativeQuality(self, x):
		if self.er == 0:
			#hasn't even be able to learn the quality
			if len(self.ts) == 0:
				return 0.5
			elif x - 1 < len(self.ts):
				return float(cs[x-1]) / float(ts[x-1])
			else:
				return float(cs[-1]) / float(ts[-1])
		return (float(x) + float(self.ep)) / (float(x) + float(self.ep) + float(self.er))
	
	def getEstimatedQualityWithFilter(self):
		if self.er == 0 or self.epv > math.pow(10, -10):
			return self.getAveragedCumulativeQuality()
		else:
			return self.getEstimatedQualityAtX(self.x)

	def getEstimatedQualityAtX(self, x):
		if self.er == 0:
			return self.getEstimatedCumulativeQuality(x)
		return float(x) * self.getEstimatedCumulativeQuality(x) - (float(x) - 1.0) * self.getEstimatedCumulativeQuality(x - 1)
	def getCumulativeQuality(self, x):
		return (float(x) + float(self.p)) / (float(x) + float(self.p) + float(self.r))
	def getQuality(self):
		#get current quality
		return float(self.x) * self.getCumulativeQuality(self.x) - (float(self.x) - 1.0) * self.getCumulativeQuality(self.x - 1)
	def getQualityAtX(self, x):
		return float(x) * self.getCumulativeQuality(x) - (float(x) - 1.0) * self.getCumulativeQuality(x - 1)
	def isAvailable(self):
		rand = random.random()
		if rand >= self.a:
			return False
		else:
			return True
		return
	def doTask(self, task, outcomes, payment=0):
		self.x = self.x + 1
		self.m += payment
		rand = random.random()

		#add noise if needed
		if self.noise_mu is not None:
			print rand
			rand += random.gauss(self.noise_mu, self.noise_sigma)
			print rand

		if rand >= self.getQuality():
			others = list(outcomes)
			others.pop(others.index(task))
			pick = random.randint(0, len(others) - 1)
			return others[pick]
		else:
			return task

	def reset(self):
		self.x = 0
		self.m = 0
		self.er = 0
		self.ep = 0
		self.epv = 0
		self.ts = []
		self.cs = []


