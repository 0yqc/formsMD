import re as regex

# --- VARS --- #

used_qid = []

# --- ALL BLOCKS --- #

def q_head(line: str): #
	title = ':'.join(line.split(':')[1:]).strip() # everything from the first ':', stripped, so sapces won't matter
	if line.split(':')[0][1:].strip() and ':' in line: # if there is a given id (there is something between '?' and ':' / end of str and there even is ':')
		id = line.split(':')[0][1:].strip() # everything until the first ':', cut off the first char (?), then strip (remove trailing/leading whitespaces)
	else: # an id needs to be generated
		id = regex.sub('[^a-zA-Z\d-]','-',title).lower() # replace anything except alphanumeric chars and '-' to - and turn it lowercase
		while '--' in id: # while there are double hyphens
			id.replace('--','-') # remove them (turn into 1)
			# this way, even 3 hyphens get turned into 2 and then into 1
		id.strip('-') # remove starting / trailing hyphens
		# system to only use each qid once: (append numbers otherwise)
		i = 0
		if id in used_qid:
			while id in used_qid:
				i += 1
				if not (id + '-' + i) in used_qid:
					break
			used_qid.append(id + '-' + i)
			id = id + '-' + i
		else:
			used_qid.append(id)
	return id, title

def q_description(text: str):
	text = text.replace('\n\t>','\n') # remove quotes
	text = regex.sub('\n *','\n',text) # remove leading whitespaces
	text = '<p>' + text + '</p>'
	text = text.replace('\n\n','</p><p>') # insert new paragraph on double newline
	return text

# --- BLOCK SPECIFIC --- #

def checkbox_answer(line: str, qid: str, count: int):
	if ':' in line: # an id was set
		aid = line.split(']')[1].split(':')[0].strip() # between ']' and ':', striped
		line = line.split(']')[0] + ']' + "".join(line.split(':')[1:]) # remove id from line
	else:
		aid = count # the nth option
	if line.startswith(('[]','[ ]')): # empty checkbox
		label = regex.sub('\[ *\]','',line).strip() # remove checkbox symbol (with(-out) space(s) inbetween), striped
		return f'<div id="{qid}_{aid}" class="answer checkbox"><input type="checkbox" name="{qid}_{aid}" id="{qid}_{aid}_checkbox"></input><label for="{qid}_{aid}_checkbox" id="{qid}_{aid}_label">{label}</label></div>'
	elif line.startswith('[x]'):
		label = line.replace('[x]','').strip() # remove checkbox symbol, striped
		return f'<div id="{qid}_{aid}" class="answer checkbox"><input type="checkbox" name="{qid}_{aid}" id="{qid}_{aid}_checkbox" checked></input><label for="{qid}_{aid}_checkbox" id="{qid}_{aid}_label">{label}</label></div>'
	else: # fake paragraph
		label = line.strip()
		return f'<div id="{qid}_{aid}" class="answer text"><input type="checkbox" name="{qid}_{aid}" id="{qid}_{aid}_checkbox" style="visibility:hidden;"></input><label id="{qid}_{aid}_label">{label}</label></div>'


# --- BLOCKS --- #

def checkbox(text: str):
	lines = text.split('\n') # create array of lines
	qid, title = q_head(lines[0]) # generate the qid (question id) and title
	i = 0 # line counter
	descr = '' # init
	aid = 0 # init
	answer_html = '' # init
	description_started = False # init
	while i < len(lines): # alternate syntax to "for line in lines" to dynamically change the current line number
		if lines[i].startswith('\t>'): # description lines
			descr += '\n' + lines[i] # add the current line to the description tag
			description_started = True
			# go to the next line:
			i += 1
			continue
		elif description_started == True: # only if the construction of the description has started already
			descr = q_description(descr) # the description is done, so it will be generated
		if lines[i].startswith(('\t[','\t\t')): # checkbox or paragraph
			answer_html += checkbox_answer(lines[i].strip(),qid,aid) # add checkbox line to the options
			aid += 1
		i += 1 # go to next line
	return f'<div id="{qid}" class="question checkbox"><h3 id="{qid}_title" class="question checkbox title">{title}</h3><div id="{qid}_description" class="question checkbox description">{descr}</div>{answer_html}</div>'