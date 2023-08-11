import os
from datetime import date
from typing import Optional, List
from lbg_utils import decode

DEFAULT_DATA_PATH = os.path.join(os.environ["HOME"], "LetterBoxed/solutions_archive")

class LBGDataInspector:

    # solutions in dict for of {length: list of sols} form
    solutions = {}

    def __init__(self, the_date: Optional[str] = None, sol_path: Optional[str] = None):

        if the_date is None:
            self.date = str(date.today())
        else:
            self.date = the_date

        if sol_path is None:
            self.solutions_root_path = DEFAULT_DATA_PATH
        else:
            self.solutions_root_path = sol_path

        self.data_root = os.path.join(self.solutions_root_path, self.date)
        if not os.path.isdir(self.data_root):
            raise RuntimeError(f"data path is invalid, try again: {self.data_root}")

        print(self.data_root)
        self.par = self.find_par()


    def find_par(self):
        found_exception = False
        len = 2
        while not found_exception:
            try:
                f = open(os.path.join(self.data_root, f"length_{len}_solutions.txt"), "r")
            except FileNotFoundError:
                found_exception = True
            finally:
                if found_exception:
                    len -= 1
                else:
                    len += 1

        print(f"par is {len}")

        return len  


    def get_sols(self, length: int):
        if not length in self.solutions.keys():
            f = f"length_{length}_solutions.txt"
            try:
                with open(os.path.join(self.data_root, f), "r") as sols:
                    self.solutions[length] = decode(sols.readlines())
            except FileNotFoundError:
                print(f"Error: could not find length {length} file ({f})")
                return None

        return self.solutions[length]
    
    def get_range_of_sols_length(self, sols):
        lengths = [len(''.join(s)) for s in sols]
        return (min(lengths), max(lengths))
    
    def get_sols_of_length(self, sols, length):
        query_res = []
        for s in sols:
            if len(''.join(s)) == length:
                query_res.append(s)

        return query_res
    
    def get_sols_with_word(self, word: str, stop_length: int = None):
        if stop_length is None:
            print("wtf")
            stop_length = self.par
        elif stop_length < 2:
            stop_length = 2

        ret_sols = []
        for len in range(2, stop_length + 1):
            sols = self.get_sols(len)
            for s in sols:
                if word in s:
                    ret_sols.append(s)

        return ret_sols
    
    # If the data has been updated since initial read, it may be useful to clear
    # so that subsequent calls to get_sols will refresh the data stored in this object
    def clear_solutions_entry(self, length):
        self.solutions.pop(length, None)

    def clear_solutions_dict(self):
        self.solutions = {}
            

if __name__ == "__main__":
    di = LBGDataInspector()