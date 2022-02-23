"""
Wordle
"""

from collections import defaultdict
import logging
import os
import sys
import uuid

import pandas as pd

logging.getLogger().setLevel(logging.INFO)


class Player:

    """"""

    def __init__(self, name):
        self.name = name
        self.guesses = defaultdict(list)
        self.score = 0

    def __str__(self):
        return self.name


class Game:

    """"""

    def __init__(self, word_length=5):

        self.game_uuid = str(uuid.uuid4())

        # config
        self.word_length = word_length

        # parse words
        self.words = pd.read_csv("data/words_alpha.txt", names=["word"])
        self.words = self.words[self.words.word.str.len() == self.word_length]
        self.words_set = set(list(self.words.word))
        print(f"loaded {len(self.words)} words with length {self.word_length}")

        # players
        self.players = []
        self.asker_idx = 0
        self.guesser_idx = 1

    @property
    def asker(self):
        return self.players[self.asker_idx]

    @property
    def guesser(self):
        return self.players[self.guesser_idx]

    def set_players(self, names):
        for name in names:
            self.players.append(Player(name))

        print(f"Welcome {self.players[0].name} and {self.players[1].name}!\n")

    def parse_guess(self, word, guess):

        # nailed it
        if word == guess:
            return True, "!" * self.word_length

        # else, return meaningful output
        output = ""
        for i, c in enumerate(guess):
            if c not in word:
                output += "X"
            elif c in word and c != word[i]:
                output += "?"
            else:
                output += "!"
        return False, output

    def play(self):

        while True:

            round_uuid = str(uuid.uuid4())
            _ = os.system("clear")

            # get word
            word = None
            while True:
                word = (
                    input(f"First, {self.asker.name}, please enter a word: ")
                    .lower()
                    .strip()
                )
                if word in self.words_set:
                    _ = os.system("clear")
                    print("Thanks!  Here we go...\n")
                    break
                else:
                    print(
                        f"word not recognized or not word length {self.word_length}, try again"
                    )

            # guess
            count = 0
            while count < 7:

                if count == 6:
                    print(f"Sorry, that's all your guesses!  The word was: {word}.")
                    break
                
                guess_names = {
                    0:"first",
                    1:"second",
                    2:"third",
                    3:"fourth",
                    4:"fifth",
                    5:"sixth and final"
                }
                
                guess = (
                    input(f"{self.guesser.name}, your {guess_names[count]} guess please: ")
                    .lower()
                    .strip()
                )
                if guess not in self.words_set:
                    print(
                        f"word not recognized or not word length {self.word_length}, try again"
                    )
                    continue
                elif guess in [
                    _guess[0] for _guess in self.guesser.guesses[round_uuid]
                ]:
                    print("word already guess, please try again")
                    continue
                else:
                    logging.debug("valid guess received")
                    count += 1
                    result, output = self.parse_guess(word, guess)
                    self.guesser.guesses[round_uuid].append((guess, output))
                    if result:
                        print("Success!  Well done.")
                        self.guesser.score += 1
                        break
                    else:
                        # print(f"Not quite, here's what you've tried so far:")
                        for _guess, _output in self.guesser.guesses[round_uuid]:
                            print(f"#{count}, '{_guess}' --> {_output}")
                        continue

            play_again = input("Play again (y/n)? ").strip().lower()
            if play_again == "y":
                self.asker_idx, self.guesser_idx = self.guesser_idx, self.asker_idx
                continue
            else:
                print("Well, we had fun.  Final scores:")
                for player in self.players:
                    print(f"\tPlayer {player.name} score: {player.score}")
                return


def play(word_length=5):

    """"""
    _ = os.system("clear")

    g = Game(word_length=word_length)

    names = [input(f"Enter name for Player {x}: ") for x in range(0, 2)]
    g.set_players(names)

    g.play()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        word_length = int(sys.argv[1])
    else:
        word_length = 5
    play(word_length=word_length)
