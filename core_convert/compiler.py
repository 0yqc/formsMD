import re
import uuid
import markdown as md

# GLOBAL VARIABLES #

gen_id_used = {}  # store used ids for the ID generation


# GENERAL FUNCTIONS -- MULTIPLE QUESTION TYPES #

def compile_options(block: str, g_options: dict):
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
			option.append(True)
		if option[1] == 'true':
			option[1] = True
		elif option[1] == 'false':
			option[1] = False
		options.update({option[0]:option[1]})
	for option in g_options:
		if not option in options:
			options.update({option:g_options[option]})
	if 'opt' in options:
		options.update({'req':not options['opt']})
		options.pop('opt')
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
	options = compile_options(options_str, g_options)
	if 'id' in options:
		qid = options['id']
	else:
		qid = gen_id(title, True, 'global_qid')
	title = md.markdown(title).removeprefix('<p>').removesuffix('</p>')
	description = md.markdown(description)
	return qid.strip(), title.strip(), options, description.strip(), q_specific.strip()


# BLOCKS -- BLOCK-SPECIFIC FUNCTIONS #

def options_answer(block: str, q_title: str, qid: str, req: bool, none_label: str):
	block = block.split('\n')
	# init
	answer = ''
	prechecked = False
	for line in block:
		options = {}  # reset
		if line.startswith('()') or line.startswith('( )'):
			line = line.removeprefix('()').removeprefix('( )').strip()
			anstype = 'unchecked'
		elif line.lower().startswith('(x)'):
			line = line.removeprefix('(x)').removeprefix('(X)').strip()
			anstype = 'checked'
			prechecked = True
		else:
			anstype = 'hidden'
		if '{' in line and '}' in line:
			line_parts = line.replace('}', '{').split('{')
			options = compile_options(line_parts[1], g_options = {})
			line = ' '.join(list(line_parts[0].strip()) + [item.strip() for item in line_parts[2:]])
		if 'id' in options:
			aid = options['id']
		else:
			aid = gen_id(line, True, f'local_{qid}')
		other = True if options.get('other') == True else False
		line = md.markdown(line).replace('<p>', ' ').replace('</p>', ' ').strip()  # don't allow multi-line labels / remove leading/trailing tags
		answer += f'''
		<div id="{qid}_ans_{aid}" class="answer_option{' hidden' if anstype == 'hidden' else ''}{' other' if other else ''}">
			<input type="radio" id="{qid}_ans_{aid}_input" name="{q_title} ({qid})" value="{line} ({aid})" required{' checked' if anstype == 'checked' else ''}{' style="visibility:hidden;"' if anstype == 'hidden' else ''}>
			{
		f'<span id="{qid}_ans_{aid}_label">{line}</span>'
		if anstype == 'hidden' else
		f'<label id="{qid}_ans_{aid}_label" for="{qid}_ans_{aid}_input">{line}</label>'
		}
			{
		f'<input type="text" id="{qid}_ans_{aid}_textinput" aria-label="Enter your answer for {line} (Other Input Field)" required name="{line} ({aid})">'
		if other else ''
		}
		</div>
		'''.replace('\n', '').replace('\t', '')
	if not req:
		answer += f"""
		<div id="{qid}_none" class="answer_option none">
			<input type="radio" id="{qid}_none_input" name="{q_title} ({qid})" value="{none_label} (none)"{' checked' if not prechecked else ''}>
			<label id="{qid}_none_label" for="{qid}_none_input">{none_label}</label>
		</div>
		""".replace('\n', '').replace('\t', '')
	return answer


# BLOCKS -- DIRECT ACCESS #

def options(block: str, g_options: dict):
	qid, title, options, description, q_specific = compile_lines(block, g_options)
	none_label = options.get('none_label') if options.get('none_label') else 'No Answer'
	answer = options_answer(q_specific, title, qid, options['req'], none_label)
	return f'''
	<fieldset id="{qid}" class="question radio{' required' if options['req'] else ''}">
		<legend id="{qid}_title" class="title">{title}</legend>
		<div id="{qid}_description" class="description">
			{description}
		</div>
		<div id="{qid}_answer" class="answer">
			{answer}
		</div>
	</fieldset>
	'''.replace('\n', '').replace('\t', '')


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
	options = compile_options(block, g_options = {})
	if 'opt' in options:
		options.update({'req':not options['opt']})
		options.pop('opt')
	if not 'req' in options:
		options.update({'req':'true'})
	return options
