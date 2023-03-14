from wordle import Wordle

def main():
    print('KEY:\n\t-1 => Letter Not In Word\n\t0 => Letter In Word, Wrong Position\n\t1 => Letter In Correct Position\n')

    wordle = Wordle()

    while wordle.remaining_guesses > 0 and not wordle.victory:
        current_guess = input("Guess a word:\n").lower()
        try:
            print(wordle.make_guess(current_guess))
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()