from scipy import stats

import statsmodels.api as sm
import pandas
from pandas import DataFrame, Series

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

	#make sure we at least have more than 10 samples
	#print ts, zs
	slope, intercept, r_value, p_value, std_err = stats.linregress(ts[5:], zs[5:])

	#different linear regression tool
	#print slope, intercept, r_value, p_value, std_err
	#temp = sm.OLS(zs, sm.add_constant(ts)).fit()
	#print temp.summary()

	#print slope
	#print intercept
	#print ts
	#print zs
	#print slope
	#print intercept

	r = 1.0 / slope
	p = (intercept - 1.0) * r

	result = {'r': r, 'p': p, 'e': std_err, 'rv': r_value, 'pv': p_value}

	#print cs
	#print ts
	#print result
	#print result
	#print result
	return result
