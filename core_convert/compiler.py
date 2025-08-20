import re
import uuid

# GENERAL FUNCTIONS -- MULTIPLE QUESTION TYPES #

def compile_options(option_lines: str):
	option_lines = option_lines.split('\n')
	option_strs = []
	options = {} # init
	comma_replace = str(uuid.uuid4())
	for line in option_lines:
		line = line.removeprefix('{').removesuffix('}')
		line = re.sub(r'(".*?)(,)(.*?")', rf'\g<1>{comma_replace}\3', line)
		line = re.sub(r'''('.*?)(,)(.*?')''', rf'\g<1>{comma_replace}\3', line)
		line = re.sub(r'(\(.*?)(,)(.*?\))', rf'\g<1>{comma_replace}\3', line)
		option_strs_raw = line.split(',')
		for option in range(len(option_strs_raw)):
			option_strs.append(option_strs_raw[option].replace(comma_replace,','))
	for option in option_strs:
		option = option.replace(':', '=').replace("'", '').replace('"', '')
		option = option.split('=')
		if len(option) < 2:
			option.append('true')
		options.update({option[0]: option[1]})
	return options



# BLOCKS -- DIRECT ACCESS #

def multiple_choice(block: str):
	None


def checkbox(block: str):
	None


def dropdown(block: str):
	None


def input(block: str):
	None


def area(block: str):
	None


def matrix(block: str):
	None


def g_options(block: str):
	block = re.sub(r'\? ?options\n','',block)
	g_options = compile_options(block)
	return g_options