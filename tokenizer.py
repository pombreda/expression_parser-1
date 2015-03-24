# string tokenizer
import re

# defines pattern for identifying tokens
class TokenPattern:
	def __init__(self, regex, symbol):
		self.regex = regex
		self.token_id = symbol

# includes the matched string and a token identifier which is
# used for parsing
class Token:
	def __init__(self, tokString, symbol):
		self.tokenString = tokString
		self.token_id = symbol

# tokenizes an input string
class Tokenizer:
	def __init__(self):
		self.tokenPatterns = []
		self.tokens = []

	# add token pattern
	def add(self, regex, symbol):
		self.tokenPatterns.append(TokenPattern(re.compile(r"^(" + regex + ")"), symbol))

	# tokenize string or line, pushing new tokens to the token stack
	def tokenize(self, s):
		s = s.strip()
		while len(s):
			matched = False
			for pattern in self.tokenPatterns:
				tok = pattern.regex.match(s)
				if tok:
					matched = True
					self.tokens.append(Token(tok.group(), pattern.token_id))
					s = s[tok.end():].strip()
					break
			if not matched:
				print("error: syntax error at \n-->\"" + s + "\"")
				break