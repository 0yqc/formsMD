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
		options.update({option[0]:option[1]})
	return options


def gen_id(label: str, unique = True, unique_str = None):
	label = label.lower()
	gid = re.sub(r'[^a-z0-9-]', '-', label)
	gid = re.sub('-+', '-', gid)
	gid = re.sub(r'^-+|-+$', '', gid)
	if unique:
		if unique_str in gen_id_used:
			i = 1
			suffix = ''
			while gid + suffix in gen_id_used[unique_str]:
				suffix = f'-{i}'
				i += 1
			gid = gid + suffix
			gen_id_used[unique_str].append(gid)
		else:
			gen_id_used.update({unique_str:[gid]})
	return gid


def compile_lines(block: str, g_options: dict):
	block = block.split('\n')
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
		elif line.strip():
			q_specific += line + '\n'
	# post-processing
	options = compile_options(options_str)
	if 'opt' in options:
		options.update({'req':not options['opt']})
		options.pop('opt')
	if not 'req' in options:  # apply global default
		options.update({'req':g_options['req']})
	if 'id' in options:
		qid = options['id']
	else:
		qid = gen_id(title, True, 'global_qid')
	title = md.markdown(title)
	description = md.markdown(description)
	return qid.strip(), title.strip(), options, description.strip(), q_specific.strip()


# BLOCKS -- BLOCK-SPECIFIC FUNCTIONS #

def radio_answer(block: str, req: str, qid: str):
	block = block.split('\n')
	# init
	answer = ''
	options = {}
	for line in block:
		if line.startswith('()') or line.startswith('( )'):
			line = line.removeprefix('()').removeprefix('( )').strip()
			anstype = 'unchecked'
		elif line.lower().startswith('(x)'):
			line = line.removeprefix('(x)').removeprefix('(X)').strip()
			anstype = 'checked'
		else:
			anstype = 'hidden'
		if '{' in line and '}' in line:
			split = line.replace('}', '{').split('{')
			options = compile_options(split[1])
			line = ' '.join(list(split[0].strip()) + [item.strip() for item in split[2:]])
		if 'id' in options:
			aid = options['id']
		else:
			aid = gen_id(line, True, f'local_{qid}')
		req = True if options.get('req') == 'true' else req
		other = True if options.get('id') == 'other' else False
		line = md.markdown(line).replace('<p>', ' ').replace('</p>', ' ').strip()  # don't allow multi-line labels / remove leading/trailing tags
		answer += f'''
		<div id="{qid}_{aid}" class="answer_option radio{' required' if req else ''}{' hidden' if anstype == 'hidden' else ''}{' other' if other else ''}">
			<input type="radio" id="{qid}_{aid}_input" name="{qid}" value="{aid}"{' required' if req else ''}{' checked' if anstype == 'checked' else ''}{' style="visibility:hidden;"' if anstype == 'hidden' else ''}>
			{
		f'<span id="{qid}_{aid}_label">{line}</span>'
		if anstype == 'hidden' else
		f'<label id="{qid}_{aid}_label" for="{qid}_{aid}_input">{line}</label>'
		}
			{
		f'<input type="text" id="{qid}_{aid}_textinput" aria-label="Enter your answer for {line} (Other Input Field)">'
		if other else ''
		}
		</div>
		'''.replace('\n', '').replace('\t', '')
	return answer


# BLOCKS -- DIRECT ACCESS #

def radio(block: str, g_options: dict):
	qid, title, options, description, q_specific = compile_lines(block, g_options)
	answer = radio_answer(q_specific, options['req'], qid)
	return f'''
	<fieldset id="{qid}" class="question radio">
		<div id="{qid}_title" class="title">{title}</div>
		<div id="{qid}_description" class="description">
			{description}
		</div>
		<div id="{qid}_answer" class="answer">
			{answer}
		</div>
	</fieldset>
	'''.replace('\n', '').replace('\t', '')


def checkbox(block: str, g_options: dict):
	print(block)


def dropdown(block: str, g_options: dict):
	print(block)


def input_other(block: str, g_options: dict):
	print(block)


def area(block: str, g_options: dict):
	print(block)


def matrix(block: str, g_options: dict):
	print(block)


def global_options(block: str):
	block = block.replace('? options\n', '').replace('?options\n', '')
	options = compile_options(block)
	if 'opt' in options:
		options.update({'req':not options['opt']})
		options.pop('opt')
	if not 'req' in options:
		options.update({'req':'true'})
	return options
