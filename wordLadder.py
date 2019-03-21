#! /usr/bin/python3
import sys
import time

target = ''
dict = {}

class Word:
    def __init__(self, v, g=-1, l=[]):
        self.value = v
        self.uninformed = g
        self.list = l

def greed(a):
    # assumes same size as target
    g = 0
    for i in range(len(a)):
        if a[i] != target[i]:
            g += 1
    return g

def my_cmpA(a,b):
    aT = greed(a.value) + a.uninformed
    bT = greed(b.value) + b.uninformed
    if aT < bT:
        return -1
    if aT == bT:
        return 0
    return 1

def Lmy_cmpA(a,b):
    aGreedy = greed(a[1])
    bGreedy = greed(b[1])
    aT = aGreedy + a[0]
    bT = bGreedy + b[0]
    if aT < bT:
        return -1
    if aT == bT:
        return 0
    return 1

def uninformedL(a,b):
    aT = a[0]
    bT = b[0]
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
    global dict
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


def neighbors(infile, outfile):
    # setup
    wordsin = open(infile, 'r')
    wordsout = open(outfile, 'w')
    length = len(wordsin.readline().strip())
    wordsin.seek(0)
    getDict(length)
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


def wordladder(inWord, outWord, func):
    if not(inWord in dict) or not(outWord in dict):
        return inWord + ',' + outWord
    source = Word(inWord, 0, [inWord])
    global target
    target = outWord
    frontier = Pqueue(func)
    explored = {}
    frontier.push(source)
    top = frontier.pop()
    while top != None:
        if top.value == target:
            return ','.join(top.list)
        neighbors = dict[top.value]
        for neighbor in neighbors:
            if not(neighbor in explored):
                nextUninformed = top.uninformed + 1
                nextList = top.list[:]
                nextList.append(neighbor)
                next = Word(neighbor, nextUninformed, nextList)
                frontier.push(next)
        explored[top.value] = top
        top = frontier.pop()
    return inWord + ',' + outWord

def Lwordladder(inWord, outWord, func):
    if not(inWord in dict) or not(outWord in dict):
        return inWord + ',' + outWord
    # cost, current, list
    source = [0, inWord, inWord]
    global target
    target = outWord
    frontier = Pqueue(func)
    explored = {}
    frontier.push(source)
    top = frontier.pop()
    while top != None:
        current = top[1]
        if current == target:
            return ','.join(top[2:])
        neighbors = dict[current]
        for neighbor in neighbors:
            if not(neighbor in explored):
                next = top[:]
                next[0] = top[0] + 1
                next[1] = neighbor
                next.append(neighbor)
                frontier.push(next)
        explored[current] = 0
        top = frontier.pop()
    return inWord + ',' + outWord



def process(infile, outfile, func, ladder):
    # setup
    wordsin = open(infile, 'r')
    wordsout = open(outfile, 'w')
    line = wordsin.readline().strip()
    length = line.find(',')
    wordsin.seek(0)
    getDict(length)
    # returning output
    for line in wordsin:
        words = line.strip().split(',')
        s = ladder(words[0], words[1], func)
        wordsout.write(s + '\n')
    wordsin.close()
    wordsout.close()

def longest(word):
    source = [0, word, word]
    frontier = Pqueue(uninformedL)
    explored = {}
    frontier.push(source)
    top = frontier.pop()
    long = []
    while top != None:
        current = top[1]
        if len(top) > len(long):
            long = top[:]
        # print(','.join(top[2:]))
        neighbors = dict[current]
        for neighbor in neighbors:
            if not(neighbor in explored):
                next = top[:]
                next[0] = top[0] + 1
                next[1] = neighbor
                next.append(neighbor)
                frontier.push(next)
        explored[current] = 0
        top = frontier.pop()
    return long

def processLong(length):
    getDict(length)
    longestAns = [0]
    i = 0
    for word in dict.keys():
        ans = longest(word)
        if ans[0] >= longestAns[0]:
            longestAns = ans[:]
        # print(ans[0], ans[2:])
        i += 1
        if i%10 == 1:
            print(longestAns[0], longestAns[2:])
            print(ans[0], ans[2:])

def main():
    # neighbor(sys.argv[1], sys.argv[2])

    # start = time.time()
    # print('\nprocess using A(n):')
    # process(sys.argv[1], sys.argv[2], my_cmpA, wordladder)
    # f = open(sys.argv[2], 'r')
    # print("reading output file:")
    # print(f.read())
    # end = time.time()
    # print(end - start)

    start = time.time()
    print('\nL process using A(n):')
    process(sys.argv[1], sys.argv[2], Lmy_cmpA, Lwordladder)
    f = open(sys.argv[2], 'r')
    print("reading output file:")
    print(f.read())
    end = time.time()
    print(end - start)


    # processLong(4)

main()