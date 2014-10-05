import sys

total = len(sys.argv)
args = str(sys.argv)

if total != 4:
        print "Usage: python 2_get_addr_info.py <address>  <input_file> <output_file>"

addr_mine = sys.argv[1]
filename = sys.argv[2]
output_file = sys.argv[3]

read_file = open(filename, 'r')
op_filename = open(output_file, 'a')

#entire_text = read_file.read()
#tuples = entire_text.split('\n')
#cols = tuples.split(',')
cols = []
items = []
ctr = 0

for line in read_file:
	cols = line.split(',')
	addr = cols[0].split(': ')
	if addr[1] == addr_mine:
		op_filename.write(line)
		ctr = ctr + 1

op_filename.write('-----------------------------')
op_filename.write('Total number of occurrences: ')
op_filename.write(str(ctr))
op_filename.write('\n')		
		

read_file.close()
print 'done'
