import filter  # local file for compiling the document
import argparse  # get command line arguments
import os  # join file path
import markdown  # markdown to html conversion

# --- OPEN INPUT --- #

inp_path = os.path.join(os.getcwd(), 'input.fmd')  # set default input file, unless overwritten
out_dir = os.path.join(os.getcwd(), 'output/')  # set default output directory, unless overwritten
js_path = os.path.join(os.getcwd(), 'script.js')  # set the default position of the js file, unless overwritten

parser = argparse.ArgumentParser(description = 'core conversion of formsMD files', epilog = 'For more help you can reach out to 0yqc@duck.com')  # set-up for automatic help, etc.
parser.add_argument('-i', '--inp', '--input', dest = 'input', help = 'path of the input file. Defaults to working_dir/input.fmd')  # add argument --input to define the input file location
parser.add_argument('-o', '--out', '--output', dest = 'output', help = 'directory where the output HTML files should be saved. Defualts to working_dir/output/')  # add argument --output to define the output directory
parser.add_argument('--js', '--javascript', dest = 'javascript', help = 'file which contains necessary javascript code')
args = parser.parse_args()  # get arguments
inp_path = args.input  # overwrite the default if it has been set in the args
out_dir = args.output  # overwrite the default if it has been set in the args
js_path = args.javascript  # overwrite the default if it has been set in the args

converted = filter.file(inp_path)  # start the compiling (./filter.py)
html = markdown.markdown(converted)
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
		<script src="./script.js" def></script>
	</body>
</html>
'''.strip()

with open(js_path, 'r') as r:
	txt = r.read()
	with open(os.path.join(out_dir, 'script.js'), 'w') as f:
		f.write(txt)

with open(os.path.join(out_dir, 'page1.html'), 'w') as f:
	f.write(html)
