from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys


def main():
    options = Options()
    options.headless = True
    with Firefox(options=options) as driver:
        driver.implicitly_wait(10)
        ## instructions


if __name__ == "__main__":
    main()
