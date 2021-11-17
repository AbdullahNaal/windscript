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
syntax = ["let it be known that", "an input", "the sum of", "is bigger than", "print", "if", "and"]

# And we open a new file to write python in.
pythonscript = open(script_name + ".py", 'w')

# We get a list of the words in the script. We will compare these with the syntax.
script_lines = script.split('\n') # If we don't split by \n, we will get some items like "input\nif"
script_words = []
for n in range(len(script_lines)):
    script_words += script_lines[n].split(' ')

# index is a global variable that will track where we are at the script.
index = 0

# mode is where we will tell what kind of code we expect. We will assert it in the functions.
# It has three possibilities: [s]tatement, [e]xpression, and [c]ondition.
mode ="s"
# We start with seeking a statement, because it will be weird otherwise, right?

# We will store all known variables so we can return them as an expression when needed.
variables = []
# and it starts as nothing. It is the job of the functions to change it.
# Please note that we are not using it yet, so it is kinda just sitting here for now.
it = "nothing_yet"

# The guy here refers to the last used statement. When we string statements using "and," we want to know
# What was the last used statement.
last_index = -1
# The next functions describe the output of each item in the syntax list.

"""
The entire idea is that statements will write to the file,
and expressions will return strings for the statements to write.
"""

# All statements shall have an optional arguement called 'continuation.'
# If it is a continuation, then it was called using 'andu,' and 'andu' would have set the index correctly.
# Therefore, we shall not modify the index if we were called using 'andu.'
def letbeknown(continuation=False):
    # We want to use the global index, the global mode, and the global last index, so:
    global index, mode, last_index
    # And we have to make sure that a statement is appropriate here, so:
    assert mode == "s"
    # and we move up until we reach the variable's name.
    # We will only move up if it was called normally. If it was called using 'and' as a continuation, 
    # then the index is already set.
    if not continuation:
        while(not script_words[index] == "that"):
            index += 1
        index+=1
    # Now we write it:
    pythonscript.write(script_words[index] + " = ")
    # and we register the new variable:
    variables.append(script_words[index])
    # And we move towards its value.
    index += 2
    # Its value is an expression, the very next expression, in fact:
    mode = "e" # We are expecting an expression.
    exp = find_next()
    # Please note the find_next() returns the next function's return. The next one is an expression,
    # so it will return a string to fit here.

    # Anyway, we got the expression we want to assign, and we skip to the next line.
    # Oh, also note that we don't care about indentation yet. I think we should have a global variable
    # called indent that is initially 0, and at each statement we loop throught it before writing.
    # However, that is still an idea.
    pythonscript.write(exp)
    pythonscript.write('\n')
    # Now at a new line we expect another statement:
    mode = "s"
    # We set the last used statement to be 0, the index of this function in the interprets list, down below.
    last_index = 0
    
def inp():
    # Pretty straigthforward.
    global index, mode
    assert mode == "e"
    # We are jumping two in the index because it is "an input," two words.
    index += 2
    return "input()"

def sumof():
    global index, mode
    assert mode == "e"
    # We move towards the first of the two.
    while(not script_words[index] == "of"):
        index += 1
    index += 1
    # We will sum two expressions, so:
    mode = "e"
    exp = find_next()
    # this will stop at the word "and," so we move one more word
    index += 1
    # and we land on the next expression.
    mode = "e"
    exp2 = find_next()
    # Well, we sum them. We will cast them to float, just in case. Inputs come as a string, so just in case:
    to_return = "float(" + exp + ")" + " + " + "float(" + exp2 + ")"
    # While this will result in atrocities in the python file, it works. No one will read it anyway . . .
    return to_return

def isbigger():
    global index, mode
    # Same stuff.
    assert mode == "c"
    while(not script_words[index] == "than"):
        index += 1
    index += 1
    # It compares to an expression (number maybe), so:
    mode = "e"
    exp = find_next()
    # So, it just returns " > exp" Makes sense?
    # We will cast the expression to float, just in case:
    return " > " + "float(" + exp + ")"

def printu(continuation=False):
    global index, mode, last_index
    assert mode == "s"
    # Again, we only move forward in the index if it was not set already.
    if not continuation:
        index += 1
    mode = "e"
    exp = find_next()
    # and we output "print(str(exp))" where exp is the next expression.
    pythonscript.write("print(str(" + exp + "))\n")
    mode = "s"
    last_index = 4

def iffu(more = "nah"):
    global index, mode
    # We will only move the index forward if we start at if. 
    # If we start at more conditions, then the index is already correct.
    if more != "yeah":
        index += 1
    assert mode == "s"
    # If will take an expression first, then a condition.
    mode = "e"
    exp = find_next()
    mode = "c"
    exp += find_next()
    # Now, if we are not adding more conditions, then we just started, so:
    if more != "yeah":
        pythonscript.write("if")
    # In any case, we will write the condition we got:
    pythonscript.write(" " + exp)
    # We ready the mode for the next statement:
    mode = "s"
    # Now, if we land on more conditions, we will add them by calling iffu using more:
    if script_words[index] == "and" or script_words[index] == "or":
        pythonscript.write(" " + script_words[index])
        index += 1
        iffu("yeah")
    # At the end, all the iffus we called will reach here, but we only want one of them to add an end-line.
    # The one that shall end it is the one that called them all:
    if more != "yeah":
        pythonscript.write(": \n\t")

    # We are not setting last_index here, because iffu has its own way to deal with the ands and ors.

def andu():
    global index, mode, last_index
    # 'and' will appear in the place of a statement only, so:
    assert mode == "s"
    # if an expression expects 'and,' it will deal with it itself.
    index += 1 # We processed 'and' and we move on.
    # If the last index is -1, this means that no statement was called yet.
    # If we find a statement after the and, we should delegate all the work to the statement we found.
    # In any case, 'and' here serves no purpose and we just leave. The interpreter will call find_next()
    # by itself, and it will solve any issues, if they exist.
    if last_index == -1 or find_next(type_only=True) == "s":
        return "okay, nothing to do here."
    # If, however, we encounter an expression or sth, 
    # then we shall deal with it just like the last statement did:
    return interprets[last_index](continuation=True)

    
# *Ahem* Now we register the functions in the order the corresponding syntax occurs in the syntax list.
interprets = [letbeknown, inp, sumof, isbigger, printu, iffu, andu]
# interprets is a bad name; I will change it later.

# The type of each function in the interprets list. We will use that for andu.
types = ["s", "e", "e", "c", "s", "s", "s"]

# Now, the meat of the program is here. This guy will find the next syntax we should execute.
# With an optional arguement that checks if we are only interested in the type of the next word we hit.
def find_next(type_only=False):
    global index, mode, types
    # Using global index does not sit well with me, for some reason, but oh well. Can't find aother way.
    # We first hafta make sure we are within the bounds of the script:
    if index < len(script_words) - 1: 
        # if the word is a string, then, well, a string is an expression.
        # We can only deal with one word strings as of this moment, 
        # but changing that is easy.
        if script_words[index][0] == '"' and script_words[index][-1] == '"':
            # If we are only interested in the type, then, well, it is an expression.
            if type_only:
                return "e"
            # We increase the index, because we are done with the word.
            index += 1
            # We have to make sure an expression is appropriate here:
            assert mode == "e"
            return script_words[index-1]
        # if the word is a number or a variable name, we will return it as is. Both are an expression.
        if script_words[index].isnumeric() or script_words[index] in variables:
            if type_only:
                return "e"
            index += 1
            assert mode == "e"
            # Same as the last one.
            return script_words[index - 1]
        # and we will see if there are candidates that fit the word in the script.
        # The candidates are the items in the syntax list. n is the length of the word we came across.
        # if the first n letters of the syntax equal the word, then it is a candidate.
        candidates = [synt for synt in syntax if synt[:len(script_words[index])] == script_words[index]]
        # Now, we need to filter the candidates.
        # The first few characters matching does not guarantee that all will match.
        # For each candidate, we will run some checks:
        for candidate in candidates:
            # If the entirety of the candidate is just one word that equals the word we came across,
            # then it shall pass.
            if candidate == script_words[index]:
                continue
            # If it is just one word that does not equal the word we came across,
            if ' ' not in candidate:
                # then we are sorry, you shall not pass.
                candidates.remove(candidate)
                # and we call for the next candidate. No need to execute the rest of the loop.
                continue
            # Okay. Here will remain the dudes that are more than one word, 
            # who may or may not be the correct syntax to call.

            # Let's say the candidate is n words long. We will construct the script_full_word
            # from n words after the current one we are at, including it.
            # If we stopped at "an" from "an inputti," and "an input" was a candidate,
            # the candidate has two words, so we string "an" with "inputti," two words,
            # and the full word will become "an inputti" as it was in the script.
            # Like that, we can compare justly.
            script_full_word = ""
            # Here we are stringing words and comparing them, 
            # but we can also compare word by word, which will require less code,
            # but who cares. ^_^
            for i, word in enumerate(candidate.split(' ')):
                script_full_word += script_words[index + i] + ' ' # we be adding a word, then a whitespace,
            # but this results in a whitespace at the end. We shall remove it:
            script_full_word = script_full_word[:len(script_full_word)-1]
            # The moment of truth . . .
            if script_full_word != candidate:
                candidates.remove(candidate)
        # At this point, candidates will either have one true champion, or nothing.
        if len(candidates) == 1: # I know, we can say "if candidates:" but I like wasting space.
            if type_only: # After all the trouble, we return the type . . . oh well.
                return types[syntax.index(candidates[0])]
            # After finding the sole champion syntax candidate, we will fire the corresponding function.
            return interprets[syntax.index(candidates[0])]()
        else: # If, God forbid, nothing matches,
            if type_only: # The last hope will be we are checking for the type.
                return "e, probably" # We don't recognize what we came across, so it is an expression, I guess.
                # Most likely it is a variable name we have not registered yet or sth.
                # Whatever it might be, it is most likely an expression.
            # If not, however. If we were trying to call a function, but we found no suitable thing to call,
            # Then it is a syntax error. We will print the index of the word and the offending word.
            # We can get creative with the error message, but this will suffice for now.
            print(index, script_words[index])
            print("Syntax Error")
            exit()

# Finally, the main code.
# Keep findin' 'em syntaxers until the document ends. 
# The last word of the document is '\0' or sth, so we will ignore that.
while index < len(script_words) - 1:
    find_next()

# and we ain't gonna forget to close our friend pythonscript.
pythonscript.close()
