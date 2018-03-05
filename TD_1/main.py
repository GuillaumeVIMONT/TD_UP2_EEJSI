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

sample = []

def reservoir_sampling(edge, k):
    N = len(edge)
    for (u,v) in enumerate([edge]):
        if len(sample) < k:
            sample.append(edge)
        else:
            j = random.randint(0, k)
            if j < k:
                sample[j] = edge
    return sample

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

for i in edge_list:
	reservoir = reservoir_sampling(i, k)

write_edge_reservoir(reservoir)
