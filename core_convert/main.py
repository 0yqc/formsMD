import filter  # local file for compiling the document
import argparse  # get command line arguments
import os  # join file path
import markdown  # markdown to html conversion

# --- OPEN INPUT --- #

parser = argparse.ArgumentParser(description = 'core conversion of formsMD files', epilog = 'For more help you can reach out to 0yqc@duck.com')  # set-up for automatic help, etc.
parser.add_argument('-i', '--inp', '--input', dest = 'input', help = 'path of the input file.')
parser.add_argument('-o', '--out', '--output', dest = 'output', help = 'directory where the output HTML files should be saved.')
parser.add_argument('-a', '--assets', dest = 'assets', help = 'directory which contains script.js and style.css.')
args = parser.parse_args()  # get arguments
inp_path = args.input  # overwrite the default if it has been set in the args
out_dir = args.output  # overwrite the default if it has been set in the args
assets_path = args.assets  # overwrite the default if it has been set in the args

converted = filter.file(inp_path)  # start the compiling (./filter.py)
html = markdown.markdown(converted, extensions = ['md_in_html'])
html = f'''
<!doctype html>
<html>
	<head>
		<title>fMD Form</title>
		<link rel="stylesheet" href="./style.css">
	</head>
	<body>
		<form id="page1_form">
			{html}
			<p id="page1_submit">
				<input type="submit" value="Submit Form">
			</p>
		</form>
		<script src="./script.js"></script>
	</body>
</html>
'''.strip() # remove leading/trailing \n

with open(os.path.join(assets_path,'script.js'), 'r') as js:
	txt = js.read()
	with open(os.path.join(out_dir, 'script.js'), 'w') as f:
		f.write(txt)

with open(os.path.join(assets_path,'style.css'), 'r') as css:
	txt = css.read()
	with open(os.path.join(out_dir, 'style.css'), 'w') as f:
		f.write(txt)

with open(os.path.join(out_dir, 'page1.html'), 'w') as f:
	f.write(html)