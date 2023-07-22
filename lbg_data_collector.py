import letter_box_game
import time

if __name__ == "__main__":

    TEST_CONFIG = {
        1: 10,
        2: 10,
        3: 10,
        4: 10,
        5: 10,
        6: 10,
        7: 10,
        8: 10,
        9: 10,
        10: 10,
        20: 2,
        30: 2,
        40: 2,
        50: 2,
    }
    start = time.time()
    lbg_unit = letter_box_game.LetterBoxGame()
    for counter_val, num_trials in TEST_CONFIG.items():

        for i in range(0,num_trials):

            lbg_unit.reset_stats()
            lbg_unit.break_out_counter = counter_val
            lbg_unit.solve()
    
    duration = time.time() - start
    print(f"Data Collection complete. Runtime: {duration} sec")