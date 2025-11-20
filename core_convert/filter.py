import compiler  # local file to compile single blocks
import re  # regex filtering


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
			lines[i], new_options = compile_block(block_str.strip(), options)
			lines[i] = '\n\n' + lines[i] + '\n\n'
			options.update(new_options)
		else:
			lines[i] = lines[i]
	return ''.join(lines), options


def compile_block(text: str, options: dict):  # block compiling logic
	new_options = {}  # init
	if re.findall(r'\n\[.?]', text):  # checkbox question
		text = checkbox(text, options)
	elif re.findall(r'\n\(.?\)', text):  # multiple choice question
		text = radio(text, options)
	elif '\n|' in text:
		if 'multiple' in text:
			text = dropdown_multi(text, options)
		else:
			text = dropdown(text, options)
	elif re.findall(r'type[=:].?matrix', text):
		text = matrix(text, options)
	elif '?options' in text or '? options' in text:
		new_options = global_options(text)
		text = ''
	else:
		text = other_input(text, options)
	return text, new_options


# BLOCKS -- DIRECT ACCESS #

def radio(block: str, g_options: dict):
	qid, title, options, description, q_specific = compiler.compile_lines(block, g_options)
	answer = compiler.radio_answer(q_specific, title, qid, options)
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
	qid, title, options, description, q_specific = compiler.compile_lines(block, g_options)
	answer = compiler.checkbox_answer(q_specific, title, qid, options)
	return f'''
		<fieldset id="{qid}" class="question checkbox{' required' if options['req'] else ''}">
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
	qid, title, options, description, q_specific = compiler.compile_lines(block, g_options)
	select = compiler.dropdown_answer(q_specific, qid, options)
	return f'''
		<fieldset id="{qid}" class="question dropdown{' required' if options['req'] else ''}">
			<legend id="{qid}_title" class="title">
				<label id="{qid}_label" for="{qid}_select">{title}</label>
			</legend>
			<div id="{qid}_description" class="description">
				{description}
			</div>
			<div id="{qid}_answer" class="answer">
				<select id="{qid}_select" name="{title} ({qid})"{' required' if options['req'] else ''}{options['attr'] if 'attr' in options else ''}>
					{select}
				</select>
			</div>
		</fieldset>
		'''.replace('\n', '').replace('\t', '')


def dropdown_multi(block: str, g_options: dict):
	qid, title, options, description, q_specific = compiler.compile_lines(block, g_options)
	select = compiler.dropdown_answer(q_specific, qid, options)
	return f'''
		<fieldset id="{qid}" class="question dropdown multiple{' required' if options['req'] else ''}">
			<legend id="{qid}_title" class="title">
				<label id="{qid}_label" for="{qid}_select">{title}</label>
			</legend>
			<div id="{qid}_description" class="description">
				{description}
			</div>
			<div id="{qid}_answer" class="answer">
				<div id="{qid}_answers" class="answers"></div>
				<select id="{qid}_select" class="multiple" {options['attr'] if 'attr' in options else ''}>
					{select}
				</select>
				<input id="{qid}_hidden" type="hidden" name="{title} ({qid}): Selected Elements" value=""></input>
			</div>
		</fieldset>
		'''.replace('\n', '').replace('\t', '')


def other_input(block: str, g_options: dict):
	qid, title, options, description, q_specific = compiler.compile_lines(block, g_options)
	if options.get('type') == 'area' or options.get('type') == 'textarea':
		answer = compiler.area_answer(title, qid, options)
	else:
		answer = compiler.input_answer(q_specific, title, qid, options)
	return f'''
		<fieldset id="{qid}" class="question {options['type'] if 'type' in options else 'text'}{' required' if options['req'] else ''}">
			<legend id="{qid}_title" class="title">
				<label id="{qid}_label" for="{qid}_ans">{title}</label>
			</legend>
			<div id="{qid}_description" class="description">
				{description}
			</div>
			<div id="{qid}_answer" class="answer">
				{answer}
			</div>
		</fieldset>
		'''.replace('\n', '').replace('\t', '')


def matrix(block: str, g_options: dict):
	qid, title, options, description, q_specific = compiler.compile_lines(block, g_options)
	if options.get('type') == 'matrix':
		options['type'] = 'radio'
	else:
		options['type'] = options['type'].removeprefix('matrix_')
	answer = compiler.matrix_answer(q_specific, title, qid, options)
	return f'''
		<fieldset id="{qid}" class="question matrix {options['type']}{' required' if options['req'] else ''}">
			<legend id="{qid}_title" class="title">
				{title}
			</legend>
			<div id="{qid}_description" class="description">
				{description}
			</div>
			<div id="{qid}_answer" class="answer">
				{answer}
			</div>
		</fieldset>
		'''.replace('\n', '').replace('\t', '')


def global_options(block: str):
	block = block.replace('? options\n', '').replace('?options\n', '')
	options = compiler.compile_options(block, g_options = {})
	if 'opt' in options:
		options.update({'req': not options['opt']})
		options.pop('opt')
	if not 'req' in options:
		options.update({'req': 'true'})
	return options
