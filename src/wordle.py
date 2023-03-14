import random

class Wordle:
    def __init__(self, size=100):
        self.all_possible_solutions = self.get_possible_solutions_sampled(size)
        self.target_word = self.all_possible_solutions[random.randint(0, len(self.all_possible_solutions) - 1)]
        self.remaining_guesses = 6
        self.guesses = []
        self.victory = False

    """Returns a sampled list of possible solutions (subset of Valid Words)"""
    def get_possible_solutions_sampled(self, n):
        result = []
        with open('possible-solutions.txt','r') as file:
            # reading each line    
            for line in file:
                # reading each word        
                for word in line.split():
                    # adding the word to the list           
                    result += [word]
        return random.sample(result, n)

    """Returns a list of all possible solutions (subset of Valid Words)"""
    def get_all_possible_solutions(self):
        result = []
        with open('possible-solutions.txt','r') as file:
            # reading each line    
            for line in file:
                # reading each word        
                for word in line.split():
                    # adding the word to the list           
                    result += [word]
        return result

    """Returns a list of all acceptable guesses"""
    def get_all_valid_words(self):
        result = []
        with open('valid-wordle-words.txt','r') as file:
            # reading each line    
            for line in file:
                # reading each word        
                for word in line.split():
                    # adding the word to the list           
                    result += [word]
        return result

    """Evaluates a guess and returns the feedback"""
    def assess_move(self, guess):
        result = []
        seen_letters = []

        for n in range(5):
            if self.target_word[n] == guess[n]:
                # Correct Position (GREEN)
                result += [1]
            elif guess[n] not in self.target_word:
                # Wrong Letter (GRAY)
                result += [-1]
            else:
                # Right Letter, Wrong Position (YELLOW)
                #   Makes sure duplicate letters are marked correctly. Eg, if the letter m
                #   appears in the target once and is in the guess twice, it should only be
                #   marked 0 once.
                if guess.count(guess[n]) <= self.target_word.count(guess[n]):
                    result += [0]
                elif self.target_word.count(guess[n]) > seen_letters.count(guess[n]):
                    result += [0]
                else:
                    result += [-1]

            seen_letters += [guess[n]]
        return result

    """Get a guess"""
    def make_guess(self, guess):
        if len(guess) != 5 or guess not in self.get_all_valid_words():
            raise Exception(guess + ' is not a valid Wordle word.')

        if self.remaining_guesses > 0:
            self.remaining_guesses -= 1
            self.guesses += [guess]

            if guess == self.target_word:
                self.victory = True
        return self.assess_move(guess)


    def gameOver(self):
        return self.remaining_guesses > 0 and not self.victory