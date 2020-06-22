#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name:        logical_expression
# Purpose:     Contains logical_expression class, inference engine,
#              and assorted functions
#
# Created:     09/25/2011
# Last Edited: 07/22/2013  
# Notes:       *This contains code ported by Christopher Conly from C++ code
#               provided by Dr. Vassilis Athitsos
#              *Several integer and string variables are put into lists. This is
#               to make them mutable so each recursive call to a function can
#               alter the same variable instead of a copy. Python won't let us
#               pass the address of the variables, so put it in a list which is
#               passed by reference. We can also now pass just one variable in
#               the class and the function will modify the class instead of a
#               copy of that variable. So, be sure to pass the entire list to a
#               function (i.e. if we have an instance of logical_expression
#               called le, we'd call foo(le.symbol,...). If foo needs to modify
#               le.symbol, it will need to index it (i.e. le.symbol[0]) so that
#               the change will persist.
#              *Written to be Python 2.4 compliant for omega.uta.edu
#-------------------------------------------------------------------------------

import sys
import copy

#-------------------------------------------------------------------------------
# Begin code that is ported from code provided by Dr. Athitsos
class logical_expression:
	"""A logical statement/sentence/expression class"""
	# All types need to be mutable, so we don't have to pass in the whole class.
	# We can just pass, for example, the symbol variable to a function, and the
	# function's changes will actually alter the class variable. Thus, lists.
	def __init__(self):
		self.symbol = ['']
		self.connective = ['']
		self.subexpressions = []


def print_expression(expression, separator):
	"""Prints the given expression using the given separator"""
	if expression == 0 or expression == None or expression == '':
		print ('\nINVALID\n')

	elif expression.symbol[0]: # If it is a base case (symbol)
		sys.stdout.write('%s' % expression.symbol[0])

	else: # Otherwise it is a subexpression
		sys.stdout.write('(%s' % expression.connective[0])
		for subexpression in expression.subexpressions:
			sys.stdout.write(' ')
			print_expression(subexpression, '')
			sys.stdout.write('%s' % separator)
		sys.stdout.write(')')


def read_expression(input_string, counter=[0]):
	"""Reads the next logical expression in	 input_string"""
	# Note: counter is a list because it needs to be a mutable object so the
	# recursive calls can change it, since we can't pass the address in Python.
	result = logical_expression()
	length = len(input_string)
	while True:
		if counter[0] >= length:
			break

		if input_string[counter[0]] == ' ':    # Skip whitespace
			counter[0] += 1
			continue

		elif input_string[counter[0]] == '(':  # It's the beginning of a connective
			counter[0] += 1
			read_word(input_string, counter, result.connective)
			read_subexpressions(input_string, counter, result.subexpressions)
			break

		else:  # It is a word
			read_word(input_string, counter, result.symbol)
			break
	return result


def read_subexpressions(input_string, counter, subexpressions):
	"""Reads a subexpression from input_string"""
	length = len(input_string)
	while True:
		if counter[0] >= length:
			print ('\nUnexpected end of input.\n')
			return 0

		if input_string[counter[0]] == ' ':     # Skip whitespace
			counter[0] += 1
			continue

		if input_string[counter[0]] == ')':     # We are done
			counter[0] += 1
			return 1

		else:
			expression = read_expression(input_string, counter)
			subexpressions.append(expression)


def read_word(input_string, counter, target):
	"""Reads the next word of an input string and stores it in target"""
	word = ''
	while True:
		if counter[0] >= len(input_string):
			break

		if input_string[counter[0]].isalnum() or input_string[counter[0]] == '_':
			target[0] += input_string[counter[0]]
			counter[0] += 1

		elif input_string[counter[0]] == ')' or input_string[counter[0]] == ' ':
			break

		else:
			print('Unexpected character %s.' % input_string[counter[0]])
			sys.exit(1)


def valid_expression(expression):
	"""Determines if the given expression is valid according to our rules"""
	if expression.symbol[0]:
		return valid_symbol(expression.symbol[0])

	if expression.connective[0].lower() == 'if' or expression.connective[0].lower() == 'iff':
		if len(expression.subexpressions) != 2:
			print('Error: connective "%s" with %d arguments.' %
						(expression.connective[0], len(expression.subexpressions)))
			return 0

	elif expression.connective[0].lower() == 'not':
		if len(expression.subexpressions) != 1:
			print('Error: connective "%s" with %d arguments.' %
						(expression.connective[0], len(expression.subexpressions)))
			return 0

	elif expression.connective[0].lower() != 'and' and \
		 expression.connective[0].lower() != 'or' and \
		 expression.connective[0].lower() != 'xor':
		print('Error: unknown connective %s.' % expression.connective[0])
		return 0

	for subexpression in expression.subexpressions:
		if not valid_expression(subexpression):
			return 0
	return 1


def valid_symbol(symbol):
	"""Returns whether the given symbol is valid according to our rules."""
	if not symbol:
		return 0

	for s in symbol:
		if not s.isalnum() and s != '_':
			return 0
	return 1

# End of ported code
#-------------------------------------------------------------------------------

# Add all your functions here
model = {}
def check_true_false(knowledge_base, statement):  # 1 function
	#print_expression(knowledge_base,",")	
	cal(knowledge_base)
	#print("model",model)
	f = open("result.txt","w")
	a=TT_Entails(knowledge_base,statement)
	not_alpha = logical_expression()
	not_alpha.connective = ['not']
	not_alpha.subexpressions.append(statement)
	b = TT_Entails(knowledge_base,not_alpha)
	if(a==True and b != True):
		#print("\n"+"It is definitely true")
		f.write("It is definitely true")
	elif(a!= True and b==True):
		#print("\n"+"It is definitely false")
		f.write("It is definitely false")
	elif(a!=True and b!=True):
		#print("\n"+"It is possibly true,possibly false")
		f.write("It is possibly true,possibly false")
	elif(a==True and b==True):
		#print("\n"+"It is both true and false")
		f.write("It is both true and false"
)



def TT_Entails(KB,alpha): 	
	symbols1 = ExtractSymbols(KB)
	symbols2 = ExtractSymbols(alpha)
	symbols =  symbols1 + symbols2
	#print("symbols",len(symbols))
	return TT_Check_All(KB, alpha, symbols,model)





def TT_Check_All(KB,alpha,symbols,model):     
	if(len(symbols)==0):
		d = PL_True(KB,model)
		if(d):
			return PL_True(alpha, model)
		else: 
			return True
	else:
		p = symbols[0]
		rest = symbols[1:]  
		truea=TT_Check_All(KB, alpha, rest,extend(model,p,True))
		falsea=TT_Check_All(KB, alpha, rest,extend(model,p,False))
		return truea and falsea



def extend(model, symbol, value): 
	model_new = copy.deepcopy(model)        
	model_new[symbol] = value
	return model_new
	

def cal(statement): 	      
	for expression in statement.subexpressions:
		if expression.symbol[0]:
			model[expression.symbol[0]] = True
		elif expression.connective[0].lower() == 'not':
			if expression.subexpressions[0].symbol[0]:
				model[expression.subexpressions[0].symbol[0]] = False
		#print(model)
	return model
	



def ExtractSymbols(sentence):  
	result = [] 
	if(sentence.symbol[0] != ''):
		b = str(sentence.symbol[0])
		if(model.get(b)!=None):
			pass
		else:
			result.append(sentence.symbol[0])
	else:
		for child in sentence.subexpressions:
			result = result+ExtractSymbols(child) 
	result=list(set(result))
	return result


def PL_True(sentence,model):
	#global count
	#count+=1  
	if(sentence.symbol[0]!=''): 
		return model[sentence.symbol[0]]
	elif(sentence.connective[0].lower() == "and"): 
		for child in sentence.subexpressions:
			if(PL_True(child, model) == False):
				return False
		return True
	elif(sentence.connective[0].lower() == "or"):
		for child in sentence.subexpressions:
			if (PL_True(child, model) == True):
				return True
		return False
	elif(sentence.connective[0].lower() == "if"):
		left_child = sentence.subexpressions[0]
		right_child = sentence.subexpressions[1]
		if(PL_True(left_child, model) == True and PL_True(right_child,model) == False):
			return False
		return True

	elif(sentence.connective[0].lower() == "iff"):
		left_child = sentence.subexpressions[0]
		right_child = sentence.subexpressions[1]
		if(PL_True(left_child, model) == PL_True(right_child, model)):
			return True
		return False


	elif(sentence.connective[0].lower() == "not"):
		child = sentence.subexpressions[0]
		if(PL_True(child, model) == True):
			return False
		else:
			#result =  True
			return True 

	elif sentence.connective[0].lower() == "xor":
		number_of_symbols = 0
		for child in sentence.subexpressions:
			if(PL_True(child, model) == True):
				number_of_symbols = number_of_symbols + 1
		if(number_of_symbols == 1):
			return True
		else:
			return False









