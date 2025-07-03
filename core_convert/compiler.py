import re

# --- VARS --- #

used_qid = []


# --- ALL BLOCKS --- #

def q_head(line: str):  #
	title = ':'.join(line.split(':')[1:]).strip()  # everything from the first ':', stripped, so spaces won't matter
	if line.split(':')[0][
	   1:].strip() and ':' in line:  # if there is a given id (there is something between '?' and ':' / end of str and there even is ':')
		qid = line.split(':')[0][
			  1:].strip()  # everything until the first ':', cut off the first char (?), then strip (remove trailing/leading whitespaces)
	else:  # an id needs to be generated
		qid = re.sub('[^a-zA-Z\d-]', '-',
					 title).lower()  # replace anything except alphanumeric chars and '-' to - and turn it lowercase
		while '--' in qid:  # while there are double hyphens
			qid.replace('--', '-')  # remove them (turn into 1)
		# this way, even 3 hyphens get turned into 2 and then into 1
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


def q_options(line: str):
	options_re = re.findall('''([a-z]+)(=)([^,]+|'[^']*'|"[^"]*")''', line)  # finds all label=value
	options = {}
	for i in options_re:
		options.update({str(i[0].strip('"\'')): str(i[2].strip('"\''))})  # update the dict with the new option, which will get quotes removed and turned into a string
	return options


# --- BLOCK SPECIFIC --- #

def checkbox_answer(line: str, qid: str, count: int):
	if ':' in line:  # an id was set
		aid = line.split(']')[1].split(':')[0].strip()  # between ']' and ':', striped
		line = line.split(']')[0] + ']' + "".join(line.split(':')[1:])  # remove id from line
	else:
		aid = count  # the nth option
	if line.startswith(('[]', '[ ]')):  # empty checkbox
		label = re.sub('\[ *]', '', line).strip()  # remove checkbox symbol (with(-out) space(s) in between), striped
		return f'<div id="{qid}_{aid}" class="answer checkbox"><input type="checkbox" name="{qid}_{aid}" id="{qid}_{aid}_checkbox"></input><label for="{qid}_{aid}_checkbox" id="{qid}_{aid}_label">{label}</label></div>'
	elif line.lower().startswith('[x]'):
		label = line.replace('[x]', '').strip()  # remove checkbox symbol, striped
		return f'<div id="{qid}_{aid}" class="answer checkbox"><input type="checkbox" name="{qid}_{aid}" id="{qid}_{aid}_checkbox" checked></input><label for="{qid}_{aid}_checkbox" id="{qid}_{aid}_label">{label}</label></div>'
	else:  # fake paragraph
		label = line.strip()
		return f'<div id="{qid}_{aid}" class="answer text"><input type="checkbox" name="{qid}_{aid}" id="{qid}_{aid}_checkbox" style="visibility:hidden;"></input><label id="{qid}_{aid}_label">{label}</label></div>'


def multiple_choice_answer(line: str, qid: str, count: int):
	if ':' in line:  # an id was set
		aid = line.split(')')[1].split(':')[0].strip()  # between ')' and ':', striped
		line = line.split(')')[0] + ')' + "".join(line.split(':')[1:])  # remove id from line
	else:
		aid = count  # the nth option
	if line.startswith(('()', '( )')):  # unchecked radio select
		label = re.sub('\( *\)', '', line).strip()  # remove radio symbol (with(-out) space(s) in between), striped
		return f'<div id="{qid}_{aid}" class="answer multiple-choice"><input type="radio" name="{qid}_radio" id="{qid}_{aid}_radio" value="{qid}_{aid}"><label for="{qid}_{aid}_radio" id="{qid}_{aid}_label">{label}</label></div>'
	elif line.lower().startswith('(x)'):
		label = line.replace('(x)', '').strip()  # remove radio symbol
		return f'<div id="{qid}_{aid}" class="answer multiple-choice"><input type="radio" name="{qid}_radio" id="{qid}_{aid}_radio" value="{qid}_{aid}" checked><label for="{qid}_{aid}_radio" id="{qid}_{aid}_label">{label}</label></div>'
	else:
		label = line.strip()
		return f'<div id="{qid}_{aid}" class="answer text"><input type="radio" name="{qid}_{aid}" id="{qid}_{aid}_radio" style="visibility:hidden;"></input><label id="{qid}_{aid}_label">{label}</label></div>'


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
		elif descr_started: # only if the construction of the description has started already and the line doesn't start with > (because of 'el'if)
			descr = q_description(descr)  # the description is done, so it will be generated
			descr_started = False
		if lines[i].startswith(('\t[', '\t\t')):  # checkbox or paragraph
			answer_html += checkbox_answer(lines[i].strip(), qid, aid)  # add checkbox line to the options
			aid += 1
		i += 1  # go to next line
	return f'<div id="{qid}" class="question checkbox"><h3 id="{qid}_title" class="question checkbox title">{title}</h3><div id="{qid}_description" class="question checkbox description">{descr}</div>{answer_html}</div>'


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
	return f'<div id="{qid}" class="question multiple-choice"><h3 id="{qid}_title" class="question multiple-choice title">{title}</h3><div id="{qid}_description" class="question multiple-choice description">{descr}</div>{answer_html}</div>'


def text(block: str):
	lines = block.split('\n')  # create array of lines
	qid, title = q_head(lines[0])  # generate the qid (question id) and title
	i = 1  # line counter
	descr = ''  # init
	descr_started = False  # init
	options = {}  # init
	while i < len(lines):  # alternate syntax to "for line in lines" to dynamically change the current line number
		if lines[i].startswith('\t>'):  # description lines
			descr += '\n' + lines[i]  # add the current line to the description tag
			descr_started = True
			# go to the next line:
			i += 1
			continue
		if not lines[i].startswith('\t>'):  # must be an option line
			options.update(q_options(lines[i]))
		i += 1
	descr = q_description(descr)  # the description is done, so it will be generated # generate description
	if options['type']:
		inp_type = options['type']
	else:
		inp_type = 'text'
	return f'<div id="{qid}" class="question text {inp_type}"><h3 id="{qid}_title" class="question text {inp_type} title">{title}</h3><div id="{qid}_description" class="question text {inp_type} description">{descr}</div><input type="{inp_type}" id="{qid}_input" name="{qid}" class="answer text {inp_type}" placeholder="{options["placeholder"]}"></input></div>'
