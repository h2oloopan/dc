from scipy import stats

#learning module
def learnCurve(cs, ts):
	#cs is a list of number of correct answers
	#ts is a list of total number of tasks
	qs = cs / ts
	zs = 1 / (1 - qs)

	slope, intercept, r_value, p_value, std_err = stats.linregress(ts, zs)

	r = 1 / slope
	p = (intercept - 1) * r

	result = {'r': r, 'p': p, 'e': std_err, 'rv': r_value, 'pv': p_value}

	return result