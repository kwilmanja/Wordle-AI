from letter_based_agent import LetterBasedAgent
from fewest_words_agent import FewestWordsAgent
import datetime

def averageTime(timedeltas):
    return sum(timedeltas, datetime.timedelta(0)) / len(timedeltas)


def main(gameCount, sampleSize, agentName):
    print(
        'KEY:\n\t-1 => Letter Not In Word\n\t0 => Letter In Word, Wrong Position\n\t1 => Letter In Correct Position\n')
    wins = 0
    guessLog = []
    timeLog = []

    for i in range(gameCount):
        print('Starting Game ' + str(i))

        if agentName == "FewestWords":
            agent = FewestWordsAgent(sampleSize)
        else:
            agent = LetterBasedAgent(sampleSize)
        game = agent.game

        start = datetime.datetime.now()
        while game.gameOver():
            agent.make_guess(True)
        end = datetime.datetime.now()

        if game.victory:
            numGuesses = 6 - game.remaining_guesses
            print('Correct! Puzzle Solved in ' + str(numGuesses) + ' guesses!')
            wins += 1
            guessLog.append(numGuesses)
            timeLog.append(end - start)
        else:
            print('Game Over. You Lost! Answer: ' + game.target_word)

        print('Time: ' + str(end - start) + '\n')

    print("Algorithm Summary: ")
    print('Number of Games: ' + str(gameCount))
    print('Word Sample Size: ' + str(sampleSize))
    print('Win Percentage: ' + str(wins / gameCount))
    print('Average Number of Guesses: ' + str(sum(guessLog) / wins))
    print('Average Time of Wins: ' + str(averageTime(timeLog)))


def mainNoPrints(gameCount, sampleSize, agentName=0):
    wins = 0
    guessLog = []
    timeLog = []

    for i in range(gameCount):
        print('Starting Game ' + str(i))

        if agentName == 0:
            agent = FewestWordsAgent(sampleSize)
        else:
            agent = LetterBasedAgent(sampleSize)

        game = agent.game

        start = datetime.datetime.now()
        while game.gameOver():
            agent.make_guess()
        end = datetime.datetime.now()

        if game.victory:
            numGuesses = 6 - game.remaining_guesses
            wins += 1
            guessLog.append(numGuesses)
            timeLog.append(end - start)

    print("Algorithm Summary: ")
    print('Number of Games: ' + str(gameCount))
    print('Word Sample Size: ' + str(sampleSize))
    print('Win Percentage: ' + str(wins / gameCount))
    print('Average Number of Guesses: ' + str(sum(guessLog) / wins))
    print('Average Time of Wins: ' + str(averageTime(timeLog)))



if __name__ == "__main__":
    """
    Call main(number of game to play, number of words to sample, 0 for FewestWordsAgent and 1 for LetterBasedAgent)
    mainNoPrints : same as main but doesn't print as much
    """
    mainNoPrints(1000, 2000, 1)

