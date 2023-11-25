import ast
from typing import Optional, List

def decode(lines: List[str]):
        if lines is None or len(lines) == 0:
              return ""
        # `lines` is a list of strings of form: "['word1', 'word2']\n"
        # This method decodes this string back into a list of strings,
        # as originally solved by the lbg_solver
        ret_list = []
        for line in lines:
            l = line.strip('\n')
            if len(l) < 3:
                print(f"Found line {line} of length {len(l)}")
            try:
                ret_list.append(ast.literal_eval(l))
            except SyntaxError:
                  print(f"AST Error: couldn't handle {line}")

        return ret_list
