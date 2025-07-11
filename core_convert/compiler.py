import re

# --- VARS --- #

used_qid = []


# --- ALL BLOCKS --- #

def q_head(line: str):  #
	title = ':'.join(line.split(':')[1:]).strip()  # everything from the first ':', stripped, so spaces won't matter
	if line.split(':')[0][
	   1:].strip() and ':' in line:  # if there is a given id (there is something between '?' and ':' / end of str and there even is ':')
		qid = line.split(':')[0][
			  1:].strip()  # everything until the first ':', cut off the first char (?), then strip (remove trailing/leading whitespaces)
	else:  # an id needs to be generated
		qid = re.sub('[^a-zA-Z\d-]', '-', title).lower()  # replace anything except alphanumeric chars and '-' to - and turn it lowercase
		qid = re.sub('-+', '-', qid)  # replace any amount of consecutive hyphens with one
		qid.strip('-')  # remove starting / trailing hyphens
		# system to only use each qid once: (append numbers otherwise)
		i = 0
		if qid in used_qid:
			while qid in used_qid:
				i += 1
				if not (qid + '-' + i) in used_qid:
					break
			used_qid.append(qid + '-' + i)
			qid = qid + '-' + i
		else:
			used_qid.append(qid)
	return qid, title


def q_description(descr: str):
	descr = descr.replace('\n\t>', '\n')  # remove quotes
	descr = re.sub('\n *', '\n', descr)  # remove leading whitespaces
	descr = '<p>' + descr + '</p>'
	descr = descr.replace('\n\n', '</p><p>')  # insert new paragraph on double newline
	return descr


def options_compile(line: str):
	options_re = re.findall('''([^,\n\t]+)(=)('[^']*'|"[^"]*"|[^,]+)''', line)  # finds all label=value
	options = {}
	for i in options_re:
		options.update({str(i[0].strip('\'"')):str(i[2].strip('\'"'))})  # update the dict with the new option, which will get quotes removed and turned into a string
	return options


# --- BLOCK SPECIFIC --- #

def checkbox_answer(line: str, qid: str, count: int):
	if ':' in line:  # an id was set
		aid = line.split(']')[1].split(':')[0].strip()  # between ']' and ':', striped
		line = line.split(']')[0] + ']' + ':'.join(line.split(':')[1:])  # remove id from line
	else:
		aid = count  # the nth option
	if aid == 'other':
		if line.startswith(('[]', '[ ]')):
			label = re.sub('\[ *\]', '', line).strip()  # remove checkbox symbol (with(-out) space(s) in between), striped
			return f'<div id="{qid}_{aid}" class="answer checkbox other" markdown><input type="checkbox" name="{qid}_checkbox" id="{qid}_{aid}_checkbox" value="{qid}_{aid}"><label for="{qid}_{aid}_checkbox" id="{qid}_{aid}_label">{label}</label><input type="text" class="answer checkbox text other" id="{qid}_{aid}_other" name="{qid}_{aid}_other"></div>'
		elif line.lower().startswith('[x]'):
			label = line.replace('[x]', '').strip()  # get label text
			return f'<div id="{qid}_{aid}" class="answer checkbox other" markdown><input type="checkbox" name="{qid}_checkbox" id="{qid}_{aid}_checkbox" value="{qid}_{aid}" checked><label for="{qid}_{aid}_checkbox" id="{qid}_{aid}_label">{label}</label><input type="text" class="answer checkbox text other" id="{qid}_{aid}_other" name="{qid}_{aid}_other"></div>'
	elif line.startswith(('[]', '[ ]')):  # empty checkbox
		label = re.sub('\[ *]', '', line).strip()  # remove checkbox symbol (with(-out) space(s) in between), striped
		return f'<div id="{qid}_{aid}" class="answer checkbox" markdown><input type="checkbox" name="{qid}_{aid}" id="{qid}_{aid}_checkbox"></input><label for="{qid}_{aid}_checkbox" id="{qid}_{aid}_label">{label}</label></div>'
	elif line.lower().startswith('[x]'):
		label = line.replace('[x]', '').strip()  # remove checkbox symbol, striped
		return f'<div id="{qid}_{aid}" class="answer checkbox" markdown><input type="checkbox" name="{qid}_{aid}" id="{qid}_{aid}_checkbox" checked></input><label for="{qid}_{aid}_checkbox" id="{qid}_{aid}_label">{label}</label></div>'
	else:  # fake paragraph
		label = line.strip()
		return f'<div id="{qid}_{aid}" class="answer text" markdown><input type="checkbox" name="{qid}_{aid}" id="{qid}_{aid}_checkbox" style="visibility:hidden;"></input><label id="{qid}_{aid}_label">{label}</label></div>'


def multiple_choice_answer(line: str, qid: str, count: int):
	if ':' in line:  # an id was set
		aid = line.split(')')[1].split(':')[0].strip()  # between ')' and ':', striped
		line = line.split(')')[0] + ')' + ':'.join(line.split(':')[1:])  # remove id from line
	else:
		aid = count  # the nth option
	if aid == 'other':
		if line.startswith(('()', '( )')):
			label = re.sub('\( *\)', '', line).strip()  # remove radio symbol (with(-out) space(s) in between), striped
			return f'<div id="{qid}_{aid}" class="answer multiple-choice other" markdown><input type="radio" name="{qid}_radio" id="{qid}_{aid}_radio" value="{qid}_{aid}"><label for="{qid}_{aid}_radio" id="{qid}_{aid}_label">{label}</label><input type="text" class="answer multiple-choice text other" id="{qid}_{aid}_other" name="{qid}_{aid}_other"></div>'
		elif line.lower().startswith('(x)'):
			label = line.replace('(x)', '').strip()  # get label text
			return f'<div id="{qid}_{aid}" class="answer multiple-choice other" markdown><input type="radio" name="{qid}_radio" id="{qid}_{aid}_radio" value="{qid}_{aid}" checked><label for="{qid}_{aid}_radio" id="{qid}_{aid}_label">{label}</label><input type="text" class="answer multiple-choice text other" id="{qid}_{aid}_other" name="{qid}_{aid}_other"></div>'
	elif line.startswith(('()', '( )')):  # unchecked radio select
		label = re.sub('\( *\)', '', line).strip()  # remove radio symbol (with(-out) space(s) in between), striped
		return f'<div id="{qid}_{aid}" class="answer multiple-choice" markdown><input type="radio" name="{qid}_radio" id="{qid}_{aid}_radio" value="{qid}_{aid}"><label for="{qid}_{aid}_radio" id="{qid}_{aid}_label">{label}</label></div>'
	elif line.lower().startswith('(x)'):
		label = line.replace('(x)', '').strip()  # remove radio symbol
		return f'<div id="{qid}_{aid}" class="answer multiple-choice" markdown><input type="radio" name="{qid}_radio" id="{qid}_{aid}_radio" value="{qid}_{aid}" checked><label for="{qid}_{aid}_radio" id="{qid}_{aid}_label">{label}</label></div>'
	else:
		label = line.strip()
		return f'<div id="{qid}_{aid}" class="answer text" markdown><input type="radio" name="{qid}_{aid}" id="{qid}_{aid}_radio" style="visibility:hidden;"></input><label id="{qid}_{aid}_label">{label}</label></div>'


# --- BLOCKS --- #

def checkbox(block: str):
	lines = block.split('\n')  # create array of lines
	qid, title = q_head(lines[0])  # generate the qid (question id) and title
	i = 1  # line counter, first line already done
	descr = ''  # init
	aid = 0  # init
	answer_html = ''  # init
	descr_started = False  # init
	while i < len(lines):  # alternate syntax to "for line in lines" to dynamically change the current line number
		if lines[i].startswith('\t>'):  # description lines
			descr += '\n' + lines[i]  # add the current line to the description tag
			descr_started = True
			# go to the next line:
			i += 1
			continue
		elif descr_started:  # only if the construction of the description has started already and the line doesn't start with > (because of 'el'if)
			descr = q_description(descr)  # the description is done, so it will be generated
			descr_started = False
		if lines[i].startswith(('\t[', '\t\t')):  # checkbox or paragraph
			answer_html += checkbox_answer(lines[i].strip(), qid, aid)  # add checkbox line to the options
			aid += 1
		i += 1  # go to next line
	return f'<div id="{qid}" class="question checkbox" markdown><h3 id="{qid}_title" class="question checkbox title">{title}</h3><div id="{qid}_description" class="question checkbox description">{descr}</div>{answer_html}</div>\n'


def multiple_choice(block: str):
	lines = block.split('\n')  # create array of lines
	qid, title = q_head(lines[0])  # generate the qid (question id) and title
	i = 1  # line counter
	descr = ''  # init
	aid = 0  # init
	answer_html = ''  # init
	descr_started = False  # init
	while i < len(lines):  # alternate syntax to "for line in lines" to dynamically change the current line number
		if lines[i].startswith('\t>'):  # description lines
			descr += '\n' + lines[i]  # add the current line to the description tag
			descr_started = True
			# go to the next line:
			i += 1
			continue
		elif descr_started:  # only if the construction of the description has started already and the line doesn't start with > (because of 'el'if)
			descr = q_description(descr)  # the description is done, so it will be generated
			descr_started = False
		if lines[i].startswith(('\t(', '\t\t')):  # checkbox or paragraph
			answer_html += multiple_choice_answer(lines[i].strip(), qid, aid)  # add checkbox line to the options
			aid += 1
		i += 1  # go to next line
	return f'<div id="{qid}" class="question multiple-choice" markdown><h3 id="{qid}_title" class="question multiple-choice title">{title}</h3><div id="{qid}_description" class="question multiple-choice description">{descr}</div>{answer_html}</div>\n'


def text(block: str):
	lines = block.split('\n')  # create array of lines
	qid, title = q_head(lines[0])  # generate the qid (question id) and title
	i = 1  # line counter
	descr = ''  # init
	options = {}  # init
	while i < len(lines):  # alternate syntax to "for line in lines" to dynamically change the current line number
		if lines[i].startswith('\t>'):  # description lines
			descr += '\n' + lines[i]  # add the current line to the description tag
			# go to the next line:
			i += 1
			continue
		if not lines[i].startswith('\t>'):  # must be an option line
			options.update(options_compile(lines[i]))
		i += 1
	descr = q_description(descr)  # the description is done, so it will be generated # generate description
	try:
		inp_type = options['type']
	except KeyError:
		inp_type = 'text'
	try:
		placeholder = options['placeholder']
	except KeyError:
		placeholder = ''
	try:
		value = options['value']
	except KeyError:
		value = ''
	return f'<div id="{qid}" class="question text {inp_type}" markdown><h3 id="{qid}_title" class="question text {inp_type} title">{title}</h3><div id="{qid}_description" class="question text {inp_type} description">{descr}</div><input type="{inp_type}" id="{qid}_input" name="{qid}" class="answer text {inp_type}" placeholder="{placeholder}" value="{value}"></input></div>\n'


def area(block: str):
	lines = block.split('\n')  # create array of lines
	qid, title = q_head(lines[0])  # generate the qid (question id) and title
	i = 1  # line counter
	descr = ''  # init
	options = {}
	while i < len(lines):  # alternate syntax to "for line in lines" to dynamically change the current line number
		if lines[i].startswith('\t>'):  # description lines
			descr += '\n' + lines[i]  # add the current line to the description tag
			# go to the next line:
			i += 1
			continue
		if not lines[i].startswith('\t>'):  # must be an option line
			options.update(options_compile(lines[i]))
		i += 1
	descr = q_description(descr)  # the description is done, so it will be generated # generate description
	try:
		placeholder = options['placeholder']
	except KeyError:
		placeholder = ''
	try:
		value = options['value']
	except KeyError:
		value = ''
	try:
		rows = options['rows']
	except KeyError:
		rows = '4'
	return f'<div id="{qid}" class="question text area textarea" markdown><h3 id="{qid}_title" class="question text area title">{title}</h3><div id="{qid}_description" class="question text area description">{descr}</div><textarea id="{qid}_input" name="{qid}" rows="{rows}" placeholder="{placeholder}">{value}</textarea></div>\n'


def g_options(block: str):
	option_lines = block.split('\n')[1:]  # line 1ff
	options = {}
	for i in option_lines:
		options.update(options_compile(i))
	return options
