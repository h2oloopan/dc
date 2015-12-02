#real worker
import random
import learn
import math

class Worker:
	def __init__(self, uuid, x, c):
		self.uuid = uuid
		self.x = x
		self.c = c
		self.er = 0.0
		self.ep = 0.0
		self.m = 0.0
		self.ts = []
		self.cs = []
		self.expert = []
		self.myself = []
	def loadData(self, expert, myself):
		self.expert = expert
		self.myself = myself
	def calculateProjection(self, quality, projection):
		projection = self.getEstimatedQualityAtX(self.x + projection)
		return 1.0 * quality + 1.0 * projection
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
			if learning['r'] > 500.0:
				self.er = 500.0
			else:
				if learning['r'] <= 0:
					self.er = 500.0
				else:
					self.er = learning['r']
			self.epv = learning['pv']
			self.erv = learning['rv']
		else:
			self.er = 500.0
			self.epv = 1.0
			self.erv = 1.0
		if not math.isnan(learning['p']):
			if learning['p'] < 0:
				self.ep = 0.0
			else:
				self.ep = learning['p']
		else:
			self.ep = 0.0
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
	def getHybridQuality(self):
		if self.er == 0 or self.erv < 0:
			return self.getAveragedCumulativeQuality()
		elif self.erv > 0.4:
			return (self.getAveragedCumulativeQuality() + self.getEstimatedQualityAtX(self.x)) / 2.0
		else:
			return self.getEstimatedQualityAtX(self.x)
	def getEstimatedQualityAtX(self, x):
		if self.x == 0:
			return self.getDefaultQualityAtX(x)
		if self.er == 0:
			return self.getEstimatedCumulativeQuality(x)
		return float(x) * self.getEstimatedCumulativeQuality(x) - (float(x) - 1.0) * self.getEstimatedCumulativeQuality(x - 1)
	def overlap(self, p1, p2):
		if p1[0] < p2[0] and p2[0] < p1[1]:
			return True
		elif p1[0] < p2[1] and p2[1] < p1[1]:
			return True
		elif p2[0] < p1[0] and p1[1] < p2[1]:
			return True
		else:
			return False
	def doTask(self, index, task, outcomes, payment=0):
		self.x = self.x + 1
		self.m += payment

		task = self.expert[index]
		answer = False
		for opinion in self.myself:
			if self.overlap(opinion, task):
				answer = True
				break
		return answer
	def reset(self):
		self.x = 0
		self.m = 0
		self.er = 0
		self.ep = 0
		self.ts = []
		self.cs = []
				














