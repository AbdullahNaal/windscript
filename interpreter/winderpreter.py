# sys is used to parse the command-line arguements.
import sys

# First, we must make sure we have an arguement, which would be the name of the script we will interpret.
assert sys.argv[1]

# And we get it here. It is the first (and only) arguement. The program will work even if there are redundant arguements.
script_name = sys.argv[1]

# Now we open the script in read-only mode, and open a new file in write mode.
with open(script_name, 'r') as windscript:
    with open(script_name + ".py", 'w') as pythonscript:
        # for now, I just dumped the entire thing there. Still no idea how to go about it.
        pythonscript.write(windscript.read())

