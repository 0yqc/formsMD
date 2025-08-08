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
			lines[i], new_options = block(block_str.strip())
			lines[i] = '\n\n' + lines[i] + '\n\n'
			options.update(new_options)
		else:
			lines[i] = lines[i].strip()
	return '\n'.join(lines), options


def block(text: str):  # block compiling logic
	options = {}  # init
	if re.findall('\n\t*\[.?\]', text):  # checkbox question
		text = compiler.checkbox(text)
	elif re.findall('\n\t*\(.?\)', text):  # multiple choice question
		text = compiler.multiple_choice(text)
	elif re.findall('\n\t*\|', text):
		text = compiler.dropdown(text)
	elif 'type=area' in text:
		text = compiler.area(text)
	elif 'type=' in text:
		text = compiler.text(text)
	elif 'options' in text:
		options = compiler.g_options(text)
		text = ''
	return text, options
