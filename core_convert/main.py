import filter # local file for compiling the document
import argparse # get command line arguments
import os # join file path
import markdown # markdown to html conversion

# --- OPEN INPUT --- #

inp_path = os.path.join(os.getcwd(), 'input.fmd') # set defualt input file, unless overwritten
out_dir = os.path.join(os.getcwd(), 'output/') # set default output directory, unsless overwritten

parser = argparse.ArgumentParser(description='core conversion of formsMD files',epilog='For more help you can reach out to 0yqc@duck.com') # set-up for autmatic help, etc.
parser.add_argument('-i', '--inp', '--input', dest='input', help='path of the input file. Defaults to working_dir/input.fmd') # add argument --input to define the input file location
parser.add_argument('-o', '--out', '--output', dest='output', help='directory where the output HTML files should be saved. Defualts to working_dir/output/') # add argument --output to define the output directory
args = parser.parse_args() # get arguments
inp_path = args.input # overwritte the default if it has been set in the args
out_dir = args.output # overwritte the default if it has been set in the args 

converted = filter.file(inp_path) # start the compiling (./filter.py)
html = markdown.markdown(converted)

out = open(os.path.join(out_dir,"page1.html"),"w")
out.write(html)
print(converted)