from letter_box_game import *
from shutil import rmtree

from pytest import fixture

# DEFAULT_LBG = LetterBoxGame()
DEFAULT_SETS = ["abc", "def", "ghi", "jkl"]
DEFAULT_SETS_2 = ["mno", "pqr", "stu", "vwx"]

TEST_SOLUTION_ARCHIVE_PATH = os.path.join(os.environ['HOME'], 'LetterBoxed/unit_test/test_archive')


@fixture(scope="module")
def default_lbg():
    lbg = LetterBoxGame()
    lbg.letter_sets = DEFAULT_SETS
    lbg.super_set = ''.join(lbg.letter_sets)
    yield lbg
    lbg.letter_sets = []
    lbg.reset_stats()


@fixture(scope="module")
def test_archive_path():
    os.makedirs(TEST_SOLUTION_ARCHIVE_PATH, exist_ok=True)
    yield
    rmtree(TEST_SOLUTION_ARCHIVE_PATH)


def test_clear_set(default_lbg):

    assert(default_lbg.letter_sets != [])
    default_lbg.clear_sets()
    assert(default_lbg.letter_sets == [])

def test_add_set(default_lbg):
    orig_sets = default_lbg.letter_sets

    default_lbg.add_set('xyz')
    assert(default_lbg.letter_sets == orig_sets)

    default_lbg.clear_sets()
    new_sets = ['mno', 'pqr', 'stu', 'vwx']
    expected_sets = [i for i in new_sets]
    for i in range(0, MAX_NUM_LETTER_SETS):
        default_lbg.add_set(new_sets[i])

        assert(default_lbg.letter_sets == expected_sets[:i+1])
    

def test_super_set_coverage(default_lbg):
    assert default_lbg.super_set_coverage("fade") == 4

def test_init(default_lbg):

    assert(len(default_lbg.letter_sets) == 4)
    assert(len(default_lbg.super_set) == 12)
    assert(len(default_lbg.solutions) == 0)

def test_save_solution_file(default_lbg, test_archive_path):

    default_lbg.solution_path = TEST_SOLUTION_ARCHIVE_PATH

    default_lbg.solutions = [['a','b'],['c','d','e'],['f','g','h','i']]

    default_lbg.save_solution_file(2)
    with open(default_lbg.solution_path + f'/length_2_solutions.txt', 'r') as f:
        lines = [s.strip('\n') for s in f.readlines()]
        assert len(lines) == 1
        assert lines[0] == "['a', 'b']"

    default_lbg.save_solution_file(3)
    with open(default_lbg.solution_path + f'/length_3_solutions.txt', 'r') as f:
        lines = [s.strip('\n') for s in f.readlines()]
        assert len(lines) == 1
        assert lines[0] == "['c', 'd', 'e']"

    default_lbg.save_solution_file(4)
    with open(default_lbg.solution_path + f'/length_4_solutions.txt', 'r') as f:
        lines = [s.strip('\n') for s in f.readlines()]
        assert len(lines) == 1
        assert lines[0] == "['f', 'g', 'h', 'i']"

    default_lbg.save_solution_file(2)
    default_lbg.save_solution_file(3)
    default_lbg.save_solution_file(4)

    with open(default_lbg.solution_path + f'/length_2_solutions.txt', 'r') as f:
        lines = [s.strip('\n') for s in f.readlines()]
        assert len(lines) == 1
        assert lines[0] == "['a', 'b']"
    
    with open(default_lbg.solution_path + f'/length_3_solutions.txt', 'r') as f:
        lines = [s.strip('\n') for s in f.readlines()]
        assert len(lines) == 1
        assert lines[0] == "['c', 'd', 'e']"

    with open(default_lbg.solution_path + f'/length_4_solutions.txt', 'r') as f:
        lines = [s.strip('\n') for s in f.readlines()]
        assert len(lines) == 1
        assert lines[0] == "['f', 'g', 'h', 'i']"

    for i in range(10):
        default_lbg.save_solution_file(2)
        default_lbg.save_solution_file(3)
        default_lbg.save_solution_file(4)

    with open(default_lbg.solution_path + f'/length_2_solutions.txt', 'r') as f:
        lines = [s.strip('\n') for s in f.readlines()]
        assert len(lines) == 1
        assert lines[0] == "['a', 'b']"
    
    with open(default_lbg.solution_path + f'/length_3_solutions.txt', 'r') as f:
        lines = [s.strip('\n') for s in f.readlines()]
        assert len(lines) == 1
        assert lines[0] == "['c', 'd', 'e']"

    with open(default_lbg.solution_path + f'/length_4_solutions.txt', 'r') as f:
        lines = [s.strip('\n') for s in f.readlines()]
        assert len(lines) == 1
        assert lines[0] == "['f', 'g', 'h', 'i']"

    default_lbg.solutions = [['x', 'y', 'z']]
    default_lbg.save_solution_file(3)
    with open(default_lbg.solution_path + f'/length_3_solutions.txt', 'r') as f:
        lines = [s.strip('\n') for s in f.readlines()]
        assert len(lines) == 2
        assert lines[1] == "['x', 'y', 'z']"
    