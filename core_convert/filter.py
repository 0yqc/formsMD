import compiler # local file to compile single blocks

def file(file):
	'''
	file is the path to the file

	this function compiles .fmd files into HTML files and returns a string for further use.
	'''
	# clone all lines into a list
	with open(file, 'r') as file:
		lines = file.readlines()
	for n, i in enumerate(lines): # n is a counter (0,1,2,...), i is the current line
		if i.startswith('//'): # comment line
			lines[n] = '' # clear the current line (comments won't be rendered)
			continue
		if i.startswith('?'): # a block starts
			block_construction = True # indicator that the block is being constructed
			block_str = i # add the first line of the block to the block string
			lines[n] = '' # clear the current line
		elif i.startswith('\t') and block_construction == True: # a block continues (only applicable if it's in construction)
			block_str = block_str + i # append new lines to the block
			lines[n] = '' # clear the current line
		else: # if it's normal markdown no further processing should be done
			continue
		try: # lines[n+1] would fail if it's the last line
			if not lines[n+1].startswith('\t'): # if the block does not continue
				block_construction = False # stop the construction
				lines[n] = block(block_str) # compile the block and write it all into the last line
		except: # it's the last line, so it must be compiled one last time
			block_construction = False # stop the construction
			lines[n] = block(block_str) # compile the block
	return(''.join(lines)) # return everything at the end, joined together

def block(text: str): # block compiling logic
	if '\n\t[]' in text or '\n\t[ ]' in text or '\n\t[x]' in text.lower(): # checkbox question
		text = compiler.checkbox(text)
	return text