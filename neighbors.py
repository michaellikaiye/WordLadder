#! /usr/bin/python3
import sys
#import time
#start_time = time.time()

# setup
dictall = open('dictall.txt', 'r')
wordsin = open(sys.argv[1], 'r')
wordsout = open(sys.argv[2], 'w')

inputs = wordsin.read().split('\n')
allwords = dictall.read().split('\n')

for i in range(len(inputs)):
    if inputs[i] == '':
        inputs.pop(i)

# creating dict
length = len(inputs[0])
dict = {}
for word in allwords:
    if len(word) == length:
        dict[word] = []

# inserting dict values
letters = list('abcdefghijklmnopqrstuvwxyz')
for word in dict.keys():
    temp = set()
    for i in range(length):
        for letter in letters:
            alt = word[:i] + letter + word[i + 1:]
            if alt in dict:
                temp.add(alt)
    temp.remove(word)
    dict[word] = list(temp)

# returning output
for word in inputs:
    n = 0
    if word in dict:
        n = len(dict[word])
    s = word + ',' + str(n) + '\n'
    wordsout.write(s)
dictall.close()
wordsin.close()
wordsout.close()

# extra
f = open(sys.argv[2], 'r')
print("reading output file:")
print(f.read())
#elapsed_time = time.time() - start_time
#print('time elapsed:', elapsed_time)
