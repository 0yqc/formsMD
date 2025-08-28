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
		text = compiler.checkbox(text, options)
	elif re.findall('\n\(.?\)', text):  # multiple choice question
		text = compiler.radio(text, options)
	elif '\n|' in text:
		text = compiler.dropdown(text, options)
	elif 'type=matrix_' in text:
		text = compiler.matrix(text, options)
	elif 'type=area' in text:
		text = compiler.area(text, options)
	elif 'type=' in text:
		text = compiler.input_other(text, options)
	elif 'options' in text:
		new_options = compiler.global_options(text)
		text = ''
	return text, new_options