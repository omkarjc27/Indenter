from datetime import date
import os
import argparse
import platform
import sys

def convert(input_file,output_file):

	'''
	
	Main Conversion file for converting indented  scopes to parenthesis scopes
	It cannot currently do multiline statements

	'''

	if(output_file == input_file):
		self_op = 1
		os.rename(input_file,'cache')
		input_file = 'cache'
	else:
		self_op = 0

	# Create the file to store output
	out_f = open(output_file, "w")
	out_f.close()
	# Open the output file for appending 
	out_f = open(output_file, "a")
	# Read the input file
	in_f = open(input_file)
	inl = in_f.readlines()
	# Initial values for looping variables
	prev_line = None
	prev_indention_value = 0
	extra_line = 0 	
	mul_comment = 0
	# Initiate Stack
	stack = Stack()
	stack.push(['',0])

	# Iterating over each line
	# Every iteration appends it's previous line to the file
	for line in inl:
		# Handling line starting with # eg #define ... etc
		if line.strip().startswith("#"):
			out_f.write(line)
		# Handling single line comments
		elif line.strip().startswith("//"):
			out_f.write(line)
		# Handling multiline comments
		elif line.strip().startswith("/*"):
			mul_comment = 1
			out_f.write(line)
		elif line.strip().endswith("*/"):
			mul_comment = 0 
			out_f.write(line)	
		elif mul_comment == 1 :
			out_f.write(line)
		# Check if line is not blank
		elif len(line.strip()) > 0:
			indention_value = 0
			# Count indention
			while line[indention_value].isspace() or line[indention_value] == '\t':
				indention_value += 1
				if indention_value >= len(line):
					break
			# When going in inner scope
			if(indention_value > prev_indention_value):
				if(prev_line != None):
					out_f.write(prev_line)
				item = stack.view_top()
				out_f.write(item[0]+'{\n')
				val = [line[slice(indention_value)],indention_value] 
				stack.push(val)
			# When coming to outer scope	
			elif(indention_value < prev_indention_value):
				if(prev_line != None):
					out_f.write(prev_line.replace('\n',';\n'))
				while True:
					item = stack.view_top()
					if indention_value < item[1]:
						stack.pop()
						item = stack.view_top()
						out_f.write(item[0]+'}\n')
					else:
						break
			# Normal Line
			else:
				if(prev_line != None):
					out_f.write(prev_line.replace('\n',';\n'))

			prev_indention_value = indention_value
			prev_line = line
			if(extra_line == 1):
				out_f.write('\n')
				extra_line = 0

		# When line is blank
		else:
			extra_line = 1
	
	# For Last line which is not added in the for loop 
	if(len(prev_line.strip())>0):
		# To add a buffer so that closing bracket is not immediately after the last statement
		if(extra_line == 0):
			prev_line += '\n'
		prev_line = prev_line.replace('\n',';\n')
		out_f.write(prev_line)
	
	# Pop stack untill empty so that all scopes that are not closed get closed 
	stack.pop()
	while stack.length() > 0:
		item = stack.pop()
		out_f.write(item[0]+'}\n')
	
	# Close all opened files
	out_f.close()
	in_f.close()
	if(self_op == 1):
		os.remove('cache')


class Stack:
	'''

	Class For Storing scopes and indention records

	'''
	def __init__(self):
		self.__storage = []

	def isEmpty(self):
		return len(self.__storage) == 0

	def push(self,element):
		self.__storage.append(element)

	def pop(self):
		return self.__storage.pop()

	def view_top(self):
		l = len(self.__storage)
		return self.__storage[l-1]

	def length(self):
		return len(self.__storage)

if __name__ == '__main__':

	if len(sys.argv) > 1 :

		args = sys.argv
		del args[0]

		input_file = None
		output_file = None
		if args[0] == "--output2file":
			output_file = args[1]
			del args[0]
			del args[0]
			run = 0
		else:
			run = 1

		for arg in args:
			if os.path.isfile(arg):
				input_file = arg
				break

		if input_file == None:
			print('No File Found')
		else:
			if output_file == None:
				output_file = input_file
		
			convert(input_file,output_file)
		
			if run == 1:
				os.system(' '.join(args))
			else:	
				print("\nDone.")

	else :
		print("Help Screen")