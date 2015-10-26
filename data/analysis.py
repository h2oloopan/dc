import csv
import numpy as np
import matplotlib.pyplot as plot

expert = []
alex = []
jeff = []
sarah = []
will = []

#doing all the reading

with open('expert.csv') as csvExpert:
	reader = csv.DictReader(csvExpert)
	for row in reader:
		#print row['start'], row['end']
		pair = [float(row['start']), float(row['end'])]
		expert.append(pair)

with open('alex.csv') as csvAlex:
	reader = csv.DictReader(csvAlex)
	for row in reader:
		pair = [float(row['start']), float(row['end'])]
		alex.append(pair)

with open('jeff.csv') as csvJeff:
	reader = csv.DictReader(csvJeff)
	for row in reader:
		pair = [float(row['start']), float(row['end'])]
		jeff.append(pair)

with open('sarah.csv') as csvSarah:
	reader = csv.DictReader(csvSarah)
	for row in reader:
		pair = [float(row['start']), float(row['end'])]
		sarah.append(pair)

with open('will.csv') as csvWill:
	reader = csv.DictReader(csvWill)
	for row in reader:
		pair = [float(row['start']), float(row['end'])]
		will.append(pair)



start = 280.0
end = 1080.0
step = 20.0

def overlap(p1, p2):
	if p1[0] < p2[0] and p2[0] < p1[1]:
		return True
	elif p1[0] < p2[1] and p2[1] < p1[1]:
		return True
	elif p2[0] < p1[0] and p1[1] < p2[1]:
		return True
	else:
		return False


def analyze(expert, alex, graph):
	#alex
	time_cursor = start
	expert_cursor = 0
	alex_cursor = 0

	right = []
	wrong = []
	spindles = []
	precisions = []
	recalls = []
	accuracies = []


	precision_result = []
	precision_count = []
	recall_result = []
	recall_count = []


	while time_cursor < end:
		expert_picks = []
		alex_picks = []
		while True:
			if expert_cursor < len(expert) and expert[expert_cursor][0] < time_cursor + step:
				expert_picks.append(expert[expert_cursor])
				expert_cursor += 1
			else:
				break
		while True:
			if alex_cursor < len(alex) and alex[alex_cursor][0] < time_cursor + step:
				alex_picks.append(alex[alex_cursor])
				alex_cursor += 1
			else:
				break
		correctness = 0
		wrongness = 0
		pness = 0
		rness = 0

		tp = 0
		tn = 0
		fp = 0
		fn = 0

		for ep in expert_picks:
			if len(recall_count) == 0:
				recall_count.append(1)
			else:
				recall_count.append(recall_count[-1] + 1)

			found = False
			for ap in alex_picks:
				if overlap(ep, ap):
					found = True
			if found:
				correctness += 1
				rness += 1
				if len(recall_result) == 0:
					recall_result.append(1)
				else:
					recall_result.append(recall_result[-1] + 1)
			else:
				wrongness += 1
				if len(recall_result) == 0:
					recall_result.append(0)
				else:
					recall_result.append(recall_result[-1] + 0)
		for ap in alex_picks:
			if len(precision_count) == 0:
				precision_count.append(1)
			else:
				precision_count.append(precision_count[-1] + 1)

			found = False
			for ep in expert_picks:
				if overlap(ap, ep):
					found = True
			if not found:
				wrongness += 1
				if len(precision_result) == 0:
					precision_result.append(0)
				else:
					precision_result.append(precision_result[-1] + 0)
			else:
				pness += 1
				tp += 1
				if len(precision_result) == 0:
					precision_result.append(1)
				else:
					precision_result.append(precision_result[-1] + 1)

		right.append(correctness)
		wrong.append(wrongness)
		spindles.append(len(expert_picks))


		if len(alex_picks) == 0 and len(expert_picks) == 0:
			precisions.append(1.0)
		elif len(alex_picks) == 0:
			precisions.append(0.0)
		else:
			precisions.append(float(pness) / float(len(alex_picks)))

		if len(expert_picks) == 0 and len(alex_picks) == 0:
			recalls.append(1.0)
		elif len(expert_picks) == 0:
			recalls.append(0.0)
		else:
			recalls.append(float(rness) / float(len(expert_picks)))


		time_cursor += step

	#return spindles, right, wrong, precisions, recalls
	weight = 0.1

	percent = []
	cumulative = []
	fs = []
	total = 0.0

	c_precisions = []
	c_recalls = []
	t_precision = 0.0
	t_recall = 0.0

	for i in range(0, len(spindles)):
		s = float(spindles[i])
		r = float(right[i])
		w = float(wrong[i])
		precision = float(precisions[i])
		recall = float(recalls[i])
		#p = 0.0
		#if s == 0 and w > 0:
		#	p = 0.0
		#elif s == 0:
		#	p = 1.0
		#else:
		#	p = r / s - weight * w
		f = 0.0
		if precision + recall > 0:
			f = 2.0 * precision * recall / (precision + recall)
			#f = 1.25 * precision * recall / (0.25 * precision + recall)
		fs.append(f)

		total += f
		cumulative.append(total / float(i + 1))

		t_precision += precision
		c_precisions.append(t_precision / float(i + 1))

		t_recall += recall
		c_recalls.append(t_recall / float(i + 1))

	xs = np.arange(1, len(cumulative) + 1, 1)

	#graph[0].plot(xs, c_precisions)
	#graph[1].plot(xs, c_recalls)
	graph[2].plot(xs, cumulative)

	for i in range(0, len(precision_result)):
		precision_result[i] = float(precision_result[i]) / float(precision_count[i])

	for i in range(0, len(recall_result)):
		recall_result[i] = float(recall_result[i]) / float(recall_count[i])

	xps = np.arange(1, len(precision_result) + 1, 1)
	graph[0].plot(xps, precision_result)

	xrs = np.arange(1, len(recall_result) + 1, 1)
	graph[1].plot(xrs, recall_result)


f, ax = plot.subplots(4, 3)
analyze(expert, alex, ax[0])
analyze(expert, jeff, ax[1])
analyze(expert, sarah, ax[2])
analyze(expert, will, ax[3])

plot.show()

#right, wrong = analyze(expert, jeff)
#print right
#print wrong
#right, wrong = analyze(expert, sarah)
#print right
#print wrong
#right, wrong = analyze(expert, will)
#print right
#print wrong


















