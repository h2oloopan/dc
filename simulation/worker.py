class Worker:
	#learning curve
	x = 0 #tasks has completed
	p = 0 #prior quality
	r = 0 #time to reach 1/2 quality
	c = 0 #cost to hire
	def getQuality(self):
		#get current quality
		return (self.x + self.p) / (self.x + self.p + self.r)

