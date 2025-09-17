import filter  # local file for compiling the document
import argparse  # get command line arguments
import os  # join file path
import markdown  # markdown to html conversion

# --- OPEN INPUT --- #

parser = argparse.ArgumentParser(description = 'core conversion of formsMD files', epilog = 'For more help you can reach out to 0yqc@duck.com')  # set-up for automatic help, etc.
parser.add_argument('-i', '--inp', '--input', dest = 'input', help = 'path of the input file.')
parser.add_argument('-o', '--out', '--output', dest = 'output', help = 'directory where the output HTML files should be saved.')
parser.add_argument('-a', '--assets', dest = 'assets', help = 'directory which contains JS scripts and stylesheets.')
args = parser.parse_args()  # get arguments
inp_path = args.input
out_path = args.output
assets_path = args.assets

converted, options = filter.file(inp_path)  # start the compiling (./filter.py)

lang = options.get('lang') if 'lang' in options else 'en'
method = options.get('submit_method') if 'submit_method' in options else 'mail'
mail = options.get('mail_address') if 'mail_address' in options else ''
action_url = options.get('url') if 'url' in options else ''
redirect = options.get('redirect') if 'url' in options else 'window.location.href'
title = options.get('title') if 'title' in options else 'formsMD Form'
subject = options.get('mail_subject') if 'mail_subject' in options else f'New {title} Submission!'

if method == 'formsubmit':  # generate formsubmit link
	action_url = 'https://formsubmit.co/' + mail

html = markdown.markdown(converted)

if method == 'formsubmit' or method == 'url':
	html = f'''
	<!doctype html>
	<html lang="{lang}">
		<head>
			<meta charset="UTF-8">
			<meta name="viewport" content="width=device-width, initial-scale=1.0">
			<title>{title}</title>
			<link rel="stylesheet" href="./styles.css">
		</head>
		<body>
			<form id="fmd_form" action="{action_url}" method="POST" enctype=multipart/form-data>
				{html}
				<input type="hidden" name="_next" value="{redirect}">
				<input type="hidden" name="_subject" value="{subject}">
				<div id="submit">
					<input type="submit" value="Submit Form">
				</div>
			</form>
			<script src="./script.js"></script>
			<script src="./fmd.js"></script>
		</body>
	</html>
	'''.strip()  # remove leading/trailing \n
elif method == "mail":
	html = f'''
	<!doctype html>
	<html lang="{lang}">
		<head>
			<meta charset="UTF-8">
			<meta name="viewport" content="width=device-width, initial-scale=1.0">
			<title>{title}</title>
			<link rel="stylesheet" href="./styles.css">
		</head>
		<body>
			<form id="fmd_form" action="{action_url}">
				{html}
				<input type="submit" id="submit" value="Submit Form">
			</form>
			<script src="./fmd_mail.js"></script>
			<script src="./fmd.js"></script>
		</body>
	</html>
	'''.strip()  # remove leading/trailing \n
else:
	html = f'''
	<!doctype html>
	<html lang="{lang}">
		<head>
			<meta charset="UTF-8">
			<meta name="viewport" content="width=device-width, initial-scale=1.0">
			<title>{title}</title>
			<link rel="stylesheet" href="./styles.css">
		</head>
		<body>
			<form id="fmd_form" action="{action_url}">
				{html}
				<input type="submit" id="submit" value="Submit Form">
			</form>
			<script src="./fmd.js"></script>
		</body>
	</html>
	'''.strip()  # remove leading/trailing \n

if method == 'mail':  # javascript for opening mailto links
	with open(os.path.join(assets_path, 'fmd_mail.js'), 'r') as js:
		txt = js.read()
		txt = txt.replace('{__url__}', redirect)  # replace the redirect link at form submission
		txt = txt.replace('{__subject__}', subject)  # replaces the email subject with the user-defined
		txt = txt.replace('{__mail__}', mail)
		with open(os.path.join(out_path, 'fmd_mail.js'), 'w') as f:
			f.write(txt)

with open(os.path.join(assets_path, 'styles.css'), 'r') as css:
	txt = css.read()
	with open(os.path.join(out_path, 'styles.css'), 'w') as f:
		f.write(txt)

with open(os.path.join(assets_path, 'fmd.js'), 'r') as js:
	txt = js.read()
	with open(os.path.join(out_path, 'fmd.js'), 'w') as f:
		f.write(txt)

with open(os.path.join(out_path, 'index.html'), 'w') as f:
	f.write(html)
