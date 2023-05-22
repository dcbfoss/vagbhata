import os

filenames = sorted([ i for i in os.listdir()if i.endswith('csv')])

data = []

for index, filename in enumerate(filenames):
    data.append([])
    with open(filename,'r') as inp_file:
        for line in inp_file:
            data[-1].append(line.rstrip()+','+str(index)+'\n')

counts = [len(i) for i in data]
minval = min(counts)
ind = counts.index(minval)

rate = [int(round(i/minval)) for i in counts]
maxval = max(rate)

mix = []

for i in data[ind]:
    mix.append([i])

if ind==0:ind=1
else:ind=0

mix_ind = 0
h_counter = 0
for i in data[ind]:
    mix[mix_ind].append(i)
    h_counter+=1
    if h_counter >= maxval-1:
        h_counter = 0
        mix_ind += 1
    if mix_ind>=minval-1:
        mix_ind=0

with open('combined.csv', 'w') as outfile:
    for m in mix:
        for n in m:
            outfile.write(n)
