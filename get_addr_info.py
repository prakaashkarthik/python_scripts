import sys

total = len(sys.argv)
args = str(sys.argv)

if total != 4:	
	print "Usage: python get_addr_info.py <all/store/load/repeat/cycles> <input_file> <output_file>"

filename = sys.argv[2]
filetype = sys.argv[1]
output_file = sys.argv[3]

read_file = open(filename, 'r')
op_filename = open(output_file, 'a')

entire_text = read_file.read()
tuples = entire_text.split('\n')
#cols = tuples.split(',')
cols = []
items = []

class addr_tuple:
	
	def __init__ (self, idx, addr, ld_st, wid, sid, ts, tid, v, ctr):	
		self.index = idx 
		self.addr_acc = addr
		self.ldst_type = ld_st
		self.warp_id = wid
		self.shader_id = sid
		self.timestamp = ts
		self.thread_id = tid
		self.visited = v
		self.ctr = ctr
		self.ld_cyc_rpt = []
		self.st_cyc_rpt = []

	def idx_append(self, value):
		self.index = value	

	def visited(self, value):
		self.visited= value
	
	def addr_append(self, value):
		self.addr_acc= value
	
	def ldst_append(self, value):
		self.ldst_type= value

	def wid_append(self, value):
		self.warp_id= value
	
	def sid_append(self, value):
		self.shader_id= value

	def tid_append(self, value):
		self.thread_id= value

	def time_append(self, value):
		self.timestamp= value

	def ld_rpt_append(self, value):
		self.ld_cyc_rpt.append(value)

	def st_rpt_append(self, value):
		self.st_cyc_rpt.append(value)


		
addr_db = []
rec_temp = addr_tuple(0, 0, 'none', 0, 0,  0, 0, 0, 0)


total_num_accesses = sum(1 for line in open(filename))
op_filename.write('Total number of accesses: ')
op_filename.write(str(total_num_accesses))
op_filename.write('\n----------------------------------\n')

for record in tuples:
	item = record.split(',')
	cols.append(item)
#	#print cols
	

#print cols[1]

ovr_idx = 0

for data in cols:
	for value in data:
		val = value.split(':')
		if val[0] == 'Accessed addr':
			addr = int(val[1])
		#	libor_rec.addr_append(int(val[1]))
		
		#	libor_rec.idx_append(ovr_idx)
		elif val[0] == ' Load/Store':
			ldst = val[1]
		#	libor_rec.ldst_append(val[1])
		elif val[0] == ' Warp ID':
			wid = int(val[1])
		#	libor_rec.wid_append(int(val[1]))
		elif val[0] == ' Shader ID':
			sid = int(val[1])
		#	libor_rec.sid_append(int(val[1]))
		elif val[0] == ' timestamp':
			ts =  int(val[1])
		#	libor_rec.time_append(int(val[1]))
	addr_db.append(addr_tuple(ovr_idx, addr, ldst, wid, sid, ts, 0, 0, 0))
	ovr_idx = ovr_idx + 1

store_ctr = 0
load_ctr = 0

if filetype == 'store' or filetype == 'all':
	for rec in addr_db:
		if rec.ldst_type == ' store':
			op_filename.write(str(rec.index))
			op_filename.write('; ')			
			op_filename.write(str(rec.addr_acc))
			op_filename.write('; ')
			op_filename.write(str(rec.ldst_type))
			op_filename.write('; ')
			op_filename.write(str(rec.warp_id))
			op_filename.write('; ')
			op_filename.write(str(rec.shader_id))
			op_filename.write('; ')
			op_filename.write(str(rec.timestamp))
			op_filename.write('\n')
		

	op_filename.write('-------------------------------------------\n')	
			

if filetype == 'load' or filetype == 'all':
	for rec in addr_db:
		if rec.ldst_type == ' load':
			op_filename.write(str(rec.index))
			op_filename.write('; ')			
			op_filename.write(str(rec.addr_acc))
			op_filename.write('; ')
			op_filename.write(str(rec.ldst_type))
			op_filename.write('; ')
			op_filename.write(str(rec.warp_id))
			op_filename.write('; ')
			op_filename.write(str(rec.shader_id))
			op_filename.write('; ')
			op_filename.write(str(rec.timestamp))
			op_filename.write('\n')
		

	op_filename.write('-------------------------------------------\n')	

if filetype == 'repeat' or filetype == 'all':
	addr_db[0].visited = 1
	rec_ctr = 0
	op_filename.write('Idx ; Addr ; LD/ST; Warp ; Shader ; Cycle ; Count ; Cycles Rptd\n')
	for i in addr_db:
		for rec in addr_db:
			if rec.visited == 0 and (i.timestamp < rec.timestamp):	
				if (i.addr_acc == rec.addr_acc) and (i.index != rec.index):
					addr_db[rec.index].visited = 1
					addr_db[i.index].ctr = addr_db[i.index].ctr + 1	
					if rec.ldst_type == ' load':
						addr_db[i.index].ld_rpt_append(rec.timestamp)
					else:
						addr_db[i.index].st_rpt_append(rec.timestamp)
	
		rec_temp = addr_db[i.index]
		if (rec_temp.ctr != 0):		
			op_filename.write(str(rec_temp.index))
			op_filename.write('; ')			
			op_filename.write(str(rec_temp.addr_acc))
			op_filename.write('; ')
			op_filename.write(str(rec_temp.ldst_type))
			op_filename.write('; ')
			op_filename.write(str(rec_temp.warp_id))
			op_filename.write('; ')
			op_filename.write(str(rec_temp.shader_id))
			op_filename.write('; ')
			op_filename.write(str(rec_temp.timestamp))
			op_filename.write('; ')
			op_filename.write(str(rec_temp.ctr))
			op_filename.write('; ')
			op_filename.write(str(rec_temp.ld_cyc_rpt))
			op_filename.write('; ')
			op_filename.write(str(rec_temp.st_cyc_rpt))
			op_filename.write('\n')
#		rec_ctr = rec_ctr + 1
#		if rec_ctr % 10000 == 0:
#			print rec_ctr, 'records done'
					
#if filetype == 'store' or filetype == 'all':
#	idx = 0
#	for acc_type in ldst_type:
#		if ldst_type[idx] == ' store':
#			store_ctr = store_ctr + 1
#			op_filename.write(str(store_ctr))
#			op_filename.write('; ')			
#			op_filename.write(addr_acc[store_ctr - 1])
#			op_filename.write('; ')
#			op_filename.write(ldst_type[store_ctr - 1])
#			op_filename.write('; ')
#			op_filename.write(warp_id[store_ctr - 1])
#			op_filename.write('; ')
#			op_filename.write(shader_id[store_ctr -1])
#			op_filename.write('; ')
#			op_filename.write(timestamp[store_ctr - 1])
#			op_filename.write('\n')
#			idx = idx + 1

#	op_filename.write('---------------------------------------\n')

#idx = 0
	
#if filetype == 'load' or filetype == 'all':
#	load_file = open(output_file, 'a')
#	for type_acc in ldst_type:
#		if ldst_type[idx] == ' load':
#			load_ctr = load_ctr + 1
#			op_filename.write(str(load_ctr))
#			op_filename.write('; ')			
#			op_filename.write(addr_acc[idx])
#			op_filename.write('; ')
#			op_filename.write(ldst_type[idx])
#			op_filename.write('; ')
#			op_filename.write(warp_id[idx])
#			op_filename.write('; ')
#			op_filename.write(shader_id[idx])
#			op_filename.write('; ')
#			op_filename.write(timestamp[idx])
#			op_filename.write('\n')
#		idx = idx + 1
#	op_filename.write('---------------------------------------\n')
	
if filetype == 'repeat' or filetype == 'all':
	addr_rpt_file = open(output_file, 'a')
		


elif filetype == 'cycles' or filetype == 'all':
	cyc_rpt_file = open(output_file, 'a')


