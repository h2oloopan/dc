from scipy import stats

#learning module
def learnCurve(cs, ts):
	#cs is a list of number of correct answers
	#ts is a list of total number of tasks
	qs = []
	zs = []


	for i in range(0, len(cs)):
		qs.append(float(cs[i]) / float(ts[i]))
		if qs[i] == 1:
			qs[i] = 0
		zs.append(1.0 / (1.0 - float(qs[i])))


	slope, intercept, r_value, p_value, std_err = stats.linregress(ts, zs)

	r = 1 / slope
	p = (intercept - 1) * r

	result = {'r': r, 'p': p, 'e': std_err, 'rv': r_value, 'pv': p_value}

	return result