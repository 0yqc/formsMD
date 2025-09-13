import compiler  # local file to compile single blocks
import re # regex filtering


def file(file_path):
	with open(file_path, 'r') as f:
		lines = f.readlines()
	options = {}
	for i in range(len(lines)):
		block_str = ''
		if lines[i].startswith('\?'):
			lines[i] = lines[i].removeprefix('\\')
			continue
		elif lines[i].startswith('?'):
			while lines[i].strip():
				block_str += lines[i].strip() + '\n'
				lines[i] = ''
				i += 1
				if i < len(lines):
					continue
				else:
					i -= 1
					break
			lines[i], new_options = block(block_str.strip(),options)
			lines[i] = '\n\n' + lines[i] + '\n\n'
			options.update(new_options)
		else:
			lines[i] = lines[i]
	return ''.join(lines), options


def block(text: str, options: dict):  # block compiling logic
	new_options = {}  # init
	if re.findall('\n\[.?]', text):  # checkbox question
		text = checkbox(text, options)
	elif re.findall('\n\(.?\)', text):  # multiple choice question
		text = radio(text, options)
	elif '\n|' in text:
		text = dropdown(text, options)
	elif 'type=matrix_' in text:
		text = matrix(text, options)
	elif 'type=area' in text:
		text = area(text, options)
	elif 'type=' in text:
		text = input_other(text, options)
	elif 'options' in text:
		new_options = global_options(text)
		text = ''
	return text, new_options


# BLOCKS -- DIRECT ACCESS #

def radio(block: str, g_options: dict):
	qid, title, options, description, q_specific = compiler.compile_lines(block, g_options)
	none_label = options.get('none_label') if options.get('none_label') else 'No Answer'
	answer = compiler.radio_answer(q_specific, title, qid, options['req'], none_label)
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
	options = compiler.compile_options(block, g_options = {})
	if 'opt' in options:
		options.update({'req':not options['opt']})
		options.pop('opt')
	if not 'req' in options:
		options.update({'req':'true'})
	return options