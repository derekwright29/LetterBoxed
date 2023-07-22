from .letter_box_game import *

DEFAULT_LBG = LetterBoxGame()
DEFAULT_SETS = ["abc", "def", "ghi", "jkl"]
DEFAULT_SETS_2 = ["mno", "pqr", "stu", "vwx"]

def test_clear_set():
    the_lbg = DEFAULT_LBG

    assert(the_lbg.letter_sets != [])
    the_lbg.clear_sets()
    assert(the_lbg.letter_sets == [])

def test_add_set():

    the_lbg = DEFAULT_LBG

    orig_sets = the_lbg.letter_sets

    the_lbg.add_set('xyz')
    assert(the_lbg.letter_sets == orig_sets)

    the_lbg.clear_sets()
    new_sets = ['mno', 'pqr', 'stu', 'vwx']
    expected_sets = [i for i in new_sets]
    for i in range(0, MAX_NUM_LETTER_SETS):
        the_lbg.add_set(new_sets[i])

        assert(the_lbg.letter_sets == expected_sets[:i+1])
    

def test_super_set_coverage():
    pass

def test_init():

    the_lbg = DEFAULT_LBG

    assert(len(the_lbg.letter_sets) == 4)
    assert(len(the_lbg.super_set) == 12)
    assert(len(the_lbg.solutions) == 0)