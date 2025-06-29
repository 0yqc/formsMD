import compile # local file for compiling specific blocks
import sys # get command line arguments
import os # join file path

# --- OPEN INPUT --- #


try: # if there is an argument for the working directory
	inp_dir = os.path.join(sys.argv[1], "input/")
except: # assume current working directory
	inp_dir = "input/"

inp_ids = [] # init for filling in the IDs
for i in range(len(os.listdir(inp_dir))): # loop through every file in the input directory
	current = os.listdir(inp_dir)[i] # set the current file name as a var for further use
	if current.endswith(".fmd") and current.startswith("page_"): # only use files that start with page_ and end with .fmd (e.g. page_1.fmd)
		inp_ids.append(current.removeprefix("page_").removesuffix(".fmd")) # remove the parts mentioned above to only have the ID left

inp = []
for i in range(len(inp_ids)):
	inp[i] = open(inp_dir + "/page_" + inp_ids + ".fmd")