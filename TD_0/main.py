import random
import csv


file_input = input("Please enter input filename (e.g data.csv ) : ")

k = input("Please enter reservoir size : ")
k = int(k)

file_output = input("Please enter output filename (e.g reservoir_output.csv ) : ")


def read_edge_from_file(file_input):
	with open(file_input) as csvfile:
		edge_list = []
		reader = csv.DictReader(csvfile)
		for row in reader:
			edge = (row['Source'], row['Target'])
			edge_list.append(edge)
	return edge_list

def write_edge_reservoir(edge_reservoir):
	f = open(file_output, "w")
	header_csv = "Source, Target"
	f.write(header_csv +"\n")
	for i in edge_reservoir:
		a = str(i[0])
		b = str(i[1])
		e = a + ',' + b
		f.write(e +"\n")
	f.close()

edge_list = read_edge_from_file(file_input)
sample = []
for index, edge in enumerate(edge_list):
    if index < k:
        sample.append(edge)
    else:
        j = random.randint(0, index)
        if j < k:
           sample[j] = edge

write_edge_reservoir(sample)
