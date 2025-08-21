import re
import uuid
import markdown as md

# GLOBAL VARIABLES #

gen_id_used = {}  # store used ids for the ID generation


# GENERAL FUNCTIONS -- MULTIPLE QUESTION TYPES #

def compile_options(block: str):
	block = block.split('\n')
	# init
	option_strs = []
	options = {}
	comma_replace = str(uuid.uuid4())
	# option extract
	for line in block:
		line = line.removeprefix('{').removesuffix('}')
		line = re.sub(r'(".*?)(,)(.*?")', rf'\g<1>{comma_replace}\3', line)
		line = re.sub(r'''('.*?)(,)(.*?')''', rf'\g<1>{comma_replace}\3', line)
		line = re.sub(r'(\(.*?)(,)(.*?\))', rf'\g<1>{comma_replace}\3', line)
		option_strs_raw = line.split(',')
		for option in range(len(option_strs_raw)):
			option_strs.append(option_strs_raw[option].replace(comma_replace, ','))
	# option compile
	for option in option_strs:
		# : to =; remove all quotes
		option = option.replace(':', '=').replace("'", '').replace('"', '').lower()
		option = option.split('=')
		# assign true if valueless
		if len(option) == 1:
			option.append('true')
	return options


def gen_id(title: str, unique = True, unique_str = None):
	title = title.lower()
	id = re.sub(r'[^a-z0-9-]', '-', title)
	id = re.sub('-+', '-', id)
	if unique:
		if unique_str in gen_id_used:
			i = 1
			suffix = ''
			while id + suffix in gen_id_used[unique_str]:
				suffix = f'-{i}'
				i += 1
			id = id + suffix
			gen_id_used[unique_str].append(id)
		else:
			gen_id_used.update({unique_str:[id]})
	return id


def compile_lines(block: list):
	# init
	title = None
	options_str = ''
	description = ''
	q_specific = ''
	# sorting
	for line in block:
		if line.startswith('?'):
			title = line.removeprefix('?').strip()
		elif line.startswith('{'):
			options_str += line + '\n'
		elif line.startswith('>'):
			description += line.removeprefix('>').strip() + '\n'
		else:
			q_specific += line
	# post-processing
	title = md.markdown(title)
	options = compile_options(options_str)
	description = md.markdown(description)
	if 'opt' in options:
		options.update({'req':not options['opt']})
		options.pop('opt')
	if 'id' in options:
		qid = options['id']
	else:
		qid = gen_id(title, True, 'qid')
	return qid, title, options, description, q_specific


# BLOCKS -- DIRECT ACCESS #

def multiple_choice(block: str):
	block = block.split('\n')
	qid, title, options, description, q_specific = compile_lines(block)
	return f'''
	<div id="{qid}">
	
	</div>
	'''.strip()


def checkbox(block: str):
	print(block)


def dropdown(block: str):
	print(block)


def input_other(block: str):
	print(block)


def area(block: str):
	print(block)


def matrix(block: str):
	print(block)


def g_options(block: str):
	block = re.sub(r'\? ?options\n', '', block)
	options = compile_options(block)
	return options
