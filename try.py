x = {1 : 2, 2 : 3}
y = x.has_key(1)
z = x.has_key(2)

x[1] = x[1] + 1
print y, ' ', z, ' ', x
