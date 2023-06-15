# def average(*args):
# 	print(type(args))
# 	print("args is {}".format(args))
# 	print("*args is : ", *args)
# 	mean=0
# 	for arg in args:
# 		mean += arg
# 	return mean/len(args)

# print(average(1,2,3))

# def print_backwards(*args, file=None):
# 	for word in args[::-1]:
# 		print(word[::-1], end=' ', file=file)

# with open("backwards.txt","w") as backwards :
# 	print_backwards("hello", "planet", file=backwards)

# def print_backwards(*args, end=' ', **kwargs):
# 	print(kwargs)
# 	kwargs.pop('end',None)
# 	for word in args[::-1]:
# 		print(word[::-1], end=' ', **kwargs)

def print_backwards(*args, **kwargs):
	end_character=kwargs.pop('end','\n')
	sep_character=kwargs.pop('sep',' ')
	for word in args[::-1]:
		print(word[::-1],end=sep_character,**kwargs)
	print(end=end_character)

with open("backwards.txt","w") as backwards:
	print_backwards("hello","planet","earth","take","me","to","your","leader",end='\n')
	print("Another string")

print()
print("hello","planet","earth","take","me","to","your","leader",end='\n',sep='|')
print_backwards("hello","planet","earth","take","me","to","your","leader",end='\n',sep='|')