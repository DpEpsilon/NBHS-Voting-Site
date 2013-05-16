import parser

TEMPLATES_DIR = './templates'

def render(filename, context):
	"""
	template.render(filename, context) -> rendered html
	
	filename is location of the template relative to template.TEMPLATES_DIR
	context is a dictionary of values to give to the template
	
	Raises an error if template is invalid
	"""
	template = parser.Template(open(TEMPLATES_DIR + '/' + filename).read())
	return template.eval(context)
