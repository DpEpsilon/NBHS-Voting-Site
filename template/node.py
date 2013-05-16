import cgi

class Node(object):
	'''Base class for nodes'''
	def eval(self, context):
		raise NotImplemented('Base Node class does not implement eval')

class GroupNode(Node):
	'''Node for grouping a sequence of other nodes'''
	def __init__(self):
		self.children = []

	def add_child(self, child):
		self.children.append(child)

	def eval(self, context):
		evaluated_children = []
		for child in self.children:
			evaluated_children.append(child.eval(context))
		return ''.join(evaluated_children)

class TextNode(Node):
	'''Node for raw text'''
	def __init__(self, text):
		self.text = text

	def eval(self, context):
		return self.text

class EvalNode(Node):
	'''Node for a python expression which outputs an html-unsafe string'''
	def __init__(self, expression):
		self.expression = expression

	def eval(self, context):
		return cgi.escape(str(eval(self.expression, {}, context)))

class SafeEvalNode(Node):
	'''Node for a python expression which outputs an html string'''
	def __init__(self, expression):
		self.expression = expression

	def eval(self, context):
		return str(eval(self.expression, {}, context))

class IfNode(Node):
	'''Node for conditionally evaluating nodes'''
	def __init__(self, expression, true_node, false_node=None):
		self.expression = expression
		self.true_node = true_node
		self.false_node = false_node

	def eval(self, context):
		if eval(self.expression, {}, context):
			return self.true_node.eval(context)
		elif self.false_node:
			return self.false_node.eval(context)
		else:
			return ""

class ForNode(Node):
	'''Node that iterates over a context variable and
	repeatedly evaluates a node'''
	def __init__(self, var, iterable, repeated_node, empty_node=None):
		self.var = var
		self.iterable = iterable
		self.repeated_node = repeated_node
		self.empty_node = empty_node

	def eval(self, context):
		iterable = eval(self.iterable, {}, context)
		repeat_text = []
		current_context = context.copy()
		
		if len(iterable) == 0 and self.empty_node:
			return self.empty_node.eval(context)
		
		for i in iterable:
			current_context[self.var] = i
			repeat_text.append(self.repeated_node.eval(current_context))
		
		return ''.join(repeat_text)

