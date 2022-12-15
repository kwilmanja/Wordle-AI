import random
from wordle import Wordle
from itertools import product

"""

"""


class LetterBasedAgent:
    def __init__(self, size):
        self.game = Wordle(size)
        self.distribution = self.buildInitialDistribution()
        self.badLetters = set()
        self.knownLetters = set()
        self.confirmed = [0, 0, 0, 0, 0]
        self.gamma = 0.9

    def buildInitialDistribution(self):
        dist = {}
        allPossible = self.game.all_possible_solutions
        for word in allPossible:
            dist[word] = 1 / len(allPossible)
        return dist

    def observe(self, pattern, previousGuess):
        """
        Updates internal data based on the previous guess and resulting pattern
        """
        for i in range(5):
            if pattern[i] == -1:
                self.badLetters.add(previousGuess[i])
            elif pattern[i] == 0:
                self.knownLetters.add(previousGuess[i])
            elif pattern[i] == 1:
                self.confirmed[i] = previousGuess[i]

        self.distribution[previousGuess] = 0
        self.updateDistribution()

    def guess(self):
        bestWords = []
        bestProb = 0
        for word, prob in self.distribution.items():
            if prob > bestProb:
                bestWords = [word]
                bestProb = prob
            elif prob == bestProb:
                bestWords += [word]
        return random.choice(bestWords)

    def updateDistribution(self):
        for word, prob in self.distribution.items():
            if self.containsChracters(word, self.badLetters):
                self.distribution[word] = 0
            else:
                self.distribution[word] = self.assessProb(word)

        self.normalizeDistribution()

    def assessProb(self, word):
        result = 1
        if self.containsChracters(word, self.knownLetters):
            result += 3
        for i in range(5):
            if word[i] == self.confirmed[i]:
                result += 1
        return result


    def normalizeDistribution(self):
        total = 0
        for word, prob in self.distribution.items():
            total += prob
        if total != 0:
            for word, prob in self.distribution.items():
                self.distribution[word] = prob / total


    def containsChracters(self, word, characters):
        for c in characters:
            if c in word:
                return True
        return False

    def make_guess(self, shouldPrint=False):
        guess = self.guess()
        try:
            response = self.game.make_guess(guess)
            self.observe(response, guess)
            if shouldPrint:
                print("Guess: " + guess)
                print(str(response) + '\n')
                self.printInfo()
        except Exception as e:
            print(e)

    def printInfo(self):
        print("Distribution: " + str(self.distribution))
        print("Bad: " + str(self.badLetters))
        print("Known: " + str(self.knownLetters))
        print("Confirmed: " + str(self.confirmed) + '\n')
