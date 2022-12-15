import random
from wordle import Wordle
from itertools import product

"""An MDP agent which seeks to solve Wordle by eliminating as many possible solutions as it can
as quickly as possible

Some code adapted from Berkeley CS188 Pacman Project 6x
"""
class FewestWordsAgent:
    def __init__(self, size):
        self.game = Wordle(size)
        self.remaining_possibilities = self.game.all_possible_solutions
        self.gamma = 0.9

    def getStartState(self):
        """
        Return the start state of the MDP.

        STATE: (# of Guesses Remaining, Possible Solutions Remaining)
        """
        return (self.game.remaining_guesses, self.remaining_possibilities)

    def getPossibleActions(self, state):
        """
        Return list of possible actions from 'state'.

        ACTION: Guess a word
        """
        if self.isTerminal(state):
            return None
        return state[1]

    def getTransitionStatesAndProbs(self, state, action):
        """
        Returns list of (nextState, prob) pairs
        representing the states reachable
        from 'state' by taking 'action' along
        with their transition probabilities.
        """
        # If you're in a terminal, there are no next states
        if self.isTerminal(state):
            return []

        # Generate all 243 possible patterns of Green/Yellow/Gray Tiles
        li = [-1, 0, 1]
        all_possible_patterns = list(product(li, li, li, li, li))

        # Generate every possible next state. Each next state has remaining_guesses of one less than the current state.
        # Each next state's word list is made up of all the words that would still be valid if that pattern occured
        next_states = [(state[0] - 1, self.possibleFollowUpsByPattern(state, action, patt)) for patt in all_possible_patterns]
        next_states = list(filter(lambda s : (len(s[1]) > 0), next_states))

        # To calculate the probability of arriving in any specific next state, sum up the total words in each next state, and
        #  normalize based on that sum. Inherently, states with more valid words will be more likely than states with fewer.
        sum = 0
        for s in next_states:
            sum += len(s[1])
        next_states_and_probs = [(s, len(s[1])/sum) for s in next_states]

        return next_states_and_probs

    def getReward(self, state):
        """
        Get the reward for the given state.
        """
        if self.game.remaining_guesses == 0:
            return 0
        return len(self.game.get_all_possible_solutions()) - len(state[1])
        

    def isTerminal(self, state):
        """
        Returns true if the current state is a terminal state.
        """
        return state[0] == 0 or len(state[1]) == 0
    
    def getQValue(self, state, action):
        """
          Computes Q values
        """
        sum = 0
        for s, prob in self.getTransitionStatesAndProbs(state, action):
            sum += prob * self.computeValueFromQValues(s)
        return self.getReward(state) + self.gamma * sum
    
    def computeValueFromQValues(self, state):
        """
          Returns max Q value over legal actions.
        """

        actions = self.getPossibleActions(state)
        if actions == None or len(actions) == 0:
          return 0
        else:
          value = float('-inf')
          for action in actions:
            new_val = self.getQValue(state, action)
            value = max(value, new_val)
          return value
    
    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.
        """
        actions = self.getPossibleActions(state)
        if actions == None or len(actions) == 0:
          return None
        else:
          value = self.computeValueFromQValues(state)
          best_actions = []
          for action in actions:
            new_val = self.getQValue(state, action)
            if new_val > value:
              best_actions = [action]
            elif new_val == value:
              best_actions += [action]
          return random.choice(best_actions)

    ### Wordle Specific Functions ###
    
    def possibleFollowUpsByPattern(self, state, guess, pattern):
        """
        Based on the current remaining possibilities, the word you just guessed,
        and the pattern of Greens, Yellows, and Grays that resulted from your
        guess, return a list of all the possible words that are still valid.
        """

        follow_ups = []

        for word in state[1]:
            if self.wordFitsPattern(guess, pattern, word) and word != guess:
                follow_ups += [word]
        
        return follow_ups
        
    
    def wordFitsPattern(self, guess, pattern, new_word):
        """
        Given the current guess and the resulting pattern of Grays,
        Yellows, and Greens, does the new_word fit?
        """
        seen_letters = []

        for n in range(5):
            fits = True

            if pattern[n] == 1:
                # Green
                if new_word[n] != guess[n]:
                    fits = False
                    return fits
            elif pattern[n] == 0:
                # Yellow
                if guess[n] not in new_word or new_word[n] == guess[n]:
                    fits = False
                    return fits
            else:
                # Gray
                if guess.count(guess[n]) == 1 and guess[n] in new_word:
                    fits = False
                    return fits
                else:
                     if new_word.count(guess[n]) >= guess.count(guess[n]) or new_word.count(guess[n]) > seen_letters.count(guess[n]):
                        fits = False
                        return fits

            seen_letters += [guess[n]]
                
        return fits
    
    def make_guess(self, shouldPrint=False):
        guess = self.computeActionFromQValues(self.getStartState())
        try:
            response = self.game.make_guess(guess)
            self.remaining_possibilities = self.possibleFollowUpsByPattern((self.game.remaining_guesses, self.remaining_possibilities), guess, response)
            if shouldPrint:
                print("Guess: " + guess)
                print(str(response) + '\n')
        except Exception as e:
            print(e)


