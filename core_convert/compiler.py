import re
import markdown as md

# GLOBAL VARIABLES #

gen_id_used = {}  # store used ids for the ID generation


# GENERAL FUNCTIONS -- MULTIPLE QUESTION TYPES #

def compile_options(block: str, g_options: dict):
	if not block.strip():
		return g_options
	block = block.split('\n')
	option_str = ''
	for line in block:
		line = line.removeprefix('{').removesuffix('}')
		if line.strip():
			option_str += line + ','
	# init
	enquoted = False
	enquoted_by = ''
	c_type = 'key'  # key / value
	construct = ''
	key = ''
	options = {}
	for char in option_str:
		if (char == '=' or char == ':') and c_type == 'key' and not enquoted:
			key = construct
			construct = ''
			c_type = 'value'
		elif char == ',' and c_type == 'key' and not enquoted:
			options.update({construct: True})
			construct = ''
			c_type = 'key'
		elif char == ',' and c_type == 'value' and not enquoted:
			options.update({key: construct})
			construct = ''
			c_type = 'key'
		elif char in ['\'', '\"'] and not enquoted:
			enquoted = True
			enquoted_by = char
		elif char == enquoted_by:
			enquoted = False
			enquoted_by = ''
		else:
			construct += char
	options.update(g_options)
	if 'opt' in options:
		options.update({'req': not options['opt']})
		options.pop('opt')
	if not 'req' in options:
		options.update({'req': True})
	return options


def gen_id(label: str, unique = True, unique_str = None):
	label = label.lower()
	gid = re.sub(r'[^a-z0-9-]', '-', label)
	gid = re.sub('-+', '-', gid)
	gid = re.sub(r'^-|-$', '', gid)
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
			gen_id_used.update({unique_str: [gid]})
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
	if options_str or g_options:
		options = compile_options(options_str, g_options)
	else:
		options = {'req': True}
	if 'id' in options:
		qid = options['id']
	else:
		qid = gen_id(title, True, 'global_qid')
	title = md.markdown(title).removeprefix('<p>').removesuffix('</p>')
	description = md.markdown(description)
	return qid.strip(), title.strip(), options, description.strip(), q_specific.strip()


# BLOCKS -- BLOCK-SPECIFIC FUNCTIONS #

def radio_answer(block: str, q_title: str, qid: str, q_options: dict):
	block = block.split('\n')
	# init
	answer = ''
	prechecked = False
	req = q_options['req']
	none_label = q_options['none_label'] if 'none_label' in q_options else 'No Answer'
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
			aid = gen_id(aid, True, f'local_{qid}')
		else:
			aid = gen_id(line, True, f'local_{qid}')
		other = True if options.get('other') == True else False
		other_type = options.get('other_type') if 'other_type' in options else 'text'
		line = md.markdown(line).replace('<p>', ' ').replace('</p>', ' ').strip()  # don't allow multi-line labels / remove leading/trailing tags
		answer += f'''
		<div id="{qid}__{aid}" class="answer_option{' hidden' if anstype == 'hidden' else ''}{' other' if other else ''}">
			<input type="radio" id="{qid}__{aid}_input" name="{q_title} ({qid})" value="{line} ({aid})" required{' checked' if anstype == 'checked' else ''}{' style="visibility:hidden;"' if anstype == 'hidden' else ''}{options['attr'] if 'attr' in options else ''}>
			{
		f'<span id="{qid}__{aid}_label">{line}</span>'
		if anstype == 'hidden' else
		f'<label id="{qid}__{aid}_label" for="{qid}__{aid}_input">{line}</label>'
		}
			{
		f'<input type="{other_type}" id="{qid}__{aid}_textinput" aria-label="Enter your answer for {line} (Other Input Field)" required name="{line} ({aid})">'
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


def checkbox_answer(block: str, q_title: str, qid: str, q_options: dict):
	block = block.split('\n')
	# init
	answer = ''
	req = q_options['req']
	for line in block:
		options = {}  # reset
		if line.startswith('[]') or line.startswith('[ ]'):
			line = line.removeprefix('[]').removeprefix('[ ]').strip()
			anstype = 'unchecked'
		elif line.lower().startswith('[x]'):
			line = line.removeprefix('[x]').removeprefix('[X]').strip()
			anstype = 'checked'
		else:
			anstype = 'hidden'
		if '{' in line and '}' in line:
			line_parts = line.replace('}', '{').split('{')
			options = compile_options(line_parts[1], g_options = {})
			line = ' '.join(list(line_parts[0].strip()) + [item.strip() for item in line_parts[2:]])
		if 'id' in options:
			aid = options['id']
			aid = gen_id(aid, True, f'local_{qid}')
		else:
			aid = gen_id(line, True, f'local_{qid}')
		other = True if options.get('other') == True else False
		other_type = options.get('other_type') if 'other_type' in options else 'text'
		line = md.markdown(line).replace('<p>', ' ').replace('</p>', ' ').strip()  # don't allow multi-line labels / remove leading/trailing tags
		answer += f'''
		<div id="{qid}__{aid}" class="answer_option{' hidden' if anstype == 'hidden' else ''}{' other' if other else ''}">
			<input type="checkbox" id="{qid}__{aid}_input" name="{q_title} ({qid}): {line} ({aid})" {' required' if req else ''}{' checked' if anstype == 'checked' else ''}{' style="visibility:hidden;"' if anstype == 'hidden' else ''}{options['attr'] if 'attr' in options else ''}>
			{
		f'<span id="{qid}__{aid}_label">{line}</span>'
		if anstype == 'hidden' else
		f'<label id="{qid}__{aid}_label" for="{qid}__{aid}_input">{line}</label>'
		}
			{
		f'<input type="{other_type}" id="{qid}__{aid}_textinput" aria-label="Enter your answer for {line} (Other Input Field)" required name="{line} ({aid})">'
		if other else ''
		}
		</div>
		'''.replace('\n', '').replace('\t', '')
	return answer


def dropdown_answer(block: str, qid: str, options: dict):
	block = block.split('\n')
	# init
	optgroup_close = False
	answer = ''
	optgroup_close = False
	prechecked = False
	req = options['req']
	multi = options['multiple'] if 'multiple' in options else False
	none_label = options['none_label'] if 'none_label' in options else 'No Answer'
	select_label = options['select_label'] if 'select_label' in options else ('Select an item to add...' if multi else 'Select an option...')
	for line in block:
		options = {}  # reset
		if line.startswith('||') or line.startswith('| |'):
			line = line.removeprefix('||').removeprefix('| |').strip()
			anstype = 'unchecked'
		elif line.lower().startswith('|x|'):
			line = line.removeprefix('|x|').removeprefix('|X|').strip()
			anstype = 'checked'
			prechecked = True
		elif line == '---':
			answer += '<hr>'
			continue
		else:
			anstype = 'hidden'
		if '{' in line and '}' in line:
			line_parts = line.replace('}', '{').split('{')
			options = compile_options(line_parts[1], g_options = {})
			line = ' '.join(list(line_parts[0].strip()) + [item.strip() for item in line_parts[2:]])
		if 'id' in options:
			aid = options['id']
			aid = gen_id(aid, True, f'local_{qid}')
		else:
			aid = gen_id(line, True, f'local_{qid}')
		if not anstype == 'hidden':
			answer += f'''
				<option id="{qid}__{aid}" value="{line} ({aid})"{' selected' if anstype == 'checked' and not multi else ''}{' class="selected"' if multi and anstype == 'checked' else ''}>{line}</option>
				'''.replace('\n', '').replace('\t', '')
		else:
			if optgroup_close:
				answer += '</optgroup>'
			answer += f'''
				<optgroup id="{aid}__{aid}" label="{line}">
				'''.replace('\n', '').replace('\t', '')
			optgroup_close = True
	if optgroup_close:
		answer += '</optgroup>'
	if not prechecked and not multi:
		answer = f'''
			<option id="{qid}_none" value="">{select_label}</option>
			<hr>
			'''.replace('\n', '').replace('\t', '') + answer
	if not req and not multi:
		answer += f'''
			<hr>
			<option id="{qid}_none" value="">{none_label}</option>
			'''.replace('\n', '').replace('\t', '')
	if multi:
		answer = f'''
			<option id="{qid}_none" value="">{select_label}</option>
			<hr>
			'''.replace('\n', '').replace('\t', '') + answer
	return answer


def input_answer(block: str, q_title: str, qid: str, options: dict):
	datalist = block.split('\n')
	# init
	req = options['req']
	anstype = options['type'] if 'type' in options else 'text'
	answer = f'''
		<input id="{qid}_ans" type="{anstype}" class="answer" name="{q_title} ({qid})"{' required' if req else ''}{f' list="{qid}_datalist"' if datalist else ''}{options['attr'] if 'attr' in options else ''}>
		'''.replace('\n', '').replace('\t', '')
	if datalist:
		answer += f'''
		<datalist id="{qid}_datalist">
		'''.replace('\n', '').replace('\t', '')
		for suggestion in datalist:
			answer += f'<option value="{suggestion}"></option>'
		answer += '</datalist>'
	return answer


def area_answer(q_title: str, qid: str, options: dict):
	# init
	req = options['req']
	answer = f'''
		<textarea id="{qid}_ans" class="answer" name="{q_title} ({qid})"{' required' if req else ''} {options['attr'] if 'attr' in options else ''}></textarea>
		'''.replace('\n', '').replace('\t', '')
	return answer


def matrix_answer(block: str, q_title: str, qid: str, options: dict):
	# init
	block = block.split('\n')
	req = options['req']
	type = options['type']
	cols_list = block[0].split('|')
	cols = {}
	for col in cols_list:
		col = col.strip()
		if '{' in col and '}' in col:
			options = {}
			line_parts = col.replace('}', '{').split('{')
			options = compile_options(line_parts[1], g_options = {})
			col = ' '.join(list(line_parts[0].strip()) + [item.strip() for item in line_parts[2:]])
		if 'id' in options:
			aid = options['id']
			aid = gen_id(aid, True, f'local_{qid}')
		else:
			aid = gen_id(col, True, f'local_{qid}')
		col = md.markdown(col).replace('<p>', '').replace('</p>', '')
		cols.update({col: aid})
	block.pop(0)
	rows = {}
	for row in block:
		row = row.strip()
		if '{' in row and '}' in row:
			options = {}
			line_parts = row.replace('}', '{').split('{')
			options = compile_options(line_parts[1], g_options = {})
			row = ' '.join(list(line_parts[0].strip()) + [item.strip() for item in line_parts[2:]])
		if 'id' in options:
			aid = options['id']
			aid = gen_id(aid, True, f'local_{qid}')
		else:
			aid = gen_id(row, True, f'local_{qid}')
		row = md.markdown(row).replace('<p>', '').replace('</p>', '')
		rows.update({row: aid})
	answer = f'''
		<table>
			<thead>
				<tr>
					<th></th>
		'''.replace('\n', '').replace('\t', '')
	for col in cols:
		answer += f'<th class="head {col}">{col}</th>'
	if type == 'radio':
		specific_answer = matrix_answer_radio(cols, rows, q_title, qid)
	elif type == 'checkbox':
		specific_answer = matrix_answer_checkbox(cols, rows, q_title, qid)
	elif type == 'area':
		specific_answer = matrix_answer_area(cols, rows, q_title, qid)
	else:
		specific_answer = matrix_answer_other(cols, rows, q_title, qid, type)
	answer += f'''
				</tr>
			</thead>
			<tbody>
				{specific_answer}
			</tbody>
		</table>
		'''.replace('\n', '').replace('\t', '')
	return answer


# MATRIX ANSWERS #

def matrix_answer_radio(cols: dict, rows: dict, q_title: str, qid: str):
	answer = ''
	for row in rows:
		rid = rows[row]
		answer += f'<tr><th>{row}</th>'
		for col in cols:
			cid = cols[col]
			answer += f'<td><input id="{qid}__{rid}__{cid}_inp" type="radio" name="{qid}: {row} ({qid}__{rid})" value="{col} ({cid})" aria-label="Input for {row}/{col}"></input></td>'
		answer += '</tr>'
	return answer


def matrix_answer_checkbox(cols: dict, rows: dict, q_title: str, qid: str):
	answer = ''
	for row in rows:
		rid = rows[row]
		answer += f'<tr><th>{row}</th>'
		for col in cols:
			cid = cols[col]
			answer += f'<td><input id="{qid}__{rid}__{cid}_inp" type="checkbox" name="{qid}: {row}/{col} ({qid}__{rid}__{cid})" aria-label="Input for {row}/{col}"></input></td>'
		answer += '</tr>'
	return answer


def matrix_answer_area(cols: dict, rows: dict, q_title: str, qid: str):
	answer = ''
	for row in rows:
		rid = rows[row]
		answer += f'<tr><th>{row}</th>'
		for col in cols:
			cid = cols[col]
			answer += f'<td><textarea id="{qid}__{rid}__{cid}_inp" name="{qid}: {rid}/{cid} ({qid}__{rid}__{cid})" aria-label="Input for {row}/{col}"></textarea></td>'
		answer += '</tr>'
	return answer


def matrix_answer_other(cols: dict, rows: dict, q_title: str, qid: str, type: str):
	answer = ''
	for row in rows:
		rid = rows[row]
		answer += f'<tr><th>{row}</th>'
		for col in cols:
			cid = cols[col]
			answer += f'<td><input id="{qid}__{rid}__{cid}_inp" type="{type}" name="{qid}: {row}/{col} ({qid}__{rid}__{cid})" aria-label="Input for {row}/{col}"></input></td>'
		answer += '</tr>'
	return answer
