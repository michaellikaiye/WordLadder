Pre-Wordladder Assignment
You'll be creating a program called "neighbors.py" that reads our standard wordlist (dictall.txt), and finds the "neighbors" of each of the requested words in the input file.  It then outputs the word, and the number of its neighbors (not counting the word itself).

All the words in the input file will be the same length.

You can download the wordlist from here: dictall.txt (right-click and "Save as...")

At home, put the wordlist file into the parent of the directory where you'll be testing your program.  Therefore you'll be openning the wordlist file with the python statement:
fin = open("dictall.txt","r")

For instance, if the word is "head", then it has the following neighbors: bead, dead, lead, mead, read, heed, held, herd, heal, heap, hear, heat  for a total of 12.

If the word is "love" then its neighbors are: cove, dove, hove, move, rove, wove, lave, live, lobe, lode, loge, lone, lope, lore, lose for a total of 15

You must create a dictionary whose keys are each of the words in the entire wordlist of the required length (let's say, 4).   That means, if the length of the input words is, say 4, we can loook through the entire dictall.txt wordlist and find the approx. 2,500 4-letter words, and we must create dictionary entries for all 2,500 of them.  For each dictionary item, the value is the list of all of the words that are neighbors to the key of that entry.  For instance, one entry in the dictionary might be:  d["head"] = ["bead", "dead", "lead", "mead", "read", "heed", "held", "herd", "heal", "heap", "hear", "heat"]

You'll be given the usual input filename and output filename on the command-line like so:

- python3 neighbors.py  harry.txt  answers.txt

If the input file is:

- head
- love
- bozo
Then the output file will be:
- head,12
- love,15
- bozo,0

You will have 2 seconds of CPU to read, compute and write the output file.

You may "import sys" as your only library import
