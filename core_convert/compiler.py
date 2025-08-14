import re  # regex
import markdown as md  # markdown processing, sudo apt install python-markdown-doc

# --- VARS --- #

used_qid = []
used_aid = []


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
	title = md.markdown(title).removeprefix('<p>').removesuffix('</p>')
	return qid, title


def q_description(descr: str):
	descr = descr.replace('\n>', '\n')  # remove quotes
	descr = re.sub('\n *', '\n', descr)  # remove leading whitespaces
	descr = '<p>' + descr + '</p>'
	descr = descr.replace('\n\n', '</p><p>')  # insert new paragraph on double newline
	descr = md.markdown(descr).removeprefix('<p>').removesuffix('</p>')
	return descr


def options_compile(line: str):
	options_re = re.findall('''([^,\n]+)(=)('[^']*'|"[^"]*"|[^,]+)''', line)  # finds all label=value
	options = {}
	for i in options_re:
		options.update({str(i[0].strip('\'"')):str(i[2].strip('\'"'))})  # update the dict with the new option, which will get quotes removed and turned into a string
	return options


# --- BLOCK SPECIFIC --- #

def checkbox_answer(line: str, qid: str):
	if ':' in line:  # an id was set
		aid = line.split(']')[1].split(':')[0].strip()  # between ']' and ':', striped
		line = line.split(']')[0] + ']' + ':'.join(line.split(':')[1:])  # remove id from line
	else:  # generate aid
		label = re.sub('\[.*?] *', '', line)
		aid = re.sub('[^a-zA-Z\d-]', '-', label).lower()  # replace anything except alphanumeric chars and '-' to - and turn it lowercase
		aid = re.sub('-+', '-', aid)  # replace any amount of consecutive hyphens with one
		aid = aid.strip('-')  # remove starting / trailing hyphens
		# system to only use each qid once: (append numbers otherwise)
		i = 0
		if aid in used_aid:
			while aid in used_aid:
				i += 1
				if not (aid + '-' + i) in used_qid:
					break
			used_aid.append(qid + '-' + i)
			aid = aid + '-' + i
		else:
			used_aid.append(qid)
	if aid == 'other':
		if line.startswith(('[]', '[ ]')):
			label = re.sub('\[ *]', '', line).strip()  # remove checkbox symbol (with(-out) space(s) in between), striped
			label = md.markdown(label).removeprefix('<p>').removesuffix('</p>')
			return f'<div id="{qid}_{aid}" class="answer checkbox other"><input type="checkbox" name="{qid}_checkbox" id="{qid}_{aid}_checkbox" ><label for="{qid}_{aid}_checkbox" id="{qid}_{aid}_label">{label}</label><input type="text" class="answer checkbox text other" id="{qid}_{aid}_text" name="{qid}_{aid}_text" aria-label="Text for {label}" placeholder="Enter your answer"></div>'
		elif line.lower().startswith('[x]'):
			label = line.replace('[x]', '').strip()  # get label text
			label = md.markdown(label).removeprefix('<p>').removesuffix('</p>')
			return f'<div id="{qid}_{aid}" class="answer checkbox other"><input type="checkbox" name="{qid}_checkbox" id="{qid}_{aid}_checkbox" checked><label for="{qid}_{aid}_checkbox" id="{qid}_{aid}_label">{label}</label><input type="text" class="answer checkbox text other" id="{qid}_{aid}_text" name="{qid}_{aid}_text" aria-label="Text for {label}" placeholder="Enter your answer"></div>'
	elif line.startswith(('[]', '[ ]')):  # empty checkbox
		label = re.sub('\[ *]', '', line).strip()  # remove checkbox symbol (with(-out) space(s) in between), striped
		label = md.markdown(label).removeprefix('<p>').removesuffix('</p>')
		return f'<div id="{qid}_{aid}" class="answer checkbox"><input type="checkbox" name="{qid}_{aid}" id="{qid}_{aid}_checkbox"><label for="{qid}_{aid}_checkbox" id="{qid}_{aid}_label">{label}</label></div>'
	elif line.lower().startswith('[x]'):
		label = line.replace('[x]', '').strip()  # remove checkbox symbol, striped
		label = md.markdown(label).removeprefix('<p>').removesuffix('</p>')
		return f'<div id="{qid}_{aid}" class="answer checkbox"><input type="checkbox" name="{qid}_{aid}" id="{qid}_{aid}_checkbox" checked><label for="{qid}_{aid}_checkbox" id="{qid}_{aid}_label">{label}</label></div>'
	else:  # fake paragraph
		label = line.strip()
		label = md.markdown(label).removeprefix('<p>').removesuffix('</p>')
		return f'<div id="{qid}_{aid}" class="answer text"><input type="checkbox" name="{qid}_{aid}" id="{qid}_{aid}_checkbox" style="visibility:hidden;"><label id="{qid}_{aid}_label">{label}</label></div>'


def multiple_choice_answer(line: str, qid: str):
	if ':' in line:  # an id was set
		aid = line.split(')')[1].split(':')[0].strip()  # between ')' and ':', striped
		line = line.split(')')[0] + ')' + ':'.join(line.split(':')[1:])  # remove id from line
	else:
		label = re.sub('\(.*?\) *', '', line)
		aid = re.sub('[^a-zA-Z\d-]', '-', label).lower()  # replace anything except alphanumeric chars and '-' to - and turn it lowercase
		aid = re.sub('-+', '-', aid)  # replace any amount of consecutive hyphens with one
		aid = aid.strip('-')  # remove starting / trailing hyphens
		# system to only use each qid once: (append numbers otherwise)
		i = 0
		if aid in used_aid:
			while aid in used_aid:
				i += 1
				if not (aid + '-' + i) in used_qid:
					break
			used_aid.append(qid + '-' + i)
			aid = aid + '-' + i
		else:
			used_aid.append(qid)
	if aid == 'other':
		if line.startswith(('()', '( )')):
			label = re.sub('\( *\)', '', line).strip()  # remove radio symbol (with(-out) space(s) in between), striped
			label = md.markdown(label).removeprefix('<p>').removesuffix('</p>')
			return f'<div id="{qid}_{aid}" class="answer multiple-choice other"><input type="radio" name="{qid}_radio" id="{qid}_{aid}_radio" value="{aid}"><label for="{qid}_{aid}_radio" id="{qid}_{aid}_label">{label}</label><input type="text" class="answer multiple-choice text other" id="{qid}_{aid}_other" name="{qid}_{aid}_other" aria-label="Text for {label}" placeholder="Enter your answer"></div>'
		elif line.lower().startswith('(x)'):
			label = line.replace('(x)', '').strip()  # get label text
			label = md.markdown(label).removeprefix('<p>').removesuffix('</p>')
			return f'<div id="{qid}_{aid}" class="answer multiple-choice other"><input type="radio" name="{qid}_radio" id="{qid}_{aid}_radio" value="{aid}" checked><label for="{qid}_{aid}_radio" id="{qid}_{aid}_label">{label}</label><input type="text" class="answer multiple-choice text other" id="{qid}_{aid}_other" name="{qid}_{aid}_other" aria-label="Text for {label}" placeholder="Enter your answer"></div>'
	elif line.startswith(('()', '( )')):  # unchecked radio select
		label = re.sub('\( *\)', '', line).strip()  # remove radio symbol (with(-out) space(s) in between), striped
		label = md.markdown(label).removeprefix('<p>').removesuffix('</p>')
		return f'<div id="{qid}_{aid}" class="answer multiple-choice"><input type="radio" name="{qid}_radio" id="{qid}_{aid}_radio" value="{aid}"><label for="{qid}_{aid}_radio" id="{qid}_{aid}_label">{label}</label></div>'
	elif line.lower().startswith('(x)'):
		label = line.replace('(x)', '').strip()  # remove radio symbol
		label = md.markdown(label).removeprefix('<p>').removesuffix('</p>')
		return f'<div id="{qid}_{aid}" class="answer multiple-choice"><input type="radio" name="{qid}_radio" id="{qid}_{aid}_radio" value="{aid}" checked><label for="{qid}_{aid}_radio" id="{qid}_{aid}_label">{label}</label></div>'
	else:
		label = line.strip()
		label = md.markdown(label).removeprefix('<p>').removesuffix('</p>')
		return f'<div id="{qid}_{aid}" class="answer multiple-choice"><input type="radio" name="{qid}_{aid}" id="{qid}_{aid}_radio" style="visibility:hidden;"><label id="{qid}_{aid}_label">{label}</label></div>'


def matrix_answer(label: str, qid: str, min: int, max: int):
	if ':' in label:  # an id was set
		aid = label.split(':')[0].strip()
		label = label.split(':')[1].strip()
	else:
		aid = re.sub('[^a-zA-Z\d-]', '-', label).lower()  # replace anything except alphanumeric chars and '-' to - and turn it lowercase
		aid = re.sub('-+', '-', aid)  # replace any amount of consecutive hyphens with one
		aid = aid.strip('-')  # remove starting / trailing hyphens
		# system to only use each qid once: (append numbers otherwise)
		i = 0
		if aid in used_aid:
			while aid in used_aid:
				i += 1
				if not (aid + '-' + i) in used_qid:
					break
			used_aid.append(qid + '-' + i)
			aid = aid + '-' + i
		else:
			used_aid.append(qid)
	answer_html = f'<tr id="{qid}_{aid}" class="answer matrix"><td id="{qid}_{aid}_label">{label}</td>'
	for i in range(max-min+1): # both are inclusive
		n = min + i
		answer_html += f'<td><input type="radio" name="{qid}_{aid}_radio" value="{n}" id="{qid}_{aid}_radio_{n}" aria-label="{n}"></input></td>'
	answer_html += f'</tr>'
	return answer_html


def dropdown_option(line: str, qid: str):
	if ':' in line:  # an id was set
		aid = line.split(')')[1].split(':')[0].strip()  # between ')' and ':', striped
		line = line.split(')')[0] + ')' + ':'.join(line.split(':')[1:])  # remove id from line
	else:
		label = re.sub('\(.*?\) *', '', line)
		aid = re.sub('[^a-zA-Z\d-]', '-', label).lower()  # replace anything except alphanumeric chars and '-' to - and turn it lowercase
		aid = re.sub('-+', '-', aid)  # replace any amount of consecutive hyphens with one
		aid = aid.strip('-')  # remove starting / trailing hyphens
		# system to only use each qid once: (append numbers otherwise)
		i = 0
		if aid in used_aid:
			while aid in used_aid:
				i += 1
				if not (aid + '-' + i) in used_qid:
					break
			used_aid.append(qid + '-' + i)
			aid = aid + '-' + i
		else:
			used_aid.append(qid)
	if line.startswith(('||', '| |')):  # normal select item
		label = re.sub('\| *\|', '', line).strip()  # get label text
		label = md.markdown(label).removeprefix('<p>').removesuffix('</p>')
		return f'<option value="{aid}" id="{qid}_{aid}">{label}</option>'
	elif line.lower().startswith('|x|'):
		label = line.replace('|x|', '').strip()  # get label text
		label = md.markdown(label).removeprefix('<p>').removesuffix('</p>')
		return f'<option value="{aid}" id="{qid}_{aid}" selected>{label}</option>'
	else:  # optgroup
		label = line.strip()
		label = md.markdown(label).removeprefix('<p>').removesuffix('</p>')
		return f'<optgroup label="{label}" id="{qid}_{aid}">'


# --- BLOCKS --- #

def checkbox(block: str):
	used_aid = []
	lines = block.split('\n')  # create array of lines
	qid, title = q_head(lines[0])  # generate the qid (question id) and title
	i = 1  # line counter, first line already done
	descr = ''  # init
	answer_html = ''  # init
	descr_started = False  # init
	while i < len(lines):  # alternate syntax to "for line in lines" to dynamically change the current line number
		if lines[i].startswith('>'):  # description lines
			descr += '\n' + lines[i]  # add the current line to the description tag
			descr_started = True
			# go to the next line:
			i += 1
			continue
		elif descr_started:  # only if the construction of the description has started already and the line doesn't start with > (because of 'el'if)
			descr = q_description(descr)  # the description is done, so it will be generated
			descr_started = False
		if lines[i].startswith(('[', '')):  # checkbox or paragraph
			answer_html += checkbox_answer(lines[i].strip(), qid)  # add checkbox line to the options
		i += 1  # go to next line
	return f'<div id="{qid}" class="question checkbox"><h3 id="{qid}_title" class="question checkbox title">{title}</h3><div id="{qid}_description" class="question checkbox description">{descr}</div>{answer_html}</div>'


def multiple_choice(block: str):
	used_aid = []
	lines = block.split('\n')  # create array of lines
	qid, title = q_head(lines[0])  # generate the qid (question id) and title
	i = 1  # line counter
	descr = ''  # init
	answer_html = ''  # init
	descr_started = False  # init
	while i < len(lines):  # alternate syntax to "for line in lines" to dynamically change the current line number
		if lines[i].startswith('>'):  # description lines
			descr += '\n' + lines[i]  # add the current line to the description tag
			descr_started = True
			# go to the next line:
			i += 1
			continue
		elif descr_started:  # only if the construction of the description has started already and the line doesn't start with > (because of 'el'if)
			descr = q_description(descr)  # the description is done, so it will be generated
			descr_started = False
		if lines[i].startswith(('(', '')):  # checkbox or paragraph
			answer_html += multiple_choice_answer(lines[i].strip(), qid)  # add checkbox line to the options
		i += 1  # go to next line
	return f'<div id="{qid}" class="question multiple-choice"><h3 id="{qid}_title" class="question multiple-choice title">{title}</h3><div id="{qid}_description" class="question multiple-choice description">{descr}</div>{answer_html}</div>'


def matrix(block: str):
	used_aid = []
	lines = block.split('\n')  # create array of lines
	qid, title = q_head(lines[0])  # generate the qid (question id) and title
	i = 1  # line counter
	descr = ''  # init
	options = {}  # init
	min, max = 1, 5  # default values
	answer_html = ''  # init
	descr_started = False  # init
	while i < len(lines):  # alternate syntax to "for line in lines" to dynamically change the current line number
		if lines[i].startswith('>'):  # description lines
			descr += '\n' + lines[i]  # add the current line to the description tag
			descr_started = True
			# go to the next line:
			i += 1
			continue
		elif descr_started:  # only if the construction of the description has started already and the line doesn't start with > (because of 'el'if)
			descr = q_description(descr)  # the description is done, so it will be generated
			descr_started = False
		if lines[i].startswith('*'):
			answer_html += matrix_answer(lines[i].removeprefix('*').strip(), qid, min, max)
		elif lines[i].startswith('{'):  # must be an option line
			options.update(options_compile(lines[i].strip('{}')))
			try:
				min = int(options['min'])
			except (KeyError, ValueError):
				pass
			try:
				max = int(options['max'])
			except (KeyError, ValueError):
				pass
		i += 1
	html = f'<div id="{qid}" class="question matrix"><h3 id="{qid}_title" class="question matrix title">{title}</h3><div id="{qid}_description" class="question matrix description">{descr}</div><table><thead><tr><td></td>'
	for i in range(max-min+1): # both inclusive
		n = min + i
		html += f'<td>{n}</td>'
	html += f'</tr></thead><tbody>{answer_html}</tbody></table></div>'
	return html



def dropdown(block: str):
	lines = block.split('\n')  # create array of lines
	qid, title = q_head(lines[0])  # generate the qid (question id) and title
	i = 1  # line counter
	descr = ''  # init
	answer_html = ''  # init
	descr_started = False  # init
	while i < len(lines):  # alternate syntax to "for line in lines" to dynamically change the current line number
		if lines[i].startswith('>'):  # description lines
			descr += '\n' + lines[i]  # add the current line to the description tag
			descr_started = True
			# go to the next line:
			i += 1
			continue
		elif descr_started:  # only if the construction of the description has started already and the line doesn't start with > (because of 'el'if)
			descr = q_description(descr)  # the description is done, so it will be generated
			descr_started = False
		if lines[i].startswith(('|', '')):  # checkbox or paragraph
			answer_html += dropdown_option(lines[i].strip(), qid)  # add checkbox line to the options
		i += 1  # go to next line
	return f'<div id="{qid}" class="question dropdown"><label for="{qid}_input" id="{qid}_label"><h3 id="{qid}_title" class="question dropdown title">{title}</h3></label><div id="{qid}_description" class="question dropdown description">{descr}</div><select id="{qid}_input" class="question dropdown input">{answer_html}</select></div>'


def text(block: str):
	lines = block.split('\n')  # create array of lines
	qid, title = q_head(lines[0])  # generate the qid (question id) and title
	i = 1  # line counter
	descr = ''  # init
	options = {}  # init
	datalist_html = f'<datalist id="{qid}_datalist" class="question text datalist">'
	datalist = False
	while i < len(lines):  # alternate syntax to "for line in lines" to dynamically change the current line number
		if lines[i].startswith('>'):  # description lines
			descr += '\n' + lines[i]  # add the current line to the description tag
			# go to the next line:
			i += 1
			continue
		elif lines[i].startswith('-'):
			datalist = True
			datalist_html = datalist_html + '<option value="' + re.sub('- *', '', lines[i]) + '">'
		elif lines[i].startswith('{'):  # must be an option line
			options.update(options_compile(lines[i].strip('{}')))
		i += 1
	datalist_html = datalist_html + '</datalist>'
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
	if datalist:
		return f'<div id="{qid}" class="question text {inp_type}"><label for="{qid}_input" id="{qid}_label"><h3 id="{qid}_title" class="question text {inp_type} title">{title}</h3></label><div id="{qid}_description" class="question text {inp_type} description">{descr}</div><input type="{inp_type}" id="{qid}_input" name="{qid}" class="answer text {inp_type}" placeholder="{placeholder}" value="{value}" list="{qid}_datalist">{datalist_html}</div>'
	else:
		return f'<div id="{qid}" class="question text {inp_type}"><label for="{qid}_input" id="{qid}_label"><h3 id="{qid}_title" class="question text {inp_type} title">{title}</h3></label><div id="{qid}_description" class="question text {inp_type} description">{descr}</div><input type="{inp_type}" id="{qid}_input" name="{qid}" class="answer text {inp_type}" placeholder="{placeholder}" value="{value}"></div>'


def area(block: str):
	lines = block.split('\n')  # create array of lines
	qid, title = q_head(lines[0])  # generate the qid (question id) and title
	i = 1  # line counter
	descr = ''  # init
	options = {}
	while i < len(lines):  # alternate syntax to "for line in lines" to dynamically change the current line number
		if lines[i].startswith('>'):  # description lines
			descr += '\n' + lines[i]  # add the current line to the description tag
			# go to the next line:
			i += 1
			continue
		if lines[i].startswith('{'):  # must be an option line
			options.update(options_compile(lines[i].strip('{}')))
		i += 1
	descr = q_description(descr)  # the description is done, so it will be generated
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
	return f'<div id="{qid}" class="question text area textarea"><label for="{qid}_input" id="{qid}_label"><h3 id="{qid}_title" class="question text area title">{title}</h3></label><div id="{qid}_description" class="question text area description">{descr}</div><textarea id="{qid}_input" name="{qid}" rows="{rows}" placeholder="{placeholder}">{value}</textarea></div>'


def g_options(block: str):
	option_lines = block.split('\n')[1:]  # line 1ff
	options = {}
	for i in option_lines:
		options.update(options_compile(i))
	return options
