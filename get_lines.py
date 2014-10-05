import sys

args = str(sys.argv)
input_file = sys.argv[1]
num_lines = sum(1 for line in open(input_file))
print num_lines
