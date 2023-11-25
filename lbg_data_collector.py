import letter_box_game
import time
import logging
import os

from datetime import date
LOG_PATH = os.path.join(os.environ["HOME"], "LetterBoxed/solutions_archive/", str(date.today()), ".data_colector_log.log")
print(f"logging to {LOG_PATH}")
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)


logging.basicConfig(filename=LOG_PATH, encoding='utf-8', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
LOG = logging.getLogger()

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
    LOG.info(f"starting data collection at {start}")
    lbg_unit = letter_box_game.LetterBoxGame()
    for counter_val, num_trials in TEST_CONFIG.items():

        LOG.info(f"Starting trails for counter_val: {counter_val}")

        for i in range(0,num_trials):

            LOG.info(f"Starting trail number: {i}")

            lbg_unit.reset_stats()
            lbg_unit.break_out_counter = counter_val
            lbg_unit.solve()
    
    duration = time.time() - start
    LOG.info(f"Data Collection complete. Runtime: {duration} sec")