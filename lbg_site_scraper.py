from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from json import loads

LETTER_BOXED_URL = 'https://www.nytimes.com/puzzles/letter-boxed'


# DEPRECATED:
# The below XPATHs are the pointers to the proper elements just by copying
# the exact XPATH from the site using Inspect.
# Problem is, it changes whenever the website devs restructure the code.
# The bottom one is the new one after a change on 10/30/2023, which caused a loss
# of one month's worth of data.
# A new solution was clearly required (see below).
#
# MAGIC_XPATH = "/html/body/div[2]/div/div[2]/div[2]/div[5]/script"
# MAGIC_XPATH = "/html/body/div[2]/div[2]/div[2]/div[5]/script"

# MAGIC_CSS_SELECTOR = "#js-hook-pz-moment__game > script:nth-child(4)"


# Current Solution:
# This search string grabs all "script" XPATH elements and looks in the "text" property
# for the string 'window.gameData'.
# This should be more robust to changes, as long as the element type (script) and the name of the
# gameData struct remain the same.
XPATH_SEARCH_STR = "//script[contains(text(), 'window.gameData')]"

def scrape_lbg_data():

    def get_data():

        SELECT = ['ourSolution', 'dictionary', 'sides', 'date', 'par']

        data_elem = browser.find_element(By.XPATH, XPATH_SEARCH_STR)
        text = data_elem.get_property("text")
        idx = text.index('{')
        json_text = text[idx:]
        orig_dict = loads(json_text)
        return {k: orig_dict[k] for k in orig_dict.keys() if k in SELECT}

    op = webdriver.ChromeOptions()
    op.add_argument(argument="headless=new")
    browser = webdriver.Chrome(options=op)
    browser.get(LETTER_BOXED_URL)

    data = get_data()

    for k in ['ourSolution', 'dictionary', 'sides']:
        data[k] = [i.lower() for i in data[k]]

    browser.close()

    return data


if __name__ == "__main__":

   data = scrape_lbg_data()
   print(data.keys())
   print(f"{data['date']}")
   print(f"The sides are {data['sides']}")
   print(f"The par is {data['par']}")
   print(f"top of dictionary is {data['dictionary'][:10]}")