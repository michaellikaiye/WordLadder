#! /usr/bin/python3
import sys
import time
class Word:
    def __init__(self, v, t='', g=-1, l=[]):
        self.value = v
        self.uninformed = g
        self.list = l
        self.target = t

def my_cmpG(a, b):
    if a.uninformed < b.uninformed:
        return -1
    if a.uninformed == b.uninformed:
        return 0
    return 1

def greed(a,b):
    # assumes same size
    g = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            g += 1
    return g

def my_cmpH(a,b):
    aGreedy = greed(a.value, a.target)
    bGreedy = greed(b.value, b.target)
    if aGreedy < bGreedy:
        return -1
    if aGreedy == bGreedy:
        return 0
    return 1

def my_cmpA(a,b):
    aGreedy = greed(a.value, a.target)
    bGreedy = greed(b.value, b.target)
    aT = aGreedy + a.uninformed
    bT = bGreedy + b.uninformed
    if aT < bT:
        return -1
    if aT == bT:
        return 0
    return 1

class Pqueue:
    def OrdinaryComparison(self, a, b):
        if a < b:
            return -1
        if a == b:
            return 0
        return 1

    def __init__(self, comparator=None):
        if comparator == None:
            self.cmpfunc = self.OrdinaryComparison
        else:
            self.cmpfunc = comparator
        self.size = 0
        self.list = [None]

    def __str__(self):
        if size > 0 and isinstance(self.list[1], Word):
            return ' | '.join([i.value + ',' + str(i.uninformed) for i in self.list[1:]])
        return ' | '. join([str(i) for i in self.list[1:]])

    def push(self, data):
        self.list.append(data)
        self.size += 1
        if self.size > 1:
            currentLoc = self.size
            parentLoc = int(currentLoc / 2)
            while parentLoc > 0 and self.cmpfunc(self.list[currentLoc], self.list[parentLoc]) == -1:
                self.list[parentLoc], self.list[currentLoc] = self.list[currentLoc], self.list[parentLoc]
                currentLoc = parentLoc
                parentLoc = int(currentLoc / 2)

    def push_all(self, lst):
        for data in lst:
            self.push(data)

    def Asmallest(self, a, b, c):
        if self.cmpfunc(b, c) == 1:
            if self.cmpfunc(a, c) == 1:
                return 2
            else:
                return 0
        elif self.cmpfunc(b, c) == -1:
            if self.cmpfunc(a, b) == 1:
                return 1
            else:
                return 0
        else:
            # choose LEFT if equal
            if self.cmpfunc(a, b) == 1:
                return 1
            else:
                return 0

    def pop(self):
        if self.size == 0:
            return None
        else:
            smallest = self.list[1]
        self.list[1] = self.list[self.size]
        self.list.pop(self.size)
        self.size -= 1
        currentLoc = 1
        childLoc1 = currentLoc * 2
        childLoc2 = childLoc1 + 1
        currentIsSmaller = False
        while currentIsSmaller == False and self.size > 1:
            if childLoc1 > self.size:
                return smallest
            if childLoc1 == self.size:
                if self.cmpfunc(self.list[currentLoc], self.list[childLoc1]) == 1:
                    self.list[currentLoc], self.list[childLoc1] = self.list[childLoc1], self.list[currentLoc]
                return smallest
            if childLoc2 == self.size:
                path = self.Asmallest(
                    self.list[currentLoc], self.list[childLoc1], self.list[childLoc2])
                if path == 1:
                    self.list[currentLoc], self.list[childLoc1] = self.list[childLoc1], self.list[currentLoc]
                elif path == 2:
                    self.list[currentLoc], self.list[childLoc2] = self.list[childLoc2], self.list[currentLoc]
                return smallest
            if childLoc2 < self.size:
                path = self.Asmallest(
                    self.list[currentLoc], self.list[childLoc1], self.list[childLoc2])
                if path == 1:
                    self.list[currentLoc], self.list[childLoc1] = self.list[childLoc1], self.list[currentLoc]
                    currentLoc = childLoc1
                    childLoc1 = currentLoc * 2
                    childLoc2 = childLoc1 + 1
                elif path == 2:
                    self.list[currentLoc], self.list[childLoc2] = self.list[childLoc2], self.list[currentLoc]
                    currentLoc = childLoc2
                    childLoc1 = currentLoc * 2
                    childLoc2 = childLoc1 + 1
                else:
                    currentIsSmaller = True
        return smallest

    def length(self):
        return self.size

    def peek(self):
        if self.size == 0:
            return None
        return self.list[1]

    def tolist(self):
        q = []
        while self.size > 0:
            q.append(self.pop())
        return q





def getDict(length):
    dictall = open('dictall.txt', 'r')
    # creating dict
    dict = {}
    for line in dictall:
        word = line.strip()
        if len(word) == length:
            dict[word] = set()
    # inserting dict values
    letters = list('abcdefghijklmnopqrstuvwxyz')
    for word in dict.keys():
        for i in range(length):
            for letter in letters:
                alt = word[:i] + letter + word[i + 1:]
                if alt in dict:
                    dict[word].add(alt)
        dict[word].remove(word)
    dictall.close()
    return dict


def neighbors(infile, outfile):
    # setup
    wordsin = open(infile, 'r')
    wordsout = open(outfile, 'w')
    length = len(wordsin.readline().strip())
    wordsin.seek(0)
    dict = getDict(length)
    # returning output
    for line in wordsin:
        word = line.strip()
        if word in dict:
            s = word + ',' + str(len(dict[word])) + '\n'
        else:
            s = word + ',0\n'
        wordsout.write(s)
    wordsin.close()
    wordsout.close()
    return dict


def wordladder(inWord, outWord, dict, func):
    if not(inWord in dict) or not(outWord in dict):
        return inWord + ',' + outWord
    source = Word(inWord, outWord, 0, [inWord])
    target = Word(outWord, outWord)
    frontier = Pqueue(func)
    explored = {}
    frontier.push(source)
    top = frontier.pop()
    while top != None:
        if top.value == target.value:
            return ','.join(top.list)
        neighbors = dict[top.value]
        for neighbor in neighbors:
            if not(neighbor in explored):
                nextUninformed = top.uninformed + 1
                nextList = top.list[:]
                nextList.append(neighbor)
                next = Word(neighbor, outWord, nextUninformed, nextList)
                frontier.push(next)
        explored[top.value] = top
        top = frontier.pop()
    return inWord + ',' + outWord


def process(infile, outfile, func):
    # setup
    wordsin = open(infile, 'r')
    wordsout = open(outfile, 'w')
    line = wordsin.readline().strip()
    length = line.find(',')
    wordsin.seek(0)
    dict = getDict(length)
    # returning output
    for line in wordsin:
        words = line.strip().split(',')
        s = wordladder(words[0], words[1], dict, func)
        wordsout.write(s + '\n')
    wordsin.close()
    wordsout.close()

def longest(func):
    dict = getDict(4)
    long = []
    for word in dict:
        for other in dict:
            if greed(word,other) == 4:
                source = Word(word, other, 0, [word])
                target = Word(other, other)
                frontier = Pqueue(func)
                explored = {}
                frontier.push(source)
                top = frontier.pop()
                while top != None:
                    print(top.list)
                    if frontier.length == 2:
                        return top.list
                    neighbors = dict[top.value]
                    for neighbor in neighbors:
                        if not(neighbor in explored):
                            nextUninformed = top.uninformed + 1
                            nextList = top.list[:]
                            nextList.append(neighbor)
                            next = Word(neighbor, other, nextUninformed, nextList)
                            frontier.push(next)
                    explored[top.value] = top
                    top = frontier.pop()
    return long

def main():
    # neighbor(sys.argv[1], sys.argv[2])
    '''
    start = time.time()
    print('process using G(n):')
    process(sys.argv[1], sys.argv[2], my_cmpG)
    f = open(sys.argv[2], 'r')
    print("reading output file:")
    print(f.read())
    end = time.time()
    print(end - start)
    '''
    '''
    start = time.time()
    print('\nprocess using H(n):')
    process(sys.argv[1], sys.argv[2], my_cmpH)
    f = open(sys.argv[2], 'r')
    print("reading output file:")
    print(f.read())
    end = time.time()
    print(end - start)
    '''
    '''
    start = time.time()
    print('\nprocess using A(n):')
    process(sys.argv[1], sys.argv[2], my_cmpA)
    f = open(sys.argv[2], 'r')
    print("reading output file:")
    print(f.read())
    end = time.time()
    print(end - start)
    '''
    longest(my_cmpA)
main()
