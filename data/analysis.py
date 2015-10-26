import csv


truth = []
alex = []
jeff = []
sarah = []
will = []

#doing all the reading

with open('expert.csv') as csvExpert:
	reader = csv.DictReader(csvExpert)
	for row in reader:
		#print row['start'], row['end']
		pair = (row['start'], row['end'])
		truth.append(pair)

with open('alex.csv') as csvAlex:
	reader = csv.DictReader(csvAlex)
	for row in reader:
		pair = (row['start'], row['end'])
		alex.append(pair)

with open('jeff.csv') as csvJeff:
	reader = csv.DictReader(csvJeff)
	for row in reader:
		pair = (row['start'], row['end'])
		jeff.append(pair)

with open('sarah.csv') as csvSarah:
	reader = csv.DictReader(csvSarah)
	for row in reader:
		pair = (row['start'], row['end'])
		sarah.append(pair)

with open('will.csv') as csvWill:
	reader = csv.DictReader(csvWill)
	for row in reader:
		pair = (row['start'], row['end'])
		will.append(pair)

