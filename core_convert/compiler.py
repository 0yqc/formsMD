import re
import uuid
import markdown


# GENERAL FUNCTIONS -- MULTIPLE QUESTION TYPES #

def compile_options(block: str):
	block = block.split('\n')
	option_strs = []  # init
	options = {}  # init
	comma_replace = str(uuid.uuid4())
	for line in block:
		line = line.removeprefix('{').removesuffix('}')
		line = re.sub(r'(".*?)(,)(.*?")', rf'\g<1>{comma_replace}\3', line)
		line = re.sub(r'''('.*?)(,)(.*?')''', rf'\g<1>{comma_replace}\3', line)
		line = re.sub(r'(\(.*?)(,)(.*?\))', rf'\g<1>{comma_replace}\3', line)
		option_strs_raw = line.split(',')
		for option in range(len(option_strs_raw)):
			option_strs.append(option_strs_raw[option].replace(comma_replace, ','))
	for option in option_strs:
		option = option.replace(':', '=').replace("'", '').replace('"', '')
		option = option.split('=')
		if len(option) < 2:
			option.append('true')
		options.update({option[0]:option[1]})
	return options


def lines_compile(block: list):
	# init
	head = None
	options_str = ''
	description = ''
	q_specific = ''
	for line in block:
		if line.startswith('?'):
			head = line
		elif line.startswith('{'):
			options_str += line + '\n'
		elif line.startswith('>'):
			description += line.removeprefix('>').strip() + '\n'
		else:
			q_specific += line
	options = compile_options(options_str)
	description = markdown.markdown(description)
	return head, options, description


# BLOCKS -- DIRECT ACCESS #

def multiple_choice(block: str):
	block = block.split('\n')
	lines_compile(block)


def checkbox(block: str):
	print()


def dropdown(block: str):
	print()


def input(block: str):
	print()


def area(block: str):
	print()


def matrix(block: str):
	print()


def g_options(block: str):
	block = re.sub(r'\? ?options\n', '', block)
	g_options = compile_options(block)
	return g_options
