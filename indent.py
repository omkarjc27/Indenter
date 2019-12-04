#!/usr/bin/env python
from datetime import date
import os
import argparse
import platform

def convert(input_file,output_file,credits):

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
	out_f.write(credits+'\n') # We can add our own credits here as a comment i.e. "Created by using IndenPro"
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
	# Initiate Stack
	stack = Stack()
	stack.push(['',0])

	# Iterating over each line
	# Every iteration appends it's previous line to the file
	for line in inl:
		# Check if line is not blank
		if len(line.strip()) > 0:
			indention_value = 0
			# Count indention
			while line[indention_value].isspace() or line[indention_value] == '\t':
				indention_value += 1
				if indention_value >= len(line):
					break
			# When going in inner
			if(indention_value > prev_indention_value):
				if(prev_line != None):
					out_f.write(prev_line)
				val = [line[slice(indention_value-1)],indention_value] 
				stack.push(val)
				item = stack.view_top()
				out_f.write(item[0]+'{\n')
			# When coming to outer scope	
			elif(indention_value < prev_indention_value):
				if(prev_line != None):
					out_f.write(prev_line.replace('\n',';\n'))
				while True:
					item = stack.view_top()
					if indention_value < item[1]:
						out_f.write(item[0]+'}\n')
						stack.pop()
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
		out_f.write(prev_line.replace('\n',';\n'))
	
	# Pop stack untill empty so that all scopes that are not closed get closed 
	while stack.length() > 1:
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

	parser = argparse.ArgumentParser()
	parser.add_argument("InputFile",help="Source Code File to Indent")
	parser.add_argument('-v', '--version', action='version', version='IndenPro version:0.0.1')
	parser.add_argument("--clang", help="Convert to JAVA code",action="store_true")
	parser.add_argument("--java", help="Convert to JAVA code",action="store_true")
	parser.add_argument("--js", help="Convert to Java-Script code",action="store_true")
	parser.add_argument("--php", help="Convert to PHP code",action="store_true")
	parser.add_argument("-o","--output_file", help="Output File To Store Processed Code \n(If Not Specified Code is stored in the InputFile)")
	args = parser.parse_args()

	print("Indenting Code...")

	input_file = args.InputFile 
	if args.output_file:
		output_file = args.output_file
	else:
		output_file = input_file

	credits = "/*\nIndented Using Indenter\n\
Write code in major languages like C,C++,C#,Go,JAVA,Java-Script,PHP etc. Without parenthesis -> {} and semi-colan -> using Indenter\n\
GoTo https://www.github.com/omkarjc27/Indenter\n*/"
	
	convert(input_file,output_file,credits)

	print("Done.")
