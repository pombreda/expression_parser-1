# expression_parser

reddit daily programming challenge 205
http://www.reddit.com/r/dailyprogrammer/comments/2yquvm/20150311_challenge_205_intermediate_rpn/

Python tokenizer and parser.

Parses an input expression and creates an abstract syntax tree (AST).  A post order walk of the tree produces the reverse polish notation for the expression.

This is bit of an over the top solution.  It would have been much easier to use the shunting-yard algorithm.  However, I wanted to revisit lexers and parsers. It has been a while since I took compiler design so it was worth it!
