from scipy import stats

#learning module
def learnCurve(cs, ts):
	#cs is a list of number of correct answers
	#ts is a list of total number of tasks
	qs = cs / ts
	zs = 1 / (1 - qs)

	slope, intercept, r_value, p_value, std_err = stats.linregress(ts, zs)

	result = {}

	return result