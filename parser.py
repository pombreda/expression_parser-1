# parser.py
from tokenizer import Tokenizer
from tokenizer import Token
from enum import Enum

# symbols
class Symbol(Enum):
# terminals
	FUNCTION 		= 0
	OPEN_PAREN 		= 1
	CLOSE_PAREN	 	= 2
	PLUSMINUS 		= 3
	MULTDIV 		= 4
	RAISED 			= 5
	NUMBER 			= 6
# nonterminals
	ROOT            = 100
	EPSILON		  	= 101
	EXPRESSION 		= 102
	SUM_OP			= 103
	SIGNED_TERM 	= 104
	TERM        	= 105
	TERM_OP    		= 106
	SIGNED_FACTOR 	= 107
	FACTOR      	= 108
	FACTOR_OP   	= 109
	ARGUMENT    	= 110
	VALUE           = 111

# define terminals
tokenizer = Tokenizer()
tokenizer.add(r"sin|cos|tan|exp|sqrt", Symbol.FUNCTION)
tokenizer.add(r"\(", Symbol.OPEN_PAREN)
tokenizer.add(r"\)", Symbol.CLOSE_PAREN)
tokenizer.add(r"[+-]", Symbol.PLUSMINUS)
tokenizer.add(r"[*/]", Symbol.MULTDIV)
tokenizer.add(r"[\^]", Symbol.RAISED)
tokenizer.add(r"[0-9]+", Symbol.NUMBER)

class AST_node:
	def __init__(self, symbol, token=None):
		self.token = token
		self.symbol = symbol
		self.children = []

	def add(self, node):
		if node != None: 
			self.children.append(node)

	def printRPN(self):
		# print post-order traversal to get the RPN expression
		for child in self.children:
			child.printRPN()
		if self.token:
			if self.token.token_id != Symbol.OPEN_PAREN and self.token.token_id != Symbol.CLOSE_PAREN:
				print(self.token.tokenString, '')

	def eval(self):
		# multiple expressions, i.e. "(e1)(e2)..(eN) multiply
		result = 0
		for node in self.children():
			if result:
				result = result * node.eval()
			else:
				result = node.eval()
		return result


class AST_expression(AST_node):
	def eval(self):



class Parser:
	def __init__(self, tokens, debug=0):
		self.tokens = list(tokens)
		self.debug = debug

	# parse the tokens
	def parse(self):
		if not self.tokens:
			return
		self.lookahead = self.tokens[0]
		ast = self.root()

		return ast

	# get another token
	def nextToken(self, node):
		node.token = self.tokens.pop(0)
		if self.tokens:
			self.lookahead = self.tokens[0]
		else:
			self.lookahead = Token('', Symbol.EPSILON)

# modified expression grammar from http://cogitolearning.co.uk/
#
#	root 			-> expression root
#        			 | epsilon
#
#	expression 		-> signed_term sum_op
#
#	sum_op 			-> PLUSMINUS term sum_op
#					 | epsilonepsilon
#
#	signed_term 	-> PLUSMINUS term
#					 | term
#
#	term 			-> factor term_op
#
#	term_op     	-> MULTDIV signed_factor term_op
#					 | epsilon
#	
#	signed_factor	-> PLUSMINUS factor
#					 | factor
#
#	factor			-> argument factor_op
#
#	factor_op		-> RAISED expression
#					 | epsilon
#
# 	argument		-> FUNCTION argument
#					 | OPEN_PAREN expression CLOSE_PAREN
#					 | value
#
#	value			-> NUMBER
#

	def root(self):
		# root -> expression
		rootNode = AST_node(Symbol.ROOT)
		while (self.lookahead.token_id != Symbol.EPSILON):
			rootNode.add(self.expression())
		return rootNode

	def expression(self):
		# expression -> signed_term sum_op
		node = AST_node(Symbol.EXPRESSION)
		if self.debug: print ("expression -> signed_term sum_op")
		node.add(self.signedTerm())
		node.add(self.sumOp())
		return node

	def sumOp(self):
		node = AST_node(Symbol.SUM_OP)
		if self.lookahead.token_id == Symbol.PLUSMINUS:
			# sum_op -> PLUSMINUS term sum_op
			if self.debug: print("sum_op -> PLUSMINUS term sum_op")
			self.nextToken(node)
			node.add(self.term())
			node.add(self.sumOp())
			return node
		# else sum_op -> EPSILON
		return None

	def signedTerm(self):
		node = AST_node(Symbol.SIGNED_TERM)
		if self.lookahead.token_id == Symbol.PLUSMINUS:
			# signed_term -> PLUSMINUS term
			if self.debug: print("signed_term -> PLUSMINUS term")
			self.nextToken(node)
			node.add(self.term())
		else:
			# signed_term -> term
			node.add(self.term())
		return node

	def term(self):
		# term -> factor term_op
		if self.debug: print("term -> factor term_op")
		node = AST_node(Symbol.TERM)
		node.add(self.factor())
		node.add(self.termOp())
		return node

	def termOp(self):
		node = AST_node(Symbol.TERM_OP)
		if self.lookahead.token_id == Symbol.MULTDIV:
			# term_op -> MULTDIV signed_factor term_op
			if self.debug: print("term_op -> MULTDIV factor term_op")
			self.nextToken(node)
			node.add(self.signedFactor())
			node.add(self.termOp())
			return node
		# else termOp -> EPSILON
		return None

	def signedFactor(self):
		node = AST_node(Symbol.SIGNED_FACTOR)
		if self.lookahead.token_id == Symbol.PLUSMINUS:
			# signed_factor -> PLUSMINUS factor
			if self.debug: print("signed_factor -> PLUSMINUS factor")
			self.nextToken(node)
			node.add(self.factor())
		else:
			# signed_factor -> factor
			if self.debug: print("signed_factor -> factor")
			node.add(self.factor())
		return node

	def factor(self):
		# factor -> argument factor_op
		if self.debug: print("factor -> argument factor_op")
		node = AST_node(Symbol.FACTOR)
		node.add(self.argument())
		node.add(self.factorOp())
		return node

	def factorOp(self):
		node = AST_node(Symbol.FACTOR_OP)
		if self.lookahead.token_id == Symbol.RAISED:
			# factor_op -> RAISED expression
			if self.debug: print("factor_op -> RAISED expression")
			self.nextToken(node)
			node.add(self.signedFactor())
			return node
		# else factorOp -> eplison
		return None

	def argument(self):
		node = AST_node(Symbol.ARGUMENT)
		if self.lookahead.token_id == Symbol.FUNCTION:
			# argument -> FUNCTION argument
			if self.debug: print("argument -> FUNCTION argument")
			self.nextToken(node)
			node.add(self.argument())
		elif self.lookahead.token_id == Symbol.OPEN_PAREN:
			# argument -> OPEN_PAREN expression CLOSE_PAREN
			if self.debug: print("argument -> OPEN_BRACKET sum CLOSE_BRACKET")
			self.nextToken(node)
			node.add(self.expression())
			if self.lookahead.token_id != Symbol.CLOSE_PAREN:
				print("error: expected closing parenthesis: \"" + self.lookahead.tokenString + "\" + found instead.")
				exit()
			self.nextToken(node)
		else:
			# argument -> value
			if self.debug: print("argument -> value")
			node.add(self.value())
		return node

	def value(self):
		node = AST_node(Symbol.VALUE)
		if self.lookahead.token_id == Symbol.NUMBER:
			# value -> NUMBER
			if self.debug: print ("value -> NUMBER")
			self.nextToken(node)
		else:
			print("error: unexpected symbol: " + str(self.lookahead.token_id) + " \"" + self.lookahead.tokenString + "\"")
			exit()
		return node

tokenizer.tokenize("(5*5)(-5 + 100 * (2))")
parser = Parser(tokenizer.tokens)
parser.parse().printRPN()