import node

structure_types = ['%', '!', '*']

TEMPLATES_DIR = './templates'

def tokenize(text):
	tokens = []
	start = 0
	end = 0
	structure = None
	
	while end < len(text):
		if structure:
			if text[end] != structure:
				end += 1
			elif end + 1 < len(text) and \
					text[end+1] == '}':
				structure = None
				end += 2
				tokens.append((True, text[start:end]))
				start = end
			else:
				end += 1
		else:
			if text[end] != '{':
				end += 1
			elif end + 1 < len(text) and \
					text[end+1] in structure_types:
				structure = text[end+1]
				tokens.append((False, text[start:end]))
				start = end
				end += 2
			else:
				end += 1
	if structure:
		tokens.append((True, text[start:]))
	else:
		tokens.append((False, text[start:]))
	return tokens
	
class Template(node.Node):
	def __init__(self, template_text):
		self.tokens = tokenize(template_text)
		self.upto = 0
		self.tree = self._base()
		if not self.end():
			raise Exception("Template appears to be invalid.")

	def eval(self, context):
		return self.tree.eval(context)
		
	def end(self):
		return self.upto == len(self.tokens)
		
	def next(self):
		if not self.end():
			self.upto += 1

	def peek(self):
		return self.tokens[self.upto] if not self.end() \
			else None

	def _base(self):
		cur_node = node.GroupNode()

		while self.peek() is not None:
			if self.peek()[0]: # inside a structure
				control_node = self._control()
				if control_node:
					cur_node.add_child(control_node)
				else:
					break
			else:
				text_node = self._text()
				if text_node:
					cur_node.add_child(text_node)
				else:
					break

		return cur_node if len(cur_node.children) > 0 else None
			
	def _control(self):
		if not self.peek()[0]:
			return None
		
		token = self.peek()[1]
		
		if token[:2] == '{%':
			instruction = token.split()[1]
			if instruction == 'if':
				return self._if()
			elif instruction == 'for':
				return self._for()
			elif instruction == 'include':
				self.next()
				return Template(open(TEMPLATES_DIR + '/' +
									 token.split()[2]).read())
			elif instruction == 'safe':
				self.next()
				return node.SafeEvalNode(''.join(token.split()[2:-1]))
			else:
				return None
		elif token[:2] == '{!':
			cur_node = node.EvalNode(token[2:-2].strip())
			self.next()
			return cur_node
		elif token[:2] == '{*':
			self.next()
			return node.TextNode('')
		else:
			return None

	def _if(self):
		if self.peek()[1].split()[1] != 'if':
			return None
		
		expression = ' '.join(self.peek()[1].split()[2:-1])
		self.next()
		true_node = self._base()
		false_node = None
		if self.peek()[1].split()[1] == 'else':
			self.next()
			false_node = self._base()
		if self.peek()[1].split()[1] == 'end' and \
				self.peek()[1].split()[2] == 'if':
			self.next()
		else:
			return None

		return node.IfNode(expression, true_node, false_node)

	def _for(self):
		head = self.peek()[1].split()
		if head[1] != 'for' or head[3] != 'in':
			return None
		
		var = head[2]
		iterable = ''.join(head[4:-1])
		self.next()
		
		repeated_node = self._base()
		empty_node = None
		
		if self.peek()[1].split()[1] == 'empty':
			self.next()
			empty_node = self._base()
		if self.peek()[1].split()[1] == 'end' and \
				self.peek()[1].split()[2] == 'for':
			self.next()
		else:
			return None

		return node.ForNode(var, iterable, repeated_node, empty_node)

	def _text(self):
		if not self.peek()[0]: # If the node is text
			cur_node = node.TextNode(self.peek()[1])
			self.next()
			return cur_node
		else:
			return None
