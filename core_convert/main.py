import filter  # local file for compiling the document
import argparse  # get command line arguments
import os  # join file path
import markdown  # markdown to html conversion

# --- OPEN INPUT --- #

parser = argparse.ArgumentParser(description='core conversion of formsMD files', epilog='For more help you can reach out to 0yqc@duck.com')  # set-up for automatic help, etc.
parser.add_argument('-i', '--inp', '--input', dest='input', help='path of the input file.')
parser.add_argument('-o', '--out', '--output', dest='output', help='directory where the output HTML files should be saved.')
parser.add_argument('-a', '--assets', dest='assets', help='directory which contains JS scripts and stylesheets.')
args = parser.parse_args()  # get arguments
inp_path = args.input
out_path = args.output
assets_path = args.assets

converted, options = filter.file(inp_path)  # start the compiling (./filter.py)

try:
	lang = options['lang']
except KeyError:
	lang = 'en'
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
	redirect = 'window.location.href'
try:
	title = options['title']
except KeyError:
	title = 'fMD Form'
try:
	subject = options['mail_subject']
except KeyError:
	subject = f'New {title} Submission'

if method == 'formsubmit':  # generate formsubmit link
	action_url = 'https://formsubmit.co/' + mail

html = markdown.markdown(converted)

if method == 'formsubmit' or method == 'url':
	html = f'''
	<!doctype html>
	<html lang="{lang}">
		<head>
			<title>{title}</title>
			<link rel="stylesheet" href="./styles.css">
		</head>
		<body>
			<form id="page1_form" action="{action_url}" method="POST">
				{html}
				<input type="hidden" name="_next" value="{redirect}">
				<input type="hidden" name="_subject" value="{subject}">
				<div id="submit">
					<input type="submit" value="Submit Form">
				</div>
			</form>
			<script src="./script.js"></script>
			<script src="./other.js"></script>
		</body>
	</html>
	'''.strip()  # remove leading/trailing \n
elif method == "mail":
	html = f'''
	<!doctype html>
	<html lang="{lang}">
		<head>
			<title>{title}</title>
			<link rel="stylesheet" href="./styles.css">
		</head>
		<body>
			<form id="page1_form" action="{action_url}">
				{html}
				<input type="submit" id="submit" value="Submit Form">
			</form>
			<script src="./mailto.js"></script>
			<script src="./other.js"></script>
		</body>
	</html>
	'''.strip()  # remove leading/trailing \n
else:
	html = f'''
	<!doctype html>
	<html lang="{lang}">
		<head>
			<title>{title}</title>
			<link rel="stylesheet" href="./styles.css">
		</head>
		<body>
			<form id="page1_form" action="{action_url}">
				{html}
				<input type="submit" id="submit" value="Submit Form">
			</form>
			<script src="./other.js"></script>
		</body>
	</html>
	'''.strip()  # remove leading/trailing \n

if method == 'mail':  # javascript for opening mailto links
	with open(os.path.join(assets_path, 'mailto.js'), 'r') as js:
		txt = js.read()
		txt = txt.replace('{__url__}', redirect)  # replace the redirect link at form submission
		txt = txt.replace('{__subject__}', subject)  # replaces the email subject with the user-defined
		txt = txt.replace('{__mail__}', mail)
		with open(os.path.join(out_path, 'mailto.js '), 'w') as f:
			f.write(txt)

with open(os.path.join(assets_path, 'styles.css'), 'r') as css:
	txt = css.read()
	with open(os.path.join(out_path, 'styles.css'), 'w') as f:
		f.write(txt)

with open(os.path.join(assets_path, 'other.js'), 'r') as js:
	txt = js.read()
	with open(os.path.join(out_path, 'other.js'), 'w') as f:
		f.write(txt)

with open(os.path.join(out_path, 'index.html'), 'w') as f:
	f.write(html)
