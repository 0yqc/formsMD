import re as regex

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
		qid = regex.sub('[^a-zA-Z\d-]', '-',
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


def q_description(text: str):
	text = text.replace('\n\t>', '\n')  # remove quotes
	text = regex.sub('\n *', '\n', text)  # remove leading whitespaces
	text = '<p>' + text + '</p>'
	text = text.replace('\n\n', '</p><p>')  # insert new paragraph on double newline
	return text


# --- BLOCK SPECIFIC --- #

def checkbox_answer(line: str, qid: str, count: int):
	if ':' in line:  # an id was set
		aid = line.split(']')[1].split(':')[0].strip()  # between ']' and ':', striped
		line = line.split(']')[0] + ']' + "".join(line.split(':')[1:])  # remove id from line
	else:
		aid = count  # the nth option
	if line.startswith(('[]', '[ ]')):  # empty checkbox
		label = regex.sub('\[ *]', '', line).strip()  # remove checkbox symbol (with(-out) space(s) in between), striped
		return f'<div id="{qid}_{aid}" class="answer checkbox"><input type="checkbox" name="{qid}_{aid}" id="{qid}_{aid}_checkbox"></input><label for="{qid}_{aid}_checkbox" id="{qid}_{aid}_label">{label}</label></div>'
	elif line.startswith('[x]'):
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
	if line.startswith(('()','( )')): # unchecked radio select
		label = regex.sub('\( *\)', '', line).strip()  # remove radio symbol (with(-out) space(s) in between), striped
		print(label)
		return f'<div id="{qid}_{aid}" class="answer multiple-choice"><input type="radio" name="{qid}_radio" id="{qid}_{aid}_radio" value="{qid}_{aid}"><label for="{qid}_{aid}_radio" id="{qid}_{aid}_label">{label}</label></div>'
	elif line.startswith('(x)'):
		label = line.replace('(x)', '').strip() # remove radio symbol
		return f'<div id="{qid}_{aid}" class="answer multiple-choice"><input type="radio" name="{qid}_radio" id="{qid}_{aid}_radio" value="{qid}_{aid}" checked><label for="{qid}_{aid}_radio" id="{qid}_{aid}_label">{label}</label></div>'
	else:
		label = line.strip()
		return f'<div id="{qid}_{aid}" class="answer text"><input type="radio" name="{qid}_{aid}" id="{qid}_{aid}_radio" style="visibility:hidden;"></input><label id="{qid}_{aid}_label">{label}</label></div>'

# --- BLOCKS --- #

def checkbox(block: str):
	lines = block.split('\n')  # create array of lines
	qid, title = q_head(lines[0])  # generate the qid (question id) and title
	i = 0  # line counter
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
		if lines[i].startswith(('\t[', '\t\t')):  # checkbox or paragraph
			answer_html += checkbox_answer(lines[i].strip(), qid, aid)  # add checkbox line to the options
			aid += 1
		i += 1  # go to next line
	return f'<div id="{qid}" class="question checkbox"><h3 id="{qid}_title" class="question checkbox title">{title}</h3><div id="{qid}_description" class="question checkbox description">{descr}</div>{answer_html}</div>'


def multiple_choice(block: str):
	lines = block.split('\n')  # create array of lines
	qid, title = q_head(lines[0])  # generate the qid (question id) and title
	i = 0  # line counter
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
		if lines[i].startswith(('\t(', '\t\t')):  # checkbox or paragraph
			answer_html += multiple_choice_answer(lines[i].strip(), qid, aid)  # add checkbox line to the options
			aid += 1
		i += 1  # go to next line
	return f'<div id="{qid}" class="question multiple-choice"><h3 id"{qid}_title" class="question multiple-choice title">{title}</h3><div id="{qid}_description" class="question multiple-choice description">{descr}</div>{answer_html}</div>'