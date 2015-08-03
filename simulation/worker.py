class Worker:
	#learning curve
	x = 0 #tasks has completed
	p = 0 #prior quality
	r = 0 #time to reach 1/2 quality
	c = 0 #cost to hire
	a = 0 #availability
	def __init__(self, x, p, r, c, a):
		self.x = x
		self.p = p
		self.r = r
		self.c = c
		self.a = a
		#print x, p, r, c, a
	def getQuality(self):
		#get current quality
		return (self.x + self.p) / (self.x + self.p + self.r)
	def isAvailable(self):
		return
	def doTask(self):
		self.x = self.x + 1
		return

