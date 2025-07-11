import filter  # local file for compiling the document
import argparse  # get command line arguments
import os  # join file path
import markdown  # markdown to html conversion

# --- OPEN INPUT --- #

parser = argparse.ArgumentParser(description = 'core conversion of formsMD files', epilog = 'For more help you can reach out to 0yqc@duck.com')  # set-up for automatic help, etc.
parser.add_argument('-i', '--inp', '--input', dest = 'input', help = 'path of the input file.')
parser.add_argument('-o', '--out', '--output', dest = 'output', help = 'directory where the output HTML files should be saved.')
parser.add_argument('-a', '--assets', dest = 'assets', help = 'directory which contains script.js and styles.css.')
args = parser.parse_args()  # get arguments
inp_path = args.input
out_path = args.output
assets_path = args.assets

converted, options = filter.file(inp_path)  # start the compiling (./filter.py)
print(options)

try:
	method = options['submit_method']
except KeyError:
	method = 'mail'
try:
	mail = options['mail_address']
except KeyError:
	mail = ''
try:
	action_url = options['url']
except KeyError:
	action_url = ''
try:
	redirect = options['redirect']
except KeyError:
	redirect = ''
try:
	subject = options['subject']
except KeyError:
	subject = 'fMD Form Submission'

if method == 'formsubmit':  # generate formsubmit link
	action_url = 'https://formsubmit.co/' + mail

html = markdown.markdown(converted, extensions = ['md_in_html'])

if method == 'formsubmit':
	html = f'''
	<!doctype html>
	<html>
		<head>
			<title>fMD Form</title>
			<link rel="stylesheet" href="./styles.css">
		</head>
		<body>
			<form id="page1_form" action="{action_url}" method="POST">
				{html}
				<input type="hidden" name="_next" value="{redirect}">
				<input type="hidden" name="_subject" value="{subject}">
				<div id="page1_submit">
					<input type="submit" value="Submit Form">
				</div>
			</form>
			<script src="./script.js"></script>
		</body>
	</html>
	'''.strip()  # remove leading/trailing \n
else:
	html = f'''
	<!doctype html>
	<html>
		<head>
			<title>fMD Form</title>
			<link rel="stylesheet" href="./styles.css">
		</head>
		<body>
			<form id="page1_form" action="{action_url}">
				{html}
				<div id="page1_submit">
					<input type="submit" value="Submit Form">
				</div>
			</form>
			<script src="./script.js"></script>
		</body>
	</html>
	'''.strip()  # remove leading/trailing \n

if method == 'mail':  # javascript for opening mailto links
	with open(os.path.join(assets_path, 'script.js'), 'r') as js:
		txt = js.read()
		txt = txt.replace('{__url__}', redirect)  # replace the redirect link at form submission
		txt = txt.replace('{__subject__}', subject)  # replaces the email subject with the user-defined
		with open(os.path.join(out_path, 'script.js'), 'w') as f:
			f.write(txt)

with open(os.path.join(assets_path, 'styles.css'), 'r') as css:
	txt = css.read()
	with open(os.path.join(out_path, 'styles.css'), 'w') as f:
		f.write(txt)

with open(os.path.join(out_path, 'page1.html'), 'w') as f:
	f.write(html)
