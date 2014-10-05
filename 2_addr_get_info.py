import sys

total = len(sys.argv)
args = str(sys.argv)

if total != 3:
        print "Usage: python 2_get_addr_info.py  <input_file> <output_file>"

filename = sys.argv[1]
output_file = sys.argv[2]

read_file = open(filename, 'r')
op_filename = open(output_file, 'a')

#entire_text = read_file.read()
#tuples = entire_text.split('\n')
#cols = tuples.split(',')
cols = []
items = []

#for record in tuples:
 #       item = record.split(',')
 #       cols.append(item)

wid_dict = {}
sid_dict = {}
rd_dict = {}
ctr_dict = {}
idx_dict = {}
ldst_dict = {}
hitmiss_dict = {}
ts_dict = {}
ovr_idx = 0

#for data in cols:
for line in read_file:
		
	cols = line.split(',')
	for value in cols:	
        	val = value.split(': ')
       		if val[0] == 'Accessed addr':
        		addr = int(val[1])
                #       libor_rec.addr_append(int(val[1]))
       		elif val[0] == ' Load/Store':
        	        ldst = val[1]
              		if ldst_dict.has_key(addr) == False:
				ldst_dict.update({addr : ldst})

	        elif val[0] == ' Warp ID':
        	        wid = int(val[1])
			if wid_dict.has_key(addr) == False:
				wid_dict.update({addr : wid})
                
         	elif val[0] == ' Shader ID':
                	sid = int(val[1])
 			if sid_dict.has_key(addr) == False:
				sid_dict.update({addr : sid})

		elif val[0] == ' timestamp':
			ts = int(val[1])
			if ts_dict.has_key(addr) == False:
				ts_dict.update({addr : ts})

		elif val[0] == ' status':
			hm = int(val[1])
			if hitmiss_dict.has_key(addr) == False:
				hitmiss_dict.update({addr : hm})

			if ctr_dict.has_key(addr) == False:
				ctr_dict.update({addr : 1})
				ovr_idx = ovr_idx + 1
				idx_dict.update({addr : ovr_idx})
				rd_dict.update({addr : 0})
				ts_dict.update({addr : ts})
		
			elif ctr_dict.has_key(addr) == True  and wid_dict.get(addr) != wid and sid_dict.get(addr) != sid and ldst_dict.get(addr) != ldst:
				ctr_dict[addr] = ctr_dict[addr] + 1
				ovr_idx = ovr_idx + 1
				if rd_dict.has_key(addr) == True:	
					rd_dict[addr] = rd_dict[addr] + (ovr_idx - idx_dict[addr])
					idx_dict[addr] = ovr_idx
				ts_dict[addr] = ts				
			
			elif ctr_dict.has_key(addr) == True and wid_dict[addr] == wid and sid_dict[addr] == sid and (ldst_dict[addr] != ldst or (ts - ts_dict[addr] > 25)):
				ctr_dict[addr] = ctr_dict[addr] + 1
                        	ovr_idx = ovr_idx + 1
                      		if rd_dict.has_key(addr) == True:
        	                	rd_dict[addr] = rd_dict[addr] + (ovr_idx - idx_dict[addr])
	                                idx_dict[addr] = ovr_idx
				ts_dict[addr] = ts

for address in ctr_dict.keys():
	op_filename.write(str(address))
	op_filename.write('; ')
	op_filename.write(str(wid_dict[address]))
	op_filename.write('; ')
	op_filename.write(str(sid_dict[address]))
	op_filename.write('; ')
	op_filename.write(str(ctr_dict[address]))
	op_filename.write('; ')
	op_filename.write(str(idx_dict[address]))
	op_filename.write('; ')
	op_filename.write(str(rd_dict[address]/ctr_dict[address]))
	op_filename.write('; ')
	op_filename.write(str(hitmiss_dict[address]))
	op_filename.write('\n')

print 'done\n'	


read_file.close()
op_filename.close()
