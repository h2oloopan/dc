#learning module
def learnCurve(curve, point):
	#use regression to learn the hyperbolic learning curve
	#the curve is y(x) = (x + p) / (x + p + r) p is the initial quality and r is the learning rate
	#linear regression to learn the linearly transformed curve first
	#then convert back to the hyperbolic form