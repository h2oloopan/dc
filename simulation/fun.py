class ModModMod:
	def f(self, m, r, p):
		if p >= len(m):
			return (1 + r) * r / 2
		elif m[p] > r:
			return self.f(m, r, p + 1)
		elif m[p] == r:
			return self.f(m, r - 1, p + 1)
		else:
			cur = m[p]
			num_circles = r / cur
			remainder = r % cur
			result = num_circles * self.f(m, cur - 1, p + 1)
			#print '(%r %r %r) left %r' % (m, r, p, result) 
			if remainder > 0:
				result += self.f(m, remainder, p + 1)
				#print 'total', result
			return result
	def findSum(self, m, r):
		return self.f(m, r, 0)


if __name__ == '__main__':
	#m = [10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 9999999, 9999999, 9999998, 9999998, 9999997, 9999994, 9999993, 9999992, 9999989, 9999988, 9999988, 9999986, 9999986, 9999986, 9999983, 9999983, 9999982, 9999974, 9999971, 9999964, 9999964, 9999964, 9999962, 9999959, 9999959, 9999874, 9999872, 9999860, 9999856, 9999800, 9999783, 9999769, 9999722, 9999648, 9999611, 9999441, 9999374, 9999310, 9999076, 9998897, 9998896, 9998862, 9998555, 9998519, 9998397, 9998349, 9997844, 9997705, 9997479, 9997436, 9997026, 9996393, 9996157, 9994988, 9994225, 9993781, 9993773, 9993541, 9993049, 9983997, 9981876, 9976641, 9975642, 9975182, 9973087, 9970604, 9966793, 9965514, 9963966, 9963766, 9949265, 9938622, 9930199, 9923577, 9914828, 9913139, 9908311, 9899982, 9873612, 9862712, 9861235, 9849410, 9789914, 9764760, 9759326, 9738240, 9697498, 9691075, 9674016, 9613096, 9456432, 8880810, 8813859, 8491063, 8138611, 8126273, 7886166, 7866570, 7830901, 7550460, 7527037, 7289395, 6639620, 5291389, 5286081, 5233444, 2702602, 1964016, 820862]
	#R = 10000000
	m = [5, 3, 2]
	R = 10
	#m = [2934]
	#R = 10000000
	answer = ModModMod().findSum(m, R)
	print answer