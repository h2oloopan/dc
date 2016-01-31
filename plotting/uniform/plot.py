import numpy as np
import matplotlib.pyplot as plot
import matplotlib
import json

total = 81
xs = np.arange(1, 1001, 1)

font = {
	'size': 18
}

matplotlib.rc('font', **font)

f, ax = plot.subplots(3, 2)

#random k

with open('rk.json') as inputfile:
	data = json.load(inputfile)

cs = data['cs']
qs = data['qs']
ws = data['ws']
#cumulative = data['cumulative']
#correct = data['correct']
#hired = data['hired']

ax[0][0].plot(xs, cs, label='cumulative quality')
ax[0][0].plot(xs, qs, 'b-.', label='quality')
ax[0][1].plot(xs, ws, label='number of workers')
ax[0][0].set_xlabel('tasks')
ax[0][0].set_ylabel('recall')
ax[0][1].set_xlabel('tasks')
ax[0][1].set_ylabel('workers')
ax[0][0].legend(bbox_to_anchor=(1, 0.5))
ax[0][1].legend(bbox_to_anchor=(1, 0.9))
ax[0][0].axis([0, 1000, 0.0, 1.0])
ax[0][0].set_autoscale_on(False)
ax[0][1].axis([0, 1000, 0.0, 5.0])
ax[0][1].set_autoscale_on(False)

#print cumulative
#print correct
#print hired

#top k

with open('tk.json') as inputfile:
	data = json.load(inputfile)

cs = data['cs']
qs = data['qs']
ws = data['ws']
#cumulative = data['cumulative']
#correct = data['correct']
#hired = data['hired']

ax[1][0].plot(xs, cs, label='cumulative quality')
ax[1][0].plot(xs, qs, 'b-.', label='quality')
ax[1][1].plot(xs, ws, label='number of workers')
ax[1][0].set_xlabel('tasks')
ax[1][0].set_ylabel('recall')
ax[1][1].set_xlabel('tasks')
ax[1][1].set_ylabel('workers')
ax[1][0].legend(bbox_to_anchor=(1, 0.5))
ax[1][1].legend(bbox_to_anchor=(1, 0.9))
ax[1][0].axis([0, 1000, 0.0, 1.0])
ax[1][0].set_autoscale_on(False)
ax[1][1].axis([0, 1000, 0.0, 5.0])
ax[1][1].set_autoscale_on(False)

#print cumulative
#print correct
#print hired

#dynamic hiring
with open('dh.json') as inputfile:
	data = json.load(inputfile)

cs = data['cs']
qs = data['qs']
ws = data['ws']
#cumulative = data['cumulative']
#correct = data['correct']
#hired = data['hired']

ax[2][0].plot(xs, cs, label='cumulative quality')
ax[2][0].plot(xs, qs, 'b-.', label='quality')
ax[2][1].plot(xs, ws, label='number of workers')
ax[2][0].set_xlabel('tasks')
ax[2][0].set_ylabel('recall')
ax[2][1].set_xlabel('tasks')
ax[2][1].set_ylabel('workers')
ax[2][0].legend(bbox_to_anchor=(1, 0.5))
ax[2][1].legend(bbox_to_anchor=(1, 0.9))
ax[2][0].axis([0, 1000, 0.0, 1.0])
ax[2][0].set_autoscale_on(False)
ax[2][1].axis([0, 1000, 0.0, 5.0])
ax[2][1].set_autoscale_on(False)

#print cumulative
#print correct
#print hired


plot.show()