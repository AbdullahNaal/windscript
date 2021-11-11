# sys is used to parse the command-line arguements.
import sys

# First, we must make sure we have an arguement, which would be the name of the script we will interpret.
assert sys.argv[1]

# And we get it here. It is the first (and only) arguement. The program will work even if there are redundant arguements.
script_name = sys.argv[1]

# We will store the script here.
script = ""

# Now we open the script in read-only mode, and store it in script.
with open(script_name, 'r') as windscript:
    script = windscript.read()

# Here is the possibilities of the syntax:
syntax = ["let it be known that NEW_VAR is EXPRESSION", "an input", "the sum of EXPRESSION and EXPRESSION", "is bigger than EXPRESSION", "print EXPRESSION", "if EXPRESSION, STATEMENT"]

# And we open a new file to write python in.
pythonscript = open(script_name + ".py", 'w')

# We get a list of the words in the script. We will compare these with the syntax.
script_lines = script.split('\n') # If we don't split by \n, we will get some items like "input\nif"
script_words = []
for n in range(len(script_lines)):
    script_words += script_lines[n].split(' ')

# index is a global variable that will track where we are at the script.
index = 0

# The next functions describe the output of each item in the syntax list.

"""
The entire idea is that statements will write to the file,
and expressions will return strings for the statements to write.

However, sometimes expressions occur within expressions, and the cycle ends with a variable name or with an absolute (number or string). We still can't deal with that. That's why we have an eyesore at iffu().
"""

def letbeknown():
    # We want to use the global index, so:
    global index
    # and we move up until we reach the variable's name.
    while(not script_words[index] == "that"):
        index += 1
    index+=1
    # Now we write it:
    pythonscript.write(script_words[index] + " = ")
    # And we move towards its value.
    index += 2
    # Its value is an expression, the very next expression, in fact:
    exp = find_next()
    """
    Please note the find_next() returns the next function's return. The next one is an expression,
    so it will return a string to fit here.
    However, we still can't discern if what we came upon is an expression or a statement,
    thus, one can write "let it be known that x is print x" and the interpreter will cry in the corner.
    For now, we will assume the greatest of circumstances, and we will correct later.
    Also, find_next() does not know that a variable name by itself is an expression, or a number for that.
    So, stuff like "let it be known that x is 5" won't go well.

    Well, step by step, shall we?
    """

    # Anyway, we got the expression we want to assign, and we skip to the next line.
    # Oh, also note that we don't care about indentation yet. I think we should have a global variable
    # called indent that is initially 0, and at each statement we loop throught it before writing.
    # However, that is still an idea.
    pythonscript.write(exp)
    pythonscript.write('\n')
    
def inp():
    # Pretty straigthforward.
    global index
    index += 1
    return "input()"

def sumof():
    global index
    # We move towards the first of the two.
    while(not script_words[index] == "of"):
        index +=1
    index +=1
    # and we just plaster a "+" between the things to sum.
    to_return = script_words[index] + " + " + script_words[index+2]
    index +=3
    return to_return

def isbigger():
    global index
    # Same stuff.
    while(not script_words[index] == "than"):
        index += 1
    index += 1
    # It compares to an expression (number maybe), but oh well, we can't deal with that yet, so . . .
    exp = script_words[index]
    # Please frgiv me-=-=-=-=-=- I just plastered whatever written after "bigger than" instead. 
    return " > " + exp

def printu():
    global index
    # If you are curious, we are moving forward here (index += 1) because index was referring to "print"
    # and well, we are dealing with that, so, neeeext!
    index += 1
    pythonscript.write("print(" + script_words[index] + ")\n")
    # I know, we should print an expression, but please bear with me for now.

def iffu():
    global index
    index += 1
    # The following lines are . . . a sight to behold.
    exp = find_next()
    exp += find_next()
    pythonscript.write("if " + exp + ": \n\t")
    # None of that will remain after I figure out how to get expressions correctly, and indent correctly.

    
# *Ahem* Now we register the functions in the order the corresponding syntax occurs in the syntax list.
interprets = [letbeknown, inp, sumof, isbigger, printu, iffu]
# interprets is a bad name; I will change it later.

# This guy stops when he matches a word from the script with the syntax.
# He won't complain if you write things that does not match the syntax.
# Heck, he is okay with you writing in arabic or whatever language you like.
# He also will look at only one word from the syntax (only "let" from "let it be known that")
# Actually, find_next() is still a kid, so excuse its manners.
def find_next():
    global index
    # Using global index does not sit well with me, for some reason, but oh well. Can't find aother way.
    # We will look forward until we reach the end of the script . . .
    while index < len(script_words):
        # and we will see if there are candidates that fit the word in the script.
        candidates = [synt for synt in syntax if synt[:len(script_words[index])] == script_words[index]]
        # if there is only one, then, well, we found it . . .
        # but actually not; we should check if it matches it FULLY, and we ain't doing that here . . .
        # yet.
        if len(candidates) == 1:
            # If we find a way to interpret, we will fire the corresponding function.
            return interprets[syntax.index(candidates[0])]()
        else:
            # if not, then we will continue until we do (or run out of words).
            index += 1

# Finally, the main code.
# Keep findin' 'em syntaxers until the document ends.
while index < len(script_words):
    find_next()

# and we ain't gonna forget to close out friend pythonscript.
pythonscript.close()
