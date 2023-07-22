import argparse
from datetime import date
import time
import os
import random
from english_words import get_english_words_set
from lbg_site_scraper import scrape_lbg_data
import copy

# CONSTANTS
MIN_WORD_LEN = 3
MAX_NUM_LETTER_SETS = 4
ENG_DICT_FILE_PATH = os.environ["HOME"] + "/eng_dictionary.txt"
STATS_FILE_PATH = os.environ["HOME"] + "/LetterBoxed/LetterBoxedStatistics.csv"
SOLUTIONS_DIR_PATH = os.environ["HOME"] + "/LetterBoxed/solutions_archive/"


class LetterBoxGame:
    def __init__(self):
        print("initting")
        self.get_dictionary()

        print("scraping today's game data")
        self.lbg_data_dict = scrape_lbg_data()
        sides = self.lbg_data_dict["sides"]
        print(f"{sides=}")
        self.clear_sets()
        if len(sides) == 4:
            for side in sides:
                print(f"adding {side=}")
                self.add_set(side)

        self.super_set = "".join(sides)
        if len(set(self.super_set)) != len(self.super_set):
            raise ValueError("sets need to have unique letters!")

        self.candidate_set = [word for word in self.lbg_data_dict["dictionary"]]

        # All viable words are in self.lbg_data_dict['dictionary']
        # Update the stored english dictionary for posterity
        self.align_dictionaries()

        self.solutions = []
        self.best_sols = []
        self.letters_to_cover = ""
        self.solve_time = 0.0

        self.solution_standard = self.lbg_data_dict['par']

        print(self)

    def __repr__(self):
        return (
            f"LetterBoxGame with "
            + str(self.letter_sets)
            + f" and {self.super_set=}. There are {len(self.candidate_set)} viable words to choose from."
        )

    def __str__(self):
        return (
            f"LetterBoxGame with "
            + str(self.letter_sets)
            + f". There are {len(self.candidate_set)} viable words to choose from."
        )
    
    def reset_stats(self):
        self.solutions = []
        self.best_sols = []
        self.solve_time = 0.0

    def get_dictionary(self):
        if (
            os.path.isfile(ENG_DICT_FILE_PATH)
            and os.stat(ENG_DICT_FILE_PATH).st_size > 1000
        ):
            f = open(ENG_DICT_FILE_PATH, "r")
            self.eng_dict = [s.strip("\n") for s in f.readlines()]
            print("pulling dictionary from file")
            f.close()
        else:
            print("pulling dictionary from scratch")
            invalids = []
            self.eng_dict = get_english_words_set(["web2"], lower=True, alpha=True)
            for word in self.eng_dict:
                if len(word) < MIN_WORD_LEN:
                    invalids.append(word)
            for inv in invalids:
                self.eng_dict.remove(inv)
            self.update_dictionary()

    def update_dictionary(self):
        f = open(ENG_DICT_FILE_PATH, "w")
        f.write("\n".join(self.eng_dict))
        f.close()

    def align_dictionaries(self):
        removes = []
        for word in self.eng_dict:
            if self.is_valid_candidate(word) and word not in self.candidate_set:
                removes.append(word)
        for word in removes:
            print(f"removing {word} from eng_dict")
            self.eng_dict.remove(word)

        self.update_dictionary()

    def clear_sets(self):
        self.letter_sets = []

    def add_set(self, letters):
        if len(self.letter_sets) == MAX_NUM_LETTER_SETS:
            print("Maximum Letter Sets reached!")
        else:
            if len(letters) == 3:
                self.letter_sets.append(letters)
            else:
                print("letter sets can only be of length 3")
                print(f"the given {letters=} is length {len(letters)}")

    def save_stats(self):
        with open(STATS_FILE_PATH, "r+") as f:
            # Put cursor at end of file
            f.seek(0, 2)
            stats_csv_str = (
                '"'
                + self.lbg_data_dict["date"]
                + '"'
                + ","
                + str(self.lbg_data_dict["par"])
                + ","
                + self.super_set
                + ","
                + str(len(self.solutions))
                + ","
                + str(len(self.best_sols))
                + ","
                + '"'
                + str(self.lbg_data_dict["ourSolution"])
                + '"'
                + ","
                + str(self.lbg_data_dict["ourSolution"] in self.solutions)
                + ","
                + '"'
                + str(self.best_sols[0])
                + '"'
                + ","
                + str(self.break_out_counter)
                + ","
                + str(self.solve_time)
                + "\n"
            )

            f.write(stats_csv_str)
        

        # solutions_path = SOLUTIONS_DIR_PATH + f"/{datetime.now().isoformat()}"
        # os.mkdir(solutions_path)
        # with open(solutions_path + f"/stats.txt", "w+") as r:
        #     r.write(stats_csv_str)

        # for i in reversed(range(2,self.solution_standard+1)):
        #     with open(SOLUTIONS_DIR_PATH + f"/{datetime.now().isoformat()}_/length_{i}_counter_{self.break_out_counter}.txt", "w+") as s:
        #         s.write('\n'.join(self.solutions))
        # if self.solution_standard != 2:
        #     with open(SOLUTIONS_DIR_PATH + f"/{datetime.now().isoformat()}_/length_2_counter_{self.break_out_counter}.txt", "w+") as sf:
        #         sf.write('\n'.join(self.best_sols))
            

    def super_set_coverage(self, word):
        coverage_set = self.super_set
        for letter in word:
            if letter in coverage_set:
                coverage_set = coverage_set.replace(letter, "")

        # Return the number of letters covered. Max is 12
        return len(self.super_set) - len(coverage_set)

    def find_possible_words(self):
        """
        This method takes in 4 sets of 3 letters and produces possible words
        """
        for word in self.eng_dict:
            if self.is_valid_candidate(word):
                self.candidate_set.append(word)

        self.candidate_set.sort(key=lambda x: self.super_set_coverage(x), reverse=True)

    def does_solution_cover_all_letters(self, words):
        self.letters_to_cover = self.super_set

        for word in words:
            for letter in word:
                if letter in self.letters_to_cover:
                    self.letters_to_cover = self.letters_to_cover.replace(letter, "")
            if len(self.letters_to_cover) == 0:
                return True
        return False

    def is_valid_candidate(self, word):
        """
        Need to check if a candidate word meets the game criteria
        1) no letters in same set are adjacent
        2) all letters in the word are included in one of the LetterSets
        """
        previous_l = ""
        for letter in word:
            if letter not in self.super_set:
                return False
            if previous_l != "":
                for letter_set in self.letter_sets:
                    if letter in letter_set:
                        if previous_l in letter_set:
                            return False
            previous_l = letter

        return True

    def get_next_word(self, prev_word, candidates):
        if prev_word is None:
            # the top of the candidates list will be the one with the most coverage
            return candidates[0]
        else:
            last_letter = prev_word[-1]
            for each in candidates:
                if each[0] == last_letter:
                    # attempt to complete the puzzle with next word
                    if set(self.letters_to_cover).issubset(set(each)):
                        return each
            # Now, try to find the word with the most coverage
            for i in range(1, len(self.letters_to_cover)):
                for each in candidates:
                    if each[0] == last_letter:
                        if set(self.letters_to_cover[:-i]).issubset(set(each)):
                            return each
        return None

    def find_solution(self, seed_set):
        self.letters_to_cover = self.super_set

        # NOTE: An explicit shallow copy had to be used here
        # because removing words from the candidate_words local variable
        # was actually removing words from self.candidate_set.
        candidate_words = copy.copy(self.candidate_set)

        guess_set = seed_set

        while not self.does_solution_cover_all_letters(guess_set):
            if (len(guess_set) == self.solution_standard):
                # This means we have not found a solution in the requisite number of words. Move on
                return None
            next_word = self.get_next_word(
                guess_set[-1] if len(guess_set) > 0 else None, candidate_words
            )
            if next_word is not None:
                candidate_words.remove(next_word)
                guess_set.append(next_word)
            else:
                return None

        return guess_set

    def shuffle_candidates(self):
        first_half = self.candidate_set[: len(self.candidate_set) // 2]
        second_half = self.candidate_set[len(self.candidate_set) // 2 :]

        random.shuffle(first_half)
        self.candidate_set = first_half + second_half

    def shuffle_candidates_full(self):
        random.shuffle(self.candidate_set)

    def prune_invalid_word(self, word):
        if word in self.eng_dict:
            self.eng_dict.remove(word)
            self.update_dictionary()
        if word in self.candidate_set:
            self.candidate_set.remove(word)

    def solve(self):
        start_time = time.time()
        print("starting solution loop")
        counter = 0
        max_counter = 0
        while True:
            self.shuffle_candidates_full()
            solution = self.find_solution(seed_set=[])

            if solution is None:
                continue

            if (
                len(solution) <= self.solution_standard
                and solution not in self.solutions
            ):
                self.solutions.append(solution)
                if len(solution) <= 2:
                    self.best_sols.append(solution)
                    print(solution, len(self.best_sols))

                if counter > max_counter:
                    max_counter = counter
                counter = 0
            else:
                counter += 1

            if counter > self.break_out_counter:
                break

            print(len(self.solutions), max_counter, end="\r")

        self.best_sols.sort(key=lambda s: len("".join(s)))

        self.solve_time = round(time.time() - start_time, 3)
        print("\nDONE!")
        print("====================================================")
        print(f"Solver found {len(self.solutions)} solutions in {self.solve_time}sec")
        print(
            f"The best solution found out of {len(self.best_sols)} length-2 solutions is:"
        )
        print(self.best_sols[0])
        print("====================================================")
        self.save_stats()

    super_set = ""
    letter_sets = []
    solutions = []
    best_sols = []
    letters_to_cover = ""
    eng_dict = None
    candidate_set = []
    solve_time = 0.0

    # The method for finding solutions is a monte carlo-style approach.
    # We randomize the order of candidate words in order to find new solutions
    # without discarding words already used in other solutions.
    # Because of this, we define a counter that determines when we decide
    # that the solution space is adequately covered.
    # if `break_out_counter` solutions in a row already exist in the solutions set,
    # we end the search and report our stats and best solution
    break_out_counter = 50

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--counter", type=int, help="Provide the break-out counter that the program determines when it has found enough solutions")
    parser.add_argument("-l", "--solution-length", type=int, help="find solutions less than or equal to [solution-length]")
    args = parser.parse_args()

    LBG = LetterBoxGame()

    if args.counter is not None:
        LBG.break_out_counter = args.counter
    if args.solution_length is not None:
        LBG.solution_standard = args.solution_length

    LBG.solve()
